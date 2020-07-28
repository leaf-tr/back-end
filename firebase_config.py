import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

config = {
  "apiKey": "AIzaSyCjw2rUF3s2Vi9NhL4D_aAjPmx_2mbrigI",
  "authDomain": "leaf-tr.firebaseapp.com",
  "databaseURL": "https://leaf-tr.firebaseio.com",
  "projectId": "leaf-tr",
  "storageBucket": "leaf-tr.appspot.com",
  "messagingSenderId": "757674002843",
  "appId": "1:757674002843:web:2a8c198a998a955f61b93e",
  "measurementId": "G-3CTQ4JYRXG"
}

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, config)

db = firestore.client()