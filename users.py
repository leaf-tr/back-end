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
 
class User(object):
  def __init__(self, fname, lname, ReadingiLbrary):
    self.fname = fname
    self.lname = lname
    self.ReadingLibrary = []

  @staticmethod
  def from_dict(source):
    user = User(source[u'fname'], source[u'lname'], source[u'ReadingLibrary'])
    
    return user

  def to_dict(self):
    dest = {
      u'fname': self.fname,
      u'lname': self.lname,
      u'ReadingLibrary': self.ReadingLibrary
    }

    return dest

  def __repr__(self):
    return(
      f'User(\
          fname={self.fname}, \
          lname={self.lname}, \
          ReadingLibrary={self.ReadingLibrary}\
        )'
    )