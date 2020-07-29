from flask import render_template
from flask_cors import CORS
import connexion

import logging

# Create the application instance
app = connexion.FlaskApp(__name__)
# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')

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

# @app.after_request
# def add_headers(response):
#     response.headers.add('Content-Type', 'application/json')
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Expose-Headers', 'Content-Type,Content-Length,Authorization,X-Pagination')
#     return response

# logging.basicConfig(level=logging.DEBUG)

if __name__=='__main__':
  app.run(host='0.0.0.0', debug=True, port=5000)