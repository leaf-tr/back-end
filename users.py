"""
This is the users module and supports all the ReST actions for the
USERS collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort


def get_timestamp():
  return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

USERS = {
  "dhjfhsdj": {
    "username": "emma97",
    "readingLibrary": {
      "hdasje1dl13": {
        "author": "John Steinbeck",
        "title": "East of Eden",
        "isbn": 9780142000656,
        "startedReading": get_timestamp(),
        "finishedReading": get_timestamp(),
        "imgUrl": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1544744853l/4406._SY475_.jpg" 
      },
      "asdsa4152dss": {
        "author": "Andy Weir",
        "title": "The Martian",
        "isbn": 9780804139021,
        "startedReading": get_timestamp(),
        "finishedReading": get_timestamp(),
        "imgUrl": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1413706054l/18007564.jpg"
      },
    }
  }
}

# GET api/users/{id}
def get_by_id(user_id):
  pass

# GET api/users/{id}/reading-library
def get_reading_library(user_id):
  if user_id in USERS:
    reading_library = USERS[user_id]["readingLibrary"]
  else:
    abort(
            404, "User with id {user_id} not found".format(user_id=user_id)
        )
  return reading_library