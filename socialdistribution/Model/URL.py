# from .db import db

class URL(db.Model):
    
    URL_id = Column(db.Integer, unique=True, primary_key=True)
    
    post_id = Column(db.Integer, unique=True, db.ForignKey('Post.post_id'))
    
    comment_id = Column(db.Integer, db.ForignKey('Comments.comment_id'))
    
    URL_link = Column(db.String(2048))
    
    URL_type = Column(db.Integer)
