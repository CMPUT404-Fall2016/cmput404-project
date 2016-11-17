from db import db
from Posts import *

class Comments(db.Model):
    
    __tablename__ = 'comments'
    
    comment_id = db.Column(db.String(33), primary_key=True, unique=True)
    
    post_id = db.Column(db.String(33), db.ForeignKey('posts.post_id'))
    
    comment_text = db.Column(db.String(800))
    
    creation_time = db.Column(db.DateTime)
    
    #    UniqueConstraint('post_id', name = 'uix_1')
    
    def __new__(cls, datum = None):
        
        """
            Input: See comments in __init__
            
            Description:
            Checks whether comment_id is inside datum dictionary.
            If not found, then it returns None
            """
        
        if datum == None:
            return super(Comments, cls).__new__(cls)
        
        if ('comment_id' and 'post_id') not in datum.keys():
            return None
        
        else:
            return super(Comments,cls).__new__(cls)

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
            return

        empty_string=""
            
        self.comment_id = datum["comment_id"]

        if "comment_text" in datum.keys():
            self.comment_text = datum["comment_text"]
        else:
            self.comment_text = empty_string

        if "creation_time" in datum.keys():
            self.creation_time = datum["creation_time"]

        self.post_id = datum["post_id"]



    def __repr__(self):
        return '<User %r>' % (self.comment_text)

# db.create_all()
