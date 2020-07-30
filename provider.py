'''
provider module for managing provider OAuth and callback routes
'''

from flask import redirect

from oauth import OAuthSignIn

from db_access import save_access_token_to_db

def oauth_authorize(provider):
  '''
  '''
  oauth = OAuthSignIn.get_provider(provider)
  return oauth.authorize()

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
  return redirect('http://localhost:3000')
