# from .db import db

from db import db
from Authors import *
from model import *
import uuid

class Posts(db.Model):
    
    __tablename__ = 'posts'

    post_id = db.Column(db.String(100), primary_key=True)
    
    title = db.Column(db.String(64))
    
    description = db.Column(db.String(128))

    content_type = db.Column(db.String(33))

    content = db.Column(db.String(800))
    
    creation_time = db.Column(db.DateTime)
    
    view_permission = db.Column(db.Integer)
    
    post_type = db.Column(db.Integer)
    
    numberOf_comments = db.Column(db.Integer)
    
    numberOf_URL = db.Column(db.Integer)
    
    numberOf_images = db.Column(db.Integer)

    author_id = db.Column(db.String(100), db.ForeignKey('authors.author_id'))
    
    comments = db.relationship('Comments', backref = 'comm', lazy = 'dynamic')

#    UniqueConstraint('post_id', name = 'uix_1')

    def __new__(cls, datum = None):
        
        """
            Input: See comments in __init__
            
            Description:
            Checks whether post_id is inside datum dictionary.
            If not found, then it returns None
        """
        
        if datum == None:
            return super(Posts, cls).__new__(cls)
		
        if 'post_id' and 'author_id' not in datum.keys():
	        return None
        else:
            return super(Posts,cls).__new__(cls)
    
    def __init__(self,datum=None):
        
        """
        Input:
        datum is a dictionary with keys as column names and values as their corresponding values.
        eg,
        
        Description:
        This constructor sets the values of fields based on datum dictionary. If any field
        is missing from datum, its default value will be inserted.
        
        TODO:

        """
        if datum == None:
            self.post_id = uuid.uuid4().hex
            return

        
        self.post_id = datum["post_id"]
        
        if "title" in datum.keys():
            self.title = datum["title"]
        else:
            self.title = empty_string
        
        if "content" in datum.keys():
            self.content = datum["content"]
        
        if "description" in datum.keys():
            self.description = datum["description"]


        if "creation_time" in datum.keys():
            self.creation_time = datum["creation_time"]
        
        if "view_permission" in datum.keys():
            self.view_permission = datum["view_permission"]


        if "content_type" in datum.keys():
            self.content_type = datum["content_type"]


        self.author_id = datum["author_id"]



    def __repr__(self):
        return '<User %r>' % (self.post_id)



# db.create_all()
