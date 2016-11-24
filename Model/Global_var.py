from db import db
from model import *
import uuid

class Global_var(db.Model):
    
    __tablename__ = 'global_variables'
    
    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.String(7000))
