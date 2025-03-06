import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TESTING = True

#removed (was present in original version)
SECRET_KEY = ''

SQLALCHEMY_DATABASE_URI = 'mysql://keeley:Ch3rrieP1e@cookbookdb.cookbookingfornerds.xyz/cookbookingfornerdsdb'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

STATIC_FOLDER = 'static'
TEMPLATES_FOLDER = 'templates'

