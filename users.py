"""
This is the users module and supports all the ReST actions for the
USERS collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort

from firebase_config import db 
import json

def get_timestamp():
  return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# POST api/users
# Authenticate user
def authenticate_user(user_data):
  # create a new user with given id
  # or replace existing user with new given data
  # firestore automatically creates / overwrites a document w/ given id
  db.collection('users').document(user_data.id).set(user_data)
  return "Authenticated user", 200

# GET api/users/{id}
def get_by_id(user_id):
  pass

# GET api/users/{id}/reading-library
def get_reading_library(user_id):
  pass

# PATCH api/users/{id}/reading-library
# param: dictionary with reading library values
def update_reading_library(user_id):
  pass