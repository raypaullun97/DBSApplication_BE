import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import urllib
import logging

app = Flask(__name__)  # Standard Flask app

params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                 "SERVER=(local);"
                                 "DATABASE=test2;"
                                 "Trusted_Connection=yes")

# app.config['SQLALCHEMY_DATABASE_URI'] = ("mssql+pyodbc:///?odbc_connect={}".format(params))
# db = SQLAlchemy(app)
# logging.debug("DB setup complete")

@app.route("/")
def hello():
    """
    Hello world on root path
    """
    logging.debug("GET '/'")
    # db.session.close()
    return {"message" : "Hello world"}

def runner():
    app.run(host='0.0.0.0', port=os.environ.get('listenport', 8080))



