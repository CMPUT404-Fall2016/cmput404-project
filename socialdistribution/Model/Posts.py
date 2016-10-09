# from .db import db

class Posts(db.Model):

    post_id = Column(db.Integer, unique=True, primary_key=True)
    
    title = Column(db.String(64))
    
    text = Column(db.String(800))
    
    creation_time = Column(db.DateTime)
    
    view_permission = Column(db.Integer)
    
    post_type = Column(db.Integer)
    
    numberOf_comments = Column(db.Integer)
    
    numberOf_URL = Column(db.Integer)
    
    numberOf_images = Column(db.Integer)
