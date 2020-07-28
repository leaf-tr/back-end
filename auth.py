from os import environ as env
from dotenv import load_dotenv, find_dotenv
import constants

from requests_oauthlib import OAuth1Session

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Goodreads credentials
GOODREADS_KEY = env.get(constants.GOODREADS_KEY)
GOODREADS_SECRET = env.get(constants.GOODREADS_SECRET)
VERIFIER = 'goodreads_verifier'

print(GOODREADS_KEY, GOODREADS_SECRET)
if GOODREADS_KEY == None or GOODREADS_SECRET == None:
  print('You need to specify Goodreads key and secret in .env file')


# OAuth endpoints given in the Goodreads API documentation
# https://www.goodreads.com/api/documentation#oauth
request_token_url = 'https://www.goodreads.com/oauth/request_token'
authorize_url = 'https://www.goodreads.com/oauth/authorize'
access_token_url = 'https://www.goodreads.com/oauth/access_token'

# Fetch a request token
goodreads = OAuth1Session(GOODREADS_KEY,
    client_secret=GOODREADS_SECRET, 
    callback_uri='http://localhost:3000/',
    verifier=VERIFIER)

goodreads.fetch_request_token(request_token_url)

# Redirect user to Goodreads for authorization
authorization_url = goodreads.authorization_url(authorize_url)
print ('Please go here and authorize,', authorization_url)

redirect_response = input('Paste the full redirect URL here:')
goodreads.parse_authorization_response(redirect_response)

print(goodreads.parse_authorization_response(redirect_response))

# Fetch the access token
goodreads.fetch_access_token(access_token_url)

# print(goodreads.fetch_access_token(access_token_url))

r = goodreads.get('https://www.goodreads.com/api/auth_user')

print(r.content)
# Get id of user who authorized OAuth
# Get an xml response with the Goodreads user_id for the user who authorized access using OAuth. You'll need to register your app (required).
# URL: https://www.goodreads.com/api/auth_user
# HTTP method: GET

# ask Goodreads for a request token
# pass Developer key and secret
# client = oauthlib.oauth1.Client(GOODREADS_KEY, client_secret=GOODREADS_SECRET)
# uri, headers, body = client.sign()

# # redirect to the authorization page of the OAuth provider
# # get user's permission to exchange request token for an access token
# client = oauthlib.oauth1.Client(GOODREADS_KEY, client_secret=GOODREADS_SECRET,
#   resource_owner_key='the_request_token', resource_owner_secret='the_request_token_secret',
#   verifier='the_verifier')
# uri, headers, body = client.sign('http://example.com/access_token')

# # receive access token and a new token secret to access protected resources
# client = oauthlib.oauth1.Client(GOODREADS_KEY, client_secret='your_new_secret',
#   resource_owner_key='the_access_token', resource_owner_secret='the_access_token_secret')
# uri, headers, body = client.sign('http://example.com/protected_resource')





