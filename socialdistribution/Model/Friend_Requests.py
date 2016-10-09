# from .db import db

class Friend_Requests(db.Model):
    
    friendrequests = Column(db.Integer, unique=True, primary_key = True)
    
    fromAuthor_id = Column(db.Integer, unique=True, db.ForignKey('Authors.author_id'))
    
    fromAuthorServer_index = Column(db.Integer, unique=True)
    
    toAuthor_id = Column(db.Integer, unique=True, db.ForignKey('Authors.author_id'))
    
    toAuthorServer_index = Column(db.Integer, unique=True)
    
    isChecked = Column(db.Boolean)
