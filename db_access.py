from firebase_config import db 

def save_access_token_to_db(provider, token, user_id, provider_user_id=None):
  data_obj = {
    provider: {
      "token": token,
      "userId": provider_user_id
      }
    }
  db.collection('users').document(user_id).update(data_obj)

def restore_access_token_from_db(provider, user_id):
  user_data = db.collection('users').document(user_id).get().to_dict()
  return user_data[provider]
