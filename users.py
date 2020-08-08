"""
This is the users module and supports all the ReST actions for the
USERS collection
"""

# System modules
from datetime import datetime
import json

from flask_login import (LoginManager,
                         UserMixin,
                         login_required,
                         login_user,
                         logout_user,
                         current_user)
  
from flask import g

from db_access import restore_access_token_from_db

from main import login_manager

class User(object):
  def __init__(self, fname, lname, readingLibrary):
    self.fname = fname
    self.lname = lname
    self.readingLibrary = []

  @staticmethod
  def from_dict(source):
    user = User(source[u'fname'], source[u'lname'], source[u'readingLibrary'])
    
    return user

  def to_dict(self):
    dest = {
      u'fname': self.fname,
      u'lname': self.lname,
      u'readingLibrary': self.readingLibrary
    }

    return dest

  def __repr__(self):
    return(
      f'User(\
          fname={self.fname}, \
          lname={self.lname}, \
          readingLibrary={self.readingLibrary}\
        )'
    )

def get_timestamp():
  ''' time formatting '''
  return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

@login_manager.user_loader
def authenticate_user(user_data):
  '''
    POST api/users

    create a new user with given id or
    replace existing user with new given data
    firestore automatically creates / overwrites a document w/ given id

    for the sake of correct response code we could check if the user exists
  '''
  g.db.collection('users').document(user_data['id']).set(user_data['data'])
  return "Authenticated user", 201

def get_by_id(user_id):
  ''' GET api/users/{id} '''
  pass

# @login_required
def get_reading_library(user_id):
  ''' GET api/users/{id}/reading-library '''
  print("got user", user_id)
  return user_id

@login_required
def update_reading_library(user_id):
  '''
    PATCH api/users/{id}/reading-library
    param: dictionary with reading library values
  '''
  pass

@login_required
def sync_provider(user_id, provider_name):
  '''
    GET api/users/{id}/sync/{goodreads}
  '''
  # query db for user's provider access token
  provider_data = restore_access_token_from_db(user_id, provider_name)
  print(provider_data)
  # if there's no data for this provider
  # if not provider_data:
  #   # we have to send OAuth request
  #   if provider_name == 'goodreads':
      # return receive_goodreads_access_token(user_id)

  # provider_user_id = provider_data['userId']
  # provider_oauth_token = provider_data['token']['oauth_token']
  # provider_oauth_token_secret = provider_data['token']['oauth_token_secret']
  # # provider has 
  # if provider_data.get('token'):
  #   print(token)
  pass
 

