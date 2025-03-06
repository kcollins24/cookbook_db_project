import requests
import cloudscraper
from bs4 import BeautifulSoup


def scrape_recipe(link):
    scraper=cloudscraper.CloudScraper()
    html=scraper.get(link).text

    soup=BeautifulSoup(html,'lxml')
    recipe_info={}

    for tag in soup.find_all('script'):
        find_type=set(str(tag.string).split('"'))
        if '@type' in find_type and 'Recipe' in find_type:
            content=tag.string.split(':')
            meaningful_content=[]
            for string_list in content:
                string_list=string_list.split('"')
                counter=0
                for string in string_list:
                    if counter%2==1:
                        meaningful_content.append(string)
                    counter+=1
            check_name=True
            instructions=False
            ingredients=False
            required_fields=['title','time','yield','ingredients','instructions','description','category']
            for pos,item in enumerate(meaningful_content):
                if instructions==True:
                    if item=='text':
                        inst_string+=meaningful_content[pos+1][:-2]
                if item == 'recipeInstructions':
                    ingredients = False
                if item == 'recipeInstructions' and meaningful_content[pos+1]=='@type':
                    instructions = True
                    inst_string=''
                if item == 'recipeInstructions' and meaningful_content[pos+1]!='@type':
                    recipe_info['instructions']=meaningful_content[pos+1]
                if ingredients==True:
                    recipe_info['ingredients'].append(item)
                if item == 'name' and check_name==True:
                    recipe_info['title']=meaningful_content[pos+1]
                if item == 'description':
                    recipe_info['description']=meaningful_content[pos+1]
                if item == 'recipeYield':
                    recipe_info['yield']=meaningful_content[pos+1]
                if item == 'totalTime':
                    recipe_info['time']=meaningful_content[pos+1][2:]
                if item == 'recipeCategory':
                    instructions=False
                    recipe_info['category']=meaningful_content[pos+1]
                if item == 'recipeCuisine':
                    instructions=False
                    if 'instructions' not in recipe_info:
                        recipe_info['instructions']=inst_string
                    break
                if item == 'NutritionInformation':
                    instructions=False
                    if 'instructions' not in recipe_info:
                        recipe_info['instructions']=inst_string
                    break
                if item == 'recipeIngredient':
                    recipe_info['ingredients']=[]
                    check_name=False
                    ingredients=True
            for item in required_fields:
                if item not in recipe_info:
                    recipe_info[item]='not found'
    return recipe_info
