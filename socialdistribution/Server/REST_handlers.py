

class RestHandlers():
	"""
	This class implements functionality based on the specifications in:
	https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/example-article.json
	"""

	def __init__(self):
		self.authenticatedUsers=[]
		pass


	def getAllPosts(self, param=None):
		"""
		This will be called in response to :
		GET http://service/posts  (all posts marked as public on the server)

		Refer to top - 113
		"""
		pass


	def getVisiblePosts(self, param=None):
		"""
		This will be called in response to :
		GET http://service/author/posts  (posts that are visible to the currently authenticated user)
		
		Refer to top - 113
		"""
		pass


	def getVisiblePostsByAuthor(self, param=None):
		"""
		This will be called in response to :
		GET http://service/author/{AUTHOR_ID}/posts  (all posts made by {AUTHOR_ID} visible to the currently authenticated user)		

		Refer to top - 113
		"""
		pass


	def getPost(self, param=None):
		"""
		This will be called in response to :
		GET http://service/posts/{POST_ID}  access to a single post with id = {POST_ID}		
		
		Refer to top - 113
		"""
		pass


	def getComments(self, param=None):
		"""
		This will be called in response to :
		GET http://service/posts/{post_id}/comments  access to the comments in a post

		Refer to line 116-141
		"""
		pass


	def isFriend(self, param=None):
		"""
		This will be called in response to :
		GET http://service/friends/<authorid>  Checks whether the authenticated cliend author is friend with the author with "authorid" 

		Refer to line : 144-154		
		"""
		pass


	def isBothFriends(self, param=None):
		"""
		This will be called in response to :
		GET http://service/friends/<authorid1>/<authorid2>  Checks whether authorid1 author is friend with authorid2 author.		

		Refer to line : 156-169
		"""
		pass


	def areFriends_LIST(self, param=None):
		"""
		This will be called in response to :
		POST http://service/friends/<authorid>  POSTS a JSON containing lists of authorids and returns with a list containing those IDs 
		who are friend with authorid author

		Refer to line : 171-196
		"""
		pass


	# TODO: a method for finding out FOAF. Refer to line 198


	def makeFriendRequest(self, param=None):
	
		"""
		This will be called in response to :
		POST http://service/friendrequest  POSTS a JSON containing author info and the to be friended author's info and this sends a friendrequest
		
		refer to line 227-244
		"""
		pass


	def unFriend(self, param=None):

		"""
		This will be called in response to :
		POST http://service/unfriend  POSTS a JSON containing author info and to be unfriended author's info and this unfriends.
		
		This is an API that is not in the assigned specifications but we created this for unfriending.
		"""
		pass


	def getAuthor(self, param=None):

		"""
		This will be called in response to :
		GET http://service/author/<AUTHORID>  Retrieves profile information about AUTHORID author. 
		NOTE: The AUTHORID is not the same as authorid mentioned in above methods. We need to be sure what this is.

		Refer to line 248-273
		"""
		pass


