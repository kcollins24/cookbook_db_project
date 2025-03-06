#route declaration
from flask import current_app as app
from flask import request, make_response, session, flash
from datetime import datetime as dt
from .models import db, User, Cookbook, Recipe, Review
from .forms import CookbookForm, RecipeForm, ReviewForm, SearchForm, RecipeFromURLForm
from flask_login import current_user, login_required, logout_user
from .fetch_recipe import scrape_recipe

from flask import(
        Flask,
        url_for,
        render_template,
        redirect,
        Blueprint
)

# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@main_bp.route('/hello_<usr>', methods=['GET'])
@login_required
def usr_page(usr):
    """Logged-in User Page."""
    return render_template(
        'dashboard.jinja2',
        title='logged in page',
        template='dashboard-template',
        current_user=current_user,
        body="You are now logged in!",
        cookbooks=Cookbook.query.filter_by(owner=current_user.name).all()
    )

@main_bp.route('/<other_usr>')
@login_required
def other_usr_page(other_usr):
    return render_template(
        'other_user_dashboard.jinja2',
        title='page for other user',
        other_user=other_usr,
        cookbooks=Cookbook.query.filter_by(owner=other_usr).all()
    )

@main_bp.route('/ckbk_creation', methods=['GET','POST'])
@login_required
def ckbk_creation():
    form=CookbookForm()
    if form.validate_on_submit():
        ckbk= Cookbook(
            title=form.title.data,
            category= form.category.data,
            owner=current_user.name
            )
        db.session.add(ckbk)
        db.session.commit()
        return redirect (url_for('main_bp.usr_page',usr=current_user))
    return render_template('cookbook_f.jinja2', form=form)

@main_bp.route('/recipe_creation',methods=['GET','POST'])
@login_required
def recipe_creation():
    form=RecipeForm()
    cid = session.get('cid', None)
    if form.validate_on_submit():
        recipe= Recipe(
            title=form.title.data,
            authors= form.authors.data,
            url='manual entry',
            cooking_time=form.cooking_time.data,
            amount=form.amount.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            description=form.description.data,
            category=form.category.data,
            main_ingredient=form.main_ingredient.data,
            user_owner=current_user.name,
            ckbk_owner=int(cid)
            )
        db.session.add(recipe)
        db.session.commit()
        flash("success")
        return redirect (url_for('main_bp.dis_ckbk', cid=cid))
    else:
        flash(form.errors)
    return render_template('recipe_f.jinja2',form=form)

@main_bp.route('/recipe_creation_from_url',methods=['GET','POST'])
@login_required
def recipe_creation_from_url():
    form=RecipeFromURLForm()
    cid = session.get('cid', None)
    if form.validate_on_submit():
        link=form.url.data
        recipe_info=scrape_recipe(link)
        #print(recipe_info)
        if 'title' in recipe_info:
            recipe=Recipe(
                    title=recipe_info['title'],
                    authors=' ',
                    url=link,
                    cooking_time=recipe_info['time'],
                    amount=recipe_info['yield'],
                    ingredients=', '.join(recipe_info['ingredients']),
                    instructions=recipe_info['instructions'],
                    description=recipe_info['description'],
                    category=recipe_info['category'],
                    main_ingredient='love',
                    user_owner=current_user.name,
                    ckbk_owner=int(cid)
                    )
            db.session.add(recipe)
            db.session.commit()
        if len(recipe_info)==0:
            return render_template('sorry.jinja2')
        return redirect (url_for('main_bp.dis_ckbk', cid=cid))
    return render_template('recipe_url_f.jinja2',form=form)

@main_bp.route('/edit_recipe',methods=['GET','POST'])
@login_required
def edit_recipe():
    rid=session.get('rid',None)
    recipe=Recipe.query.get(int(rid))
    form=RecipeForm(obj=recipe)
    if form.validate_on_submit():
        form.populate_obj(recipe)
        db.session.commit()
        return redirect(url_for('main_bp.dis_recipe', rid=rid))
    return render_template('recipe_f.jinja2',form=form)

@main_bp.route('/leave_review',methods=['GET','POST'])
@login_required
def leave_review():
    form=ReviewForm()
    rid = session.get('rid',None)
    if form.validate_on_submit():
        review= Review(
                recipe_id=int(rid),
                comment=form.comment.data,
                stars=int(form.stars.data)
                )
        db.session.add(review)
        db.session.commit()
        flash("success")
        return redirect(url_for('main_bp.dis_recipe', rid=rid))
    else:
        flash(form.errors)
    return render_template('review_f.jinja2', form=form)

@main_bp.route('/ckbk'+'<cid>', methods=['GET','POST'])
@login_required
def dis_ckbk(cid):
    session['cid']=cid
    return render_template('cookbook_inside.jinja2',
        ckbk_info=Cookbook.query.filter_by(id=cid).all(),
        recipes=Recipe.query.filter_by(ckbk_owner=cid).all()
        )

@main_bp.route('/recipe'+'<rid>', methods=['GET','POST'])
@login_required
def dis_recipe(rid):
    session['rid']=int(rid)
    return render_template('recipe_inside.jinja2',
    recipes=Recipe.query.filter_by(id=rid).all(),
    comments=Review.query.filter_by(recipe_id=rid).all()
    )

@main_bp.route('/search_form', methods=['GET','POST'])
@login_required
def search():
    form=SearchForm()
    if form.validate_on_submit():
        search_param=[]
        title = request.form.get('title', None)
        if title!='':
            search_param.append("title like '%"+title+"%'")
        
        category = request.form.get('category',None)
        if category!='':
            search_param.append("category like '%"+category+"%'")
        
        if form.search_choice.data=='Recipes':
            main_ingredient= request.form.get('main_ingredient',None)
            if main_ingredient!='':
                search_param.append("main_ingredient like '%"+main_ingredient+"%'")
            
            min_rating = request.form.get('min_rating',None)
            conditions=' AND '.join(search_param)
            query="select * from recipe where"+conditions
            recipes=db.session.execute("select * from recipe where "+conditions).all()
            avg_ratings=[]

            if int(min_rating)!=0:
                ratings=db.session.execute("select stars, recipe_id from review, (select * from recipe where "+conditions+") as searched_recipes where searched_recipes.id=recipe_id").all()
                if len(ratings)>0:
                    for recipe in recipes:
                        avg_list=[]
                        for rating in ratings:
                            if int(rating[1])==int(recipe.id):
                                avg_list.append(int(rating[0]))
                        avg=float(sum(avg_list))/float(len(avg_list))
                        avg_ratings.append((recipe.id,avg))
            return render_template('search_page.jinja2', recipes=recipes,avg_ratings=avg_ratings,min_rating=float(min_rating), cookbooks=None)
        else:
            conditions=' AND '.join(search_param)
            query="select * from cookbook where"+conditions
            cookbooks=db.session.execute("select * from cookbook where "+conditions)
            return render_template('search_page.jinja2', cookbooks=cookbooks, recipes=None)
    return render_template('search_f.jinja2', form=form)

@main_bp.route('/site_stats')
@login_required
def stats():
    all_users=db.session.execute("select name from users").all()
    all_stats=[]
    for result in all_users:
        for name in result:
            stats=db.session.execute("select COUNT(distinct recipe.title) as recipe_number, COUNT(distinct cookbook.title) as ckbk_number, user_owner from recipe, cookbook where user_owner='"+name+"' and owner='"+name+"'").all()
            all_stats.append(stats)
    return render_template('stats_page.jinja2', all_stats=all_stats)

@main_bp.route('/search_page')
@login_required
def search_results():
    return render_template('search_page.jinja2')

@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))

@app.route('/')
def home():
    #landing page
    return render_template(
            'home.jinja2'
            )
