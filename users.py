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
  
from firebase_config import db

from db_access import restore_access_token_from_db

from main import login_manager

class User(object):
  def __init__(self, fname, lname, reading_library=[]):
    self.fname = fname
    self.lname = lname
    self.reading_library = reading_library

  @staticmethod
  def from_dict(source):
    user = User(source['fname'], source['lname'], source['reading_library'])
    
    return user

  def to_dict(self):
    dest = {
      'fname': self.fname,
      'lname': self.lname,
      'reading_library': self.reading_library
    }

    return dest

  def __repr__(self):
    return(
      f'User(\
          fname={self.fname}, \
          lname={self.lname}, \
          reading_library={self.reading_library}\
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
  db.collection('users').document(user_data['id']).set(user_data['data'])
  return "Authenticated user", 201

def get_by_id(user_id):
  ''' GET api/users/{id} '''
  pass

@login_required
def get_reading_library(user_id):
  ''' GET api/users/{id}/reading-library '''
  pass

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
 

