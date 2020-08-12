'''
provider module for managing provider OAuth and callback routes
'''

from flask import redirect
from flask_cors import cross_origin

from oauth import OAuthSignIn

from db_access import save_access_token_to_db

@cross_origin(supports_credentials=True)
def oauth_authorize(provider):
  '''
  '''
  oauth = OAuthSignIn.get_provider(provider)

  oauth_url = oauth.authorize()

  return oauth_url

@cross_origin(supports_credentials=True)
def oauth_callback(provider):
  '''
  '''
  # if not current_user.is_anonymous:
  #   return redirect(url_for('index'))
  oauth = OAuthSignIn.get_provider(provider)
  provider_user_id, access_token = oauth.callback()
  # user_id, token, provider, provider_user_id=None
  # save_access_token_to_db()
  print(provider_user_id, access_token)


  # if social_id is None:
  #   flash('Authentication failed.')
  #   return redirect(url_for('index'))
  # user = User.query.filter_by(social_id=social_id).first()
  # if not user:
  #   user = User(social_id=social_id, nickname=username, email=email)
  #   db.session.add(user)
  #   db.session.commit()
  # login_user(user, True)
  return redirect('http://localhost:3000/dashboard?authorizedProvider=1')
