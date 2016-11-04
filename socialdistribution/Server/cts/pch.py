from flask import jsonify
from sqlalchemy import exc
from model import *
from datetime import datetime
import time

random.seed(time.time())



class RestHandlers():
	"""
	This class implements functionality based on the specifications in:
	https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/example-article.json
	"""
	def __init__(self):
		self.authenticatedUser = 'admin' #get it from session



	def getAllPosts(self, param=None):
		"""
		This will be called in response to :
		GET http://service/posts  (all posts marked as public on the server)

		Refer to top - 113
		"""	
		# I assume for now view_permission = 1 -> public
		rtl = []
		posts = db.session.query(Posts).filter(Posts.view_permission == 1).all()	
		for post in posts:
			rtl.append([post, self.getImages(post.post_id), self.getComments(post.post_id)])
		return rtl


	def getVisiblePosts(self, param=None):
		"""
		This will be called in response to :
		GET http://service/author/posts  (posts that are visible to the currently authenticated user)
		
		Refer to top - 113
		"""
		#Firstly fetch all friends of the currently authenticated user
		friends = db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == self.authenticatedUser, Author_Relationships.relationship_type == 1).all()
		friends2 = db.session.query(Author_Relationships).filter(Author_Relationships.author2_id == self.authenticatedUser, Author_Relationships.relationship_type == 1).all()

		#firend AND/OR public 
		rtl = []
		for friend in friends:
			rtl = db.session.query(Posts).filter(Posts.author_id == friend.author2_id, Posts.view_permission == 2).all()	
		for friend in friends2:
			rtl += db.session.query(Posts).filter(Posts.author_id == friend.author1_id, Posts.view_permission == 2).all()	
		
		#self posts exclude public ones
		rtl += db.session.query(Posts).filter(Posts.author_id == self.authenticatedUser, Posts.view_permission != 1).all()	

		#all public ones
		rtl += db.session.query(Posts).filter(Posts.view_permission == 1).all()	

		#Todos
			#friend of friend
			#restrict to one user
		

		#public post exclude self's
		posts = self.sort_posts(rtl)	
		rtl = []
		for post in posts:
			rtl.append([post, self.getImages(post.post_id), self.getComments(post.post_id)])
		return rtl



	def getVisiblePostsByAuthor(self, user_id):
		"""
		This will be called in response to :
		GET http://service/author/{AUTHOR_ID}/posts  (all posts made by {AUTHOR_ID} visible to the currently authenticated user)		

		Refer to top - 113
		"""
		rtl = []

		#First step is determine the relationship of the two authors
		friendship = db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == self.authenticatedUser, Author_Relationships.author2_id == user_id).all()

		if not friendship:
			friendship = db.session.query(Author_Relationships).filter(Author_Relationships.author2_id == self.authenticatedUser, Author_Relationships.author1_id == user_id).all()

		if not friendship:
			#they are strangers
			rtl = db.session.query(Posts).filter(Posts.author_id == user_id, Posts.view_permission == 1).all()	
		else:
			#they are friends
			rtl = db.session.query(Posts).filter(Posts.author_id == user_id, Posts.view_permission <= 2).all()	
	
		#Todo:
		#Friend of Friend
		#Private to specific user 
		posts = rtl
		rtl = []
		for post in posts:
			rtl.append([post, self.getImages(post.post_id), self.getComments(post.post_id)])
		return rtl



	def getPost(self, post_id):
		"""
		This will be called in response to :
		GET http://service/posts/{POST_ID}  access to a single post with id = {POST_ID}		
		
		Refer to top - 113
		"""
		#Return a post with its images list and its comments list
		return [db.session.query(Posts).filter(Posts.post_id == post_id).first(), self.getImages(post_id), self.getComments(post_id)]



	def getComments(self, post_id):
		"""
		This will be called in response to :
		GET http://service/posts/{post_id}/comments  access to the comments in a post

		Refer to line 116-141
		"""
		#Get the comments of the post with post_id
		return db.session.query(Comments).filter(Comments.post_id == post_id).all()	



	def getImages(self, post_id):
		#Get the images of the post with post_id
		return db.session.query(Images).filter(Images.post_id == post_id).all()	



	def delete_post(self, post_id):
		#Fetch post that needs to be deleted
		d = db.session.query(Posts).filter(Posts.post_id == post_id).first()	
		cmts = db.session.query(Comments).filter(Comments.post_id == post_id).all()
		imgs = db.session.query(Images).filter(Images.post_id == post_id).all()
		#Delete the post from DB including its images and comments
		for cmt in cmts:
			self.delete_comment(cmt.comment_id)
		for img in imgs:
			self.delete_image(img.image_id)
		try:
			db.session.delete(d)
			db.session.commit()		
			#Successfully deleted the post
			return True
		except	exc.SQLAlchemyError:
			return False



	def delete_comment(self, comment_id):
		#Fetch comment that needs to be deleted
		d = db.session.query(Comments).filter(Comments.comment_id == comment_id).first()	
		#Delete the post from DB
		try:
			db.session.delete(d)
			db.session.commit()		
			#Successfully deleted the comment
			return True
		except	exc.SQLAlchemyError:
			return False



	def delete_Image(self, image_id):
		#Fetch Image that needs to be deleted
		d = db.session.query(Images).filter(Images.image_id == image_id).first()	
		#Delete the post from DB
		try:
			db.session.delete(d)
			db.session.commit()		
			#Successfully deleted the image
			return True
		except	exc.SQLAlchemyError:
			return False



	def make_post(self, data):
		#If the post comes with images, make them
		if data["images"]:
			self.make_Image(data)
		#Make the post 
		currentTime = datetime.now()
		post =	{
							"post_id" :	data["post_id"], #Need to change to self generated uuid
							"title"	:	data["title"],
							"text"	:	data["text"],
							"creation_time" :	currentTime,
							"view_permission" : data["view_permission"],
							"author_id"	:	data["author_id"]
						}		
		try:
			db.session.add(Posts(post))
			db.session.commit()
			return True
		except exc.SQLAlchemyError:
			return False
			


	def make_comment(self, data):
		currentTime = datetime.now()	
		comment = {
								"comment_id"	:	data["comment_id"],
								"post_id"	:	data["post_id"],
								"comment_text"	:	data["comment_text"],
								"creation_time"	:	data["creation_time"]
							}
		try:
			db.session.add(Comments(comment))
			db.session.commit()
			return True
		except	exc.SQLAlchemyError:
			return False
		



	#Add the images to the database
	def make_images(self, data):
		try:
			for image in data["images"]: 
				img =	{	
								"image_id"	:	data["image_id"], #Need to change to self generated uuid
								"post_id"	:	data["post_id"],
								"images"	:	image	#Do I need to decode to BLOB?
							}
				db.session.add(Images(img))
				db.session.commit()
			return True
		except exc.SQLAlchemyError:
			return False

	

	#This merge sort function sorts the posts based on creation time
	#Complexity:	O(n*log(n))
	def sort_posts(self, posts):
		result = []
		if len(posts) < 2:
			return posts
		mid = int(len(posts)/2)
		y = self.sort_posts(posts[:mid])
		z = self.sort_posts(posts[mid:])
		i = 0
		j = 0
		while i < len(y) and j < len(z):
			if y[i].creation_time < z[j].creation_time:
				result.append(z[j])
				j += 1
			else:
				result.append(y[i])
				i += 1
		result += y[i:]
		result += z[j:]
		return result


