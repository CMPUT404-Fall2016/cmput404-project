from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from pch import RestHandlers

handler = RestHandlers() # This will be the global REST_handlers object

'''
def getHandler():
	"""
	Use this method to retrieve the handler object. In case if handler object's availability/naming is 
	changed, just change code here and not worry about changing code in all of the below rest API classes! 
	"""
	return handler
'''


class AllPosts(Resource):

	"""
	Implements functionality regarding URL : http://service/posts  (all posts marked as public on the server)
 	Refer to REST_handlers.py , method : getAllPosts
	"""
	def get(self):

		return handler.getAllPosts()



class VisiblePosts(Resource):

	"""
	Implements functionality regarding URL : http://service/author/posts  (posts that are visible to the currently authenticated user)
 	Refer to REST_handlers.py , method : getVisiblePosts
	"""
	def get(self):
	
		return handler.getVisiblePosts()


class VisiblePostsByAuthor(Resource):

	"""
	Implements functionality regarding URL : http://service/author/{AUTHOR_ID}/posts  (all posts made by {AUTHOR_ID} visible to the currently authenticated user)
 	Refer to REST_handlers.py , method : getVisiblePostsByAuthor
	"""
	def get(self, author_id):

		return handler.getVisiblePostsByAuthor(author_id)


class Post(Resource):

	"""
	Implements functionality regarding URL : http://service/posts/{POST_ID}  access to a single post with id = {POST_ID}	
 	Refer to REST_handlers.py , method : getPost
	"""
	def get(self, post_id):
		
		return handler.getPost(post_id)


class Comments(Resource):

	"""
	Implements functionality regarding URL : http://service/posts/{post_id}/comments	
 	Refer to REST_handlers.py , method : getComments
	"""
	def get(self, post_id):

		return handler.getComments(post_id)


if __name__ == '__main__':
	app = Flask(__name__)
	api = Api(app)
	parser = reqparse.RequestParser()
	parser.add_argument('task')

	api.add_resource(AllPosts, '/service/posts')
	api.add_resource(VisiblePosts, '/service/author/posts')
	api.add_resource(VisiblePostsByAuthor, '/service/author/<int:author_id>/posts')	
	api.add_resource(Post, '/service/posts/<int:post_id>')	
	api.add_resource(Comments, '/service/posts/<int:post_id>/comments')	

	app.run(debug=True)


