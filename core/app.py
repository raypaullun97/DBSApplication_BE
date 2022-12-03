import logging
import os

from flask import Flask
app = Flask(__name__)  # Standard Flask app

@app.route("/")
def hello():
    """
    Hello world on root path
    """
    logging.debug("GET '/'")
    # db.session.close()
    return {"message" : "Hello world"}

@app.route("/details/<string:name>", methods=['POST'])
def get_account_details(name):
    logging.debug("GET '/details/name'")
    # db.session.close()
    return {"message": "Hello world"}

def runner():
    app.run(host='0.0.0.0', port=os.environ.get('listenport', 8080))



