'''

Auth module that manages OAuth with third-party providers

adapted from https://github.com/miguelgrinberg/flask-oauth-example/blob/master/
'''

import json
import xmltodict

from rauth import OAuth1Service
from flask import current_app, url_for, request, redirect, session

from constants import GOODREADS, GOODREADS_URLS, GENERAL

class OAuthSignIn(object):
  providers = None

  def __init__(self, provider_name):
    self.provider_name = provider_name
    credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
    self.consumer_id = credentials['id']
    self.consumer_secret = credentials['secret']

  def authorize(self):
    pass

  def callback(self):
    pass

  def get_callback_url(self):
    return url_for('/api.provider_oauth_callback',
      provider=self.provider_name, _external=True)

  @classmethod
  def get_provider(self, provider_name):
      if self.providers is None:
          self.providers = {}
          for provider_class in self.__subclasses__():
              provider = provider_class()
              self.providers[provider.provider_name] = provider
      return self.providers[provider_name]


class GoodreadsOAuth(OAuthSignIn):

  def __init__(self):
    super(GoodreadsOAuth, self).__init__('goodreads')
    self.service = OAuth1Service(
      name='goodreads',
      consumer_key = self.consumer_id,
      consumer_secret = self.consumer_secret,
      request_token_url = GOODREADS.BASE_URL + GENERAL.OAUTH + '/request_token',
      authorize_url = GOODREADS.BASE_URL + GENERAL.OAUTH + '/authorize',
      access_token_url = GOODREADS.BASE_URL + GENERAL.OAUTH + '/access_token',
      base_url = GOODREADS.BASE_URL
    )


  def authorize(self):
    '''
    '''
    request_token = self.service.get_request_token(
        params={'oauth_callback': self.get_callback_url()}
      )
    session['request_token'] = request_token

    return redirect(self.service.get_authorize_url(request_token[0]))


  def callback(self):
    '''
    '''
    request_token = session.pop('request_token')

    # Gets an access token, intializes a new authenticated session
    # with the access token. Returns an instance of session_obj
    oauth_session = self.service.get_auth_session(
      request_token[0], 
      request_token[1] # secret
    )

    # get access token from oauth_session
    access_token = oauth_session.access_token

    # use authenticated session to get user's goodreads id
    response = oauth_session.get('/api/auth_user')
    try:
      json_data = json.dumps(xmltodict.parse(response.content))
      provider_user_id = json.loads(json_data)['GoodreadsResponse']['user']['@id']
    except:
      return "Failed to convert xml response to json format"

    return provider_user_id, access_token

