from flask import render_template
from flask_cors import CORS

import connexion
import six
from werkzeug.exceptions import Unauthorized

import logging

# Create the application instance
app = connexion.FlaskApp(__name__)
# Read the swagger.yml file to configure the endpoints
app.add_api('api_config.yml')

CORS(app.app)

# Create a URL route in our application for "/"
@app.route("/")
def home():
  """
  This function just responds to the browser URL
  localhost:5000/
  :return:        the rendered template "home.html"
  """
  return render_template("home.html")

application = app.app

def decode_token(token):
  try:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
  except JWTError as e:
    six.raise_from(Unauthorized, e)

# logging.basicConfig(level=logging.DEBUG)

if __name__=='__main__':
  app.run(host='0.0.0.0', debug=True, port=5000)