from db import db
from Posts import Posts
from Comments import Comments

class URL(db.Model):
    
    URL_id = db.Column(db.String(33), primary_key=True)
    
    post_id = db.Column(db.String(33),  db.ForeignKey('posts.post_id'))
    
    comment_id = db.Column(db.String(33), db.ForeignKey('comments.comment_id'))
    
    URL_link = db.Column(db.String(2048))
    
    URL_type = db.Column(db.Integer)


    def __init__(self, datum=None):
                
        if datum == None:
            self.URL_id = uuid.uuid4().hex
            return

        self.URL_id = datum["URL_id"]

        #A URL Must Relates To A Post
        self.post_id = datum["post_id"]

        if "comment_id" in datum.keys():
            self.comment_id = datum["comment_id"]
        
        if "URL_link" in datum.keys():
            self.URL_link = datum["URL_link"]
        
        if "URL_type" in datum.keys():
            self.URL_type = datum["URL_type"]   

    
    # Get URL_id
    def get_uid(self):
        return self.URL_id

    
    #Change URL_link
    def set_link(self, link):
        db.session.query(URL).get(self.get_uid()).URL_link = link
        db.session.commit
        

# db.create_all()



