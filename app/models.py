from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User (UserMixin, db.Model):
    __tablename__= 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(
            db.Integer,
            primary_key=True
    )

    name = db.Column(
            db.String(64),
            index=False,
            unique=True,
            nullable=False
    )

    password = db.Column(
            db.String(200),
            index=False,
            unique=False,
            nullable=False
    )

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__ (self):
        return '<User {}>'.format(self.name)

class Cookbook (db.Model):
    __tablename__='cookbook'
    __table_args__ = {'extend_existing': True}
    id= db.Column(
            db.Integer,
            primary_key=True
    )

    title= db.Column(
            db.String(200),
            index=False,
            unique=False,
            nullable=False
    )

    category = db.Column(
            db.Text,
            index=False,
            unique=False,
            nullable=True
    )

    owner= db.Column(
            db.String(64),
            index=False,
            unique=False,
            nullable=False
    )

class Recipe (db.Model):
    __tablename__='recipe'
    __table_args__ = {'extend_existing': True}
    id= db.Column(
            db.Integer,
            primary_key=True
    )

    title= db.Column(
            db.String(200),
            index=False,
            unique=False,
            nullable=False
    )

    authors= db.Column(
            db.String(200),
            index=False,
            unique=False,
            nullable=False
    )

    url= db.Column(
            db.Text,
            index=False,
            unique=False,
            nullable=False
    )

    cooking_time= db.Column(
            db.String(200),
            index=False,
            unique=False,
            nullable=False
    )

    amount= db.Column(
            db.String(200),
            index=False,
            unique=False,
            nullable=False
    )

    ingredients= db.Column(
            db.Text,
            index=False,
            unique=False,
            nullable=False
    )

    instructions= db.Column(
            db.Text,
            index=False,
            unique=False,
            nullable=False
    )

    description= db.Column(
            db.String(200),
            index=False,
            unique=False,
            nullable=False,
    )

    category=db.Column(
            db.String(200),
            index=False,
            unique=False,
            nullable=False
    )

    main_ingredient= db.Column(
            db.String(200),
            index=False,
            unique=False,
            nullable=False
    )

    user_owner= db.Column(
            db.String(64),
            index=False,
            unique=False,
            nullable=False
    )

    ckbk_owner= db.Column(
            db.Integer,
            index=False,
            unique=False,
            nullable=False
    )

class Review (db.Model):
    __tablename__='review'
    id= db.Column(
            db.Integer,
            primary_key=True
    )

    recipe_id = db.Column(
            db.Integer,
            index=False,
            unique=False,
            nullable=False
    )

    comment = db.Column(
            db.Text,
            index=False,
            unique=False,
            nullable=True
    )

    stars= db.Column(
            db.Integer,
            index=False,
            unique=False,
            nullable=False
    )

