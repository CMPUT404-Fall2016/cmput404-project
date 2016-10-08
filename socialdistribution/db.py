#from flask import Flask
from flask_sqlalchemy import SQLAlchemy



# from yourapplication.database import db_session


db = SQLAlchemy()


'''
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
'''
