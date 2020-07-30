from firebase_config import db 
from constants import DATABASE_RESPONSES

def save_access_token_to_db(user_id, token, provider, provider_user_id=None):
  data_obj = {
    provider: {
      "token": token,
      "userId": provider_user_id
      }
    }
  try:
    db.collection('users').document(user_id).update(data_obj)
  except:
    return DATABASE_RESPONSES.ERROR

def restore_access_token_from_db(user_id, provider):
  user_data = db.collection('users').document(user_id).get().to_dict()
  return user_data.get(provider)
