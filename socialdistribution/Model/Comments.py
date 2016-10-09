# from .db import db

class Comments(db.Model):

    comment_id = Column(db.Integer, primary_key=True)
    
    post_id = Column(db.Integer, unique=True, db.ForignKey('post.post_id'))
    
    comment_text = Column(db.String(800))
    
    creation_time = Column(db.DateTime)
