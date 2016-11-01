#Unfinished imports
from Flask import jsonify


# Many queries may be possible to combine to make code clean

class RestHandlers():
	"""
	This class implements functionality based on the specifications in:
	https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/example-article.json
	"""

	def __init__(self):
		self.authenticatedUser = 'admin'
		pass


	def getAllPosts(self, param=None):
		"""
		This will be called in response to :
		GET http://service/posts  (all posts marked as public on the server)

		Refer to top - 113
		"""	
		# I assume for now view_permission = 1 -> public
		data = Posts.query.filter_by(view_permission = 1).all()

		rtl = []
		for post in data:
												
			rtl.append([post.post_id, post.title, post.text])	# For now just 3 fields
		
		return jsonify(posts = rtl)	



	def getVisiblePosts(self, param=None):
		"""
		This will be called in response to :
		GET http://service/author/posts  (posts that are visible to the currently authenticated user)
		
		Refer to top - 113
		"""
		#Firstly fetch all friends of the currently authenticated user
		firends = Author_Relationships.query.filter_by(author1_id = self.authenticatedUser).filter_by(relationship_type = 1).all()
		friends2 = Author_Relationships.query.filter_by(author2_id = self.authenticatedUser).filter_by(relationship_type = 1).all()

		#For each friend, fetch all posts of the friend that can be seen by the currently authenticated user
		rtl = []
		for friend in friends:
													#This is incomlete and more complicated, Deal it later
			data = Posts.query.filter_by(author_id = friend.author2_id).filter_by(view_permission = 2).all()
	
		for friend in friends2:
													#This is more complicated, Deal later
			data += Posts.query.filter_by(author_id = friend.author1_id).filter_by(view_permission = 2).all()
		
		#self posts
		data += Posts.query.filter_by(author_id = self.authenticatedUser).all()
		
		for post in data:
			rtl.append([post.post_id, post.title, post.text])	# For now just 3 fields
	

		#Todo:
		# What about friend of friend ? Maybe we need to revise our db design


		return jsonify(posts = rtl) + getAllPosts()	


	def getVisiblePostsByAuthor(self, param=None):
		"""
		This will be called in response to :
		GET http://service/author/{AUTHOR_ID}/posts  (all posts made by {AUTHOR_ID} visible to the currently authenticated user)		

		Refer to top - 113
		"""
		rtl = []

		#First step is determine the relationship of the two authors
		firendship = Author_Relationships.query.filter_by(author1_id = self.authenticatedUser).filter_by(author2_id = user_id).all()
		if(not friendship)
			friendship = Author_Relationships.query.filter_by(author2_id = self.authenticatedUser).filter_by(author1_id = user_id).all()

		if(not friendship):
			#they are strangers
			data = Posts.query.filter_by(author_id = user_id).filter_by(view_permission = 1).all()
			
		else:
			#they are friends
			data = Posts.query.filter_by(author_id = user_id).filter_by(view_permission <= 2).all()
	
		for post in data:
			rtl.append([post.post_id, post.title, post.text])	# For now just 3 fields
	
		#Todo:
		# What about friend of friend relationship (3) ? Maybe we need to revise our db design

		return jsonify(posts = rtl)	


	def getPost(self, param=None):
		"""
		This will be called in response to :
		GET http://service/posts/{POST_ID}  access to a single post with id = {POST_ID}		
		
		Refer to top - 113
		"""
		rtl = []

		post = Posts.query.filter_by(post_id = post_id).all()
		# Question:  What if the current user does not have permission or we give it anyway?

		for post in post:
			rtl.append([post.post_id, post.title, post.text])	# For now just 3 fields


		return jsonify(posts = rtl)


	def getComments(self, param=None):
		"""
		This will be called in response to :
		GET http://service/posts/{post_id}/comments  access to the comments in a post

		Refer to line 116-141
		"""
	

		comments = Comments.query.filter_by(post_id = post_id).all()

		for comment in comments:
			rtl.append([comment_id comment.text])	# For now just 2 fields
		

		return jsonify(comts = rtl)



