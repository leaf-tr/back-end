# credit to https://stackoverflow.com/questions/2682745/how-do-i-create-a-constant-in-python?rq=1

from collections import OrderedDict
from copy import deepcopy

class Constants(object):
    """Container of constant"""

    __slots__ = ('__dict__')

    def __init__(self, **kwargs):

        if list(filter(lambda x: not x.isupper(), kwargs)):
            raise AttributeError('Constant name should be uppercase.')

        super(Constants, self).__setattr__(
            '__dict__',
            OrderedDict(map(lambda x: (x[0], deepcopy(x[1])), kwargs.items()))
        )

    def sort(self, key=None, reverse=False):
        super(Constants, self).__setattr__(
            '__dict__',
            OrderedDict(sorted(self.__dict__.items(), key=key, reverse=reverse))
        )

    def __getitem__(self, name):
        return self.__dict__[name]

    def __len__(self):
        return  len(self.__dict__)

    def __iter__(self):
        for name in self.__dict__:
            yield name

    def keys(self):
        return list(self)

    def __str__(self):
        return str(list(self))

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, str(self.__dict__))

    def __dir__(self):
        return list(self)

    def __setattr__(self, name, value):
        raise AttributeError("Immutable attribute")

    def __delattr__(*_):
        raise AttributeError("Immutable attribute")

# url consts
GENERAL = Constants(
  API = '/api',
  OAUTH = '/oauth'
)

# Goodreads-specific consts
GOODREADS = Constants(
  PROVIDER = 'goodreads',
  KEY = 'GOODREADS_KEY',
  SECRET = 'GOODREADS_SECRET',
  BASE_URL = 'https://www.goodreads.com',
  VERIFIER = 'goodreads_verifier',
)

# OAuth endpoints given in the Goodreads API documentation
# https://www.goodreads.com/api/documentation

GOODREADS_URLS = Constants(
  REQUEST_TOKEN_URL = GOODREADS.BASE_URL + GENERAL.OAUTH + '/request_token',
  AUTHORIZE_URL = GOODREADS.BASE_URL + GENERAL.OAUTH + '/authorize',
  ACCESS_TOKEN_URL = GOODREADS.BASE_URL + GENERAL.OAUTH + '/access_token',
  GET_USER_ID = GOODREADS.BASE_URL + GENERAL.API +'/auth_user',
  GET_ALL_USERS_BOOKS = GOODREADS.BASE_URL + '/review/list?format=xml&v=2',
)
