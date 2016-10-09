# from .db import db

class Images(db.Model):

    image_id = Column(db.Integer, unique=True, primary_key=True)
    
    post_id = Column(db.Integer, unique=True, db.ForignKey('Post.post_id'))
    
    comment_id = Column(db.Integer, db.ForignKey('Comments.comment_id'))
    
    image = Column(db.LargeBinary)
