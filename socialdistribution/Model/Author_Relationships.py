# from .db import db

class Author_Relationships(db.Model):

    Author_Relationships = Column(db.Integer, primary_key=True)
    
    authorServer1_id = Column(db.Integer, unique= True)
    
    author1_id = Column(db.Integer, unique = True, db.ForignKey('Authors.author_id'))
    
    authorServer2_id = Column(db.Integer, unique=True)
    
    author2_id = Column(db.Integer, unique=True,db.ForignKey('Authors.author_id'))
    
    relationship_type = Column(db.Integer)
