from os import environ as env
from dotenv import load_dotenv, find_dotenv
from constants import GOODREADS, GOODREADS_URLS

from authlib.integrations.requests_client import OAuth1Session
from authlib.integrations.requests_client import OAuth1Auth

import requests
import xmltodict
import json

from db_access import save_access_token_to_db, restore_access_token_from_db


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Goodreads credentials
GOODREADS_KEY = env.get(GOODREADS.KEY)
GOODREADS_SECRET = env.get(GOODREADS.SECRET)
VERIFIER = GOODREADS.VERIFIER
PROVIDER = GOODREADS.PROVIDER

# print(GOODREADS_KEY, GOODREADS_SECRET)
if GOODREADS_KEY == None or GOODREADS_SECRET == None:
  raise ValueError('You need to specify GOODREADS_KEY and GOODREADS_SECRET in .env file')

# Ask for user's permission to access
# their personal Goodreads data
def receive_goodreads_access_token(user_id):

  # OAuth endpoints given in the Goodreads API documentation
  # https://www.goodreads.com/api/documentation#oauth
  REQUEST_TOKEN_URL = GOODREADS_URLS.REQUEST_TOKEN_URL
  AUTHORIZE_URL = GOODREADS_URLS.AUTHORIZE_URL
  ACCESS_TOKEN_URL = GOODREADS_URLS.ACCESS_TOKEN_URL

  # Fetch a request token
  goodreads = OAuth1Session(
      GOODREADS_KEY,
      GOODREADS_SECRET,
      token=None,
      token_secret=None,
      verifier=VERIFIER
      )

  # fetch temporary credential, which will be used to generate authorization URL
  request_token = goodreads.fetch_request_token(REQUEST_TOKEN_URL)
  print("request_token", request_token)

  # generate the authorization URL
  authorization_url = goodreads.create_authorization_url(AUTHORIZE_URL)
  print ('Please go here and authorize,', authorization_url)

  # fetch the access token with this response
  redirect_response = input('Paste the full redirect URL here:')
  goodreads.parse_authorization_response(redirect_response)

  access_token = goodreads.fetch_access_token(ACCESS_TOKEN_URL, VERIFIER)
  print("access_token", access_token)

  # When we are redirected to authorization endpoint, our session is over.
  # In this case, when the authorization server send us back to our server,
  # we need to create another session:
  oauth_token = access_token['oauth_token']
  oauth_token_secret = access_token['oauth_token_secret']

  auth = OAuth1Auth(
    client_id=GOODREADS_KEY,
    client_secret=GOODREADS_SECRET,
    token=oauth_token,
    token_secret=oauth_token_secret
    )

  GET_USER_ID_URL = GOODREADS_URLS.GET_USER_ID
  response = requests.get(GET_USER_ID_URL, auth=auth)
 
  # convert xml response to json and parse the user id
  json_data = json.dumps(xmltodict.parse(response.content))
  provider_user_id = json.loads(json_data)['GoodreadsResponse']['user']['@id']

  # close the session
  auth.close()

  # save to database
  save_access_token_to_db(PROVIDER, access_token, user_id, provider_user_id)

def refresh_user_library(user_id):
  goodreads_data = restore_access_token_from_db(PROVIDER, user_id)
  goodreads_user_id = goodreads_data['userId']
  oauth_token = goodreads_data['token']['oauth_token']
  oauth_token_secret = goodreads_data['token']['oauth_token_secret']

  # start auth session
  auth = OAuth1Auth(
    GOODREADS_KEY,
    GOODREADS_SECRET,
    token=oauth_token,
    token_secret=oauth_token_secret
    )  

  '''
  GET_ALL_USERS_BOOKS

  URL: https://www.goodreads.com/review/list?v=2
  Parameters:
  v: 2
  id: Goodreads id of the user
  shelf: read, currently-reading, to-read, etc. (optional)
  sort: title, author, cover, rating, year_pub, date_pub, date_pub_edition, date_started, date_read, date_updated, date_added, recommender, avg_rating, num_ratings, review, read_count, votes, random, comments, notes, isbn, isbn13, asin, num_pages, format, position, shelves, owned, date_purchased, purchase_location, condition (optional)
  search[query]: query text to match against member's books (optional)
  order: a, d (optional)
  page: 1-N (optional)
  per_page: 1-200 (optional)
  key: Developer key (required)

  '''

  test = '&per_page=2&shelf=read'
  GET_ALL_USERS_BOOKS_URL = GOODREADS_URLS.GET_ALL_USERS_BOOKS + test + '&id=' + goodreads_user_id
  
  response = requests.get(GET_ALL_USERS_BOOKS_URL, auth=auth)
  json_data = json.dumps(xmltodict.parse(response.content))

  total_books = json.loads(json_data)['GoodreadsResponse']['reviews']['@total']

  readingLibrary = []
  for item_data in json.loads(json_data)['GoodreadsResponse']['reviews']['review']:
    book_obj = {}
    shelves_list = []
    authors_list = []
   
    book_data = item_data['book']

    book_obj = {
      'isbn': book_data.get('isbn'),
      'isbn13': book_data.get('isbn13'),
      'title': book_data.get('title_without_series'),
      'seriesTitle': book_data.get('title'),
      'imageUrl': book_data.get('image_url'),
      'startedAt': item_data.get('started_at'),
      'startedAt': item_data.get('started_at'),
      'readAt': item_data.get('read_at'),
      'dateAdded': item_data.get('date_added'),
      'dateUpdated': item_data.get('date_updated'),
      'readCount': item_data.get('read_count'),
      'type': 'book'
    }
    # iterate over and save authors this book was written by
    for author in book_data['authors'].values():
      authors_list.append(author['name'])
    
    # iterate over and save shelves this book belongs to
    for shelf in item_data['shelves'].values():
      shelves_list.append(shelf['@name'])

    book_obj.update({
      'shelves': shelves_list,
      'authors': authors_list
    })
    
    readingLibrary.append(book_obj)

receive_goodreads_access_token('1YPwuwLecA6znkm6G5cz')
refresh_user_library('1YPwuwLecA6znkm6G5cz')