from flask import render_template
from flask_cors import CORS
import connexion

import logging
# Create the application instance
app = connexion.App(__name__)
# CORS(app)

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')

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

logging.basicConfig(level=logging.DEBUG)

if __name__=='__main__':
  app.run(host='0.0.0.0', debug=True, port=5000)