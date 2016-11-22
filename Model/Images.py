from db import db
from Posts import Posts;
from Comments import Comments
import uuid

class Images(db.Model):

    image_id = db.Column(db.String(33), primary_key=True)
    
    post_id = db.Column(db.String(33), db.ForeignKey('posts.post_id') )
    
    comment_id = db.Column(db.String(33), db.ForeignKey('comments.comment_id'))
    
    image = db.Column(db.LargeBinary)


    # Default Constructor
    def __init__(self, datum=None):
        if datum == None:
            self.image_id = uuid.uuid4().hex
            return

        self.image_id = datum["image_id"]   

        #A Image Must Relates To A Post
        self.post_id = datum["post_id"]

        if "comment_id" in datum.keys():
            self.comment_id = datum["comment_id"]
        
        self.image = datum["image"]

    
    # Get image id
    def get_iid(self):
        return self.image_id

    def set_postID(self, pid):
        #Later we need to make sure foreign key exists
        self.post_id = pid
    
    #Change Image
    def set_image(self, blob):
        db.session.query(Images).get(self.get_iid()).image = blob
        db.session.commit
        


# db.create_all()
