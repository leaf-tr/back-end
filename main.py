'''
main module of the application where middleware packages
such as CORS, connexion, and flask_login are connected
'''

import logging

from datetime import datetime, timedelta
from os import environ as env
from dotenv import load_dotenv, find_dotenv

from flask import render_template, session
from flask_login import LoginManager
from flask_cors import CORS

import connexion

from constants import GENERAL, GOODREADS

# load env variables
ENV_FILE = find_dotenv()
if ENV_FILE:
  load_dotenv(ENV_FILE)

# initialize LoginManager class
login_manager = LoginManager()

# Create the application instance
APP_INSTANCE = connexion.FlaskApp(__name__)

# Read the api_config.yml file to configure the endpoints
APP_INSTANCE.add_api('api_config.yml')

FLASK_APP = APP_INSTANCE.app

# get sensitive env vars from untracked .env file
GOODREADS_KEY = env.get(GOODREADS.KEY)
GOODREADS_SECRET = env.get(GOODREADS.SECRET)
SECRET_KEY = env.get(GENERAL.FLASK_SECRET)
FLASK_APP.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# make sure env vars exist
if GOODREADS_KEY is None or GOODREADS_SECRET is None or SECRET_KEY is None:
  raise ValueError('You need to specify {}, {}, {} \
    in .env file'.format(GOODREADS_KEY, GOODREADS_SECRET, SECRET_KEY))

# put env vars to good use
# FLASK_APP.config['SESSION_COOKIE_DOMAIN'] = 'http://127.0.0.1:3000'
FLASK_APP.config['SECRET_KEY'] = env.get(GENERAL.FLASK_SECRET)
FLASK_APP.config['OAUTH_CREDENTIALS'] = {
  'goodreads': {
    'id': GOODREADS_KEY,
    'secret': GOODREADS_SECRET
  }
}

# login_manager.init_app(FLASK_APP)

CORS(FLASK_APP)

# Create a URL route in our application for '/'
@APP_INSTANCE.route('/')
def home():
  '''
  This function just responds to the browser URL
  localhost:5000/
  :return:        the rendered template 'home.html'
  '''
  return render_template('home.html')


# logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
  FLASK_APP.run()
