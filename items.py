"""
This is the books module and supports all the ReST actions for the
BOOKS collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort


def get_timestamp():
  return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# Data to serve with our API
BOOKS = {
  "Adventures of Someone": {
      "author": "Doug Kl",
      "isbn": 44644578454812,
      "timestamp": get_timestamp(),
  },
  "Hello World": {
      "author": "Kent Powers",
      "isbn": 87684515454846,
      "timestamp": get_timestamp(),
  },
  "Easter": {
      "author": "Bunny Hop",
      "isbn": 12646515454814,
      "timestamp": get_timestamp(),
  },
}


def get_all():
  """
  This function responds to a request for /api/items
  with the complete lists of reading items
  :return:        json string of list of reading items for this user
  """
  # Create the list of books from our data
  return [BOOKS[key] for key in sorted(BOOKS.keys())]