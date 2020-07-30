from os import environ as env
from dotenv import load_dotenv, find_dotenv

from authlib.integrations.requests_client import OAuth1Session
from authlib.integrations.requests_client import OAuth1Auth

import requests
import xmltodict
import json

from constants import GOODREADS, GOODREADS_URLS, GENERAL

from db_access import save_access_token_to_db, restore_access_token_from_db

ENV_FILE = find_dotenv()
if ENV_FILE:
  load_dotenv(ENV_FILE)

# Goodreads credentials
GOODREADS_KEY = env.get(GOODREADS.KEY)
GOODREADS_SECRET = env.get(GOODREADS.SECRET)
PROVIDER = GOODREADS.PROVIDER

if GOODREADS_KEY is None or GOODREADS_SECRET is None:
  raise ValueError('You need to specify GOODREADS_KEY and GOODREADS_SECRET in .env file')


def refresh_user_library(user_id):
  goodreads_data = restore_access_token_from_db(user_id, PROVIDER)
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
  sort: title, author, cover, rating, year_pub, date_pub, date_pub_edition, date_started,
  date_read, date_updated, date_added, recommender, avg_rating, num_ratings, review,
  read_count, votes, random, comments, notes, isbn, isbn13, asin, num_pages, format,
  position, shelves, owned, date_purchased, purchase_location, condition (optional)
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