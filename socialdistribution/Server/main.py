from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from Server.REST_handlers import REST_handlers

handler = None # This will be the global REST_handlers object

def getHandler():
	"""
	Use this method to retrieve the handler object. In case if handler object's availability/naming is 
	changed, just change code here and not worry about changing code in all of the below rest API classes! 
	"""
	return handler


class Main():

	def __init__(self, app):
		self.app = app
		self.api = Api(app)
		parser = reqparse.RequestParser()
		parser.add_argument('task')

		pass


	def run(self):

	    app.run(debug=True)


class AllPosts(Resource):

	"""
	Implements functionality regarding URL : http://service/posts  (all posts marked as public on the server)
 	Refer to REST_handlers.py , method : getAllPosts
	"""
	def get():
		pass


class VisiblePosts(Resource):

	"""
	Implements functionality regarding URL : http://service/author/posts  (posts that are visible to the currently authenticated user)
 	Refer to REST_handlers.py , method : getVisiblePosts
	"""
	def get():
		pass


class VisiblePostsByAuthor(Resource):

	"""
	Implements functionality regarding URL : http://service/author/{AUTHOR_ID}/posts  (all posts made by {AUTHOR_ID} visible to the currently authenticated user)
 	Refer to REST_handlers.py , method : getVisiblePostsByAuthor
	"""
	def get():
		pass



class Post(Resource):

	"""
	Implements functionality regarding URL : http://service/posts/{POST_ID}  access to a single post with id = {POST_ID}	
 	Refer to REST_handlers.py , method : getPost
	"""
	def get():
		pass



class Comments(Resource):

	"""
	Implements functionality regarding URL : http://service/posts/{post_id}/comments	
 	Refer to REST_handlers.py , method : getComments
	"""
	def get():
		pass


# TODO: Refer to method: isFriend.. Have a confusion so I leave it for later.



class MutuallyFriend(Resource):

	"""
	Implements functionality regarding URL : http://service/friends/<authorid1>/<authorid2>  Checks whether authorid1 author is friend with authorid2 author.	
 	Refer to REST_handlers.py , method : isBothFriends
	"""
	def get():
		pass



class MultipleFriendship(Resource):

	"""
	Implements functionality regarding URL : http://service/friends/<authorid>  POSTS a JSON containing lists of authorids and returns with a list containing those IDs
 	Refer to REST_handlers.py , method : areFriends_LIST
	"""
	def post():
		pass



class MakeFriendship(Resource):

	"""
	Implements functionality regarding URL : http://service/friendrequest  POSTS a JSON containing author info and the to be friended author's info and this sends a friendrequest
 	Refer to REST_handlers.py , method : makeFriendRequest
	"""
	def post():
		pass



class RemoveFriend(Resource):

	"""
	Implements functionality regarding URL : http://service/unfriend  POSTS a JSON containing author info and to be unfriended author's info and this unfriends.
 	Refer to REST_handlers.py , method : unFriend
	"""
	def post():
		pass



class FetchAuthor(Resource):

	"""
	Implements functionality regarding URL : http://service/author/<AUTHORID>  Retrieves profile information about AUTHORID author.
 	Refer to REST_handlers.py , method : getAuthor
	"""
	def post():
		pass







