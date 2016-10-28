from db import db
from Posts import Posts;
from Comments import Comments

class Images(db.Model):

	image_id = db.Column(db.Integer, unique=True, primary_key=True)
    
	post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id') )
    
	comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'))
    
	image = db.Column(db.LargeBinary)


	# Default Constructor
	def __init__(self, datum):
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
