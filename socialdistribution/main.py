import flask
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
# from Server.REST_handlers import REST_handlers
import json
import uuid
from model import *
from Server.author_endpointHandlers import *


# admin stuff -----------------------------------
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView



import os
import os.path as op
from db import db

from wtforms import validators




from flask_admin.contrib import sqla
from flask_admin.contrib.sqla import filters
from flask_admin.form import rules
#------------------------------------------------





handler = None # This will be the global REST_handlers object
COOKIE_NAME = "cookie_cmput404_"
COOKIE_NAMES = ["cookie_cmput404_author_id","cookie_cmput404_session_id","cookie_cmput404_github_id"] 

def getHandler():
	"""
	Use this method to retrieve the handler object. In case if handler object's availability/naming is 
	changed, just change code here and not worry about changing code in all of the below rest API classes! 
	"""
	return handler




# def main(self, app):

app = Flask(__name__, static_url_path='')


app.config['SECRET_KEY'] = '123456790'

# Create admin
admin = Admin(app, name='Example: Admin', template_mode='bootstrap3')

# Add views
admin.add_view(ModelView(Authors, db.session))
admin.add_view(ModelView(Posts, db.session))
admin.add_view(ModelView(Images, db.session))
admin.add_view(ModelView(URL, db.session))





# api = Api(app)
# parser = reqparse.RequestParser()
# api.add_resource(Login, '/login/')
# api.add_resource(Registration, '/register/')



	# parser.add_argument('task')



	# def run(self):

	#     app.run(debug=True)


# class AllPosts(Resource):

# 	"""
# 	Implements functionality regarding URL : http://service/posts  (all posts marked as public on the server)
#  	Refer to REST_handlers.py , method : getAllPosts
# 	"""
# 	def get():
# 		pass


# class VisiblePosts(Resource):

# 	"""
# 	Implements functionality regarding URL : http://service/author/posts  (posts that are visible to the currently authenticated user)
#  	Refer to REST_handlers.py , method : getVisiblePosts
# 	"""
# 	def get():
# 		pass


# class VisiblePostsByAuthor(Resource):

# 	"""
# 	Implements functionality regarding URL : http://service/author/{AUTHOR_ID}/posts  (all posts made by {AUTHOR_ID} visible to the currently authenticated user)
#  	Refer to REST_handlers.py , method : getVisiblePostsByAuthor
# 	"""
# 	def get():
# 		pass



# class Post(Resource):

# 	"""
# 	Implements functionality regarding URL : http://service/posts/{POST_ID}  access to a single post with id = {POST_ID}	
#  	Refer to REST_handlers.py , method : getPost
# 	"""
# 	def get():
# 		pass



# class Comments(Resource):

# 	"""
# 	Implements functionality regarding URL : http://service/posts/{post_id}/comments	
#  	Refer to REST_handlers.py , method : getComments
# 	"""
# 	def get():
# 		pass


# # TODO: Refer to method: isFriend.. Have a confusion so I leave it for later.



# class MutuallyFriend(Resource):

# 	"""
# 	Implements functionality regarding URL : http://service/friends/<authorid1>/<authorid2>  Checks whether authorid1 author is friend with authorid2 author.	
#  	Refer to REST_handlers.py , method : isBothFriends
# 	"""
# 	def get():
# 		pass



# class MultipleFriendship(Resource):

# 	"""
# 	Implements functionality regarding URL : http://service/friends/<authorid>  POSTS a JSON containing lists of authorids and returns with a list containing those IDs
#  	Refer to REST_handlers.py , method : areFriends_LIST
# 	"""
# 	def post():
# 		pass



# class MakeFriendship(Resource):

# 	"""
# 	Implements functionality regarding URL : http://service/friendrequest  POSTS a JSON containing author info and the to be friended author's info and this sends a friendrequest
#  	Refer to REST_handlers.py , method : makeFriendRequest
# 	"""
# 	def post():
# 		pass



# class RemoveFriend(Resource):

# 	"""
# 	Implements functionality regarding URL : http://service/unfriend  POSTS a JSON containing author info and to be unfriended author's info and this unfriends.
#  	Refer to REST_handlers.py , method : unFriend
# 	"""
# 	def post():
# 		pass



# class FetchAuthor(Resource):

# 	"""
# 	Implements functionality regarding URL : http://service/author/<AUTHORID>  Retrieves profile information about AUTHORID author.
#  	Refer to REST_handlers.py , method : getAuthor
# 	"""
# 	def post():
# 		pass



def flask_post_json():
    '''Ah the joys of frameworks! They do so much work for you
       that they get in the way of sane operation!'''
    if (request.json != None):
        return request.json
    elif (request.data != None and request.data != ''):
        return json.loads(request.data)
    else:
        return json.loads(request.form.keys()[0])



def getResponse(body=None, cookie=None, custom_headers=None, status_code=None):
	"""
	Generates 
	"""
	if body == None:
		response = app.make_response("")
	else:
		response = app.make_response(json.dumps(body))
	response.mimetype = "application/json"

	if custom_headers != None:
		for header in custom_headers:
			response.headers.add_header(header[0], header[1])

	if cookie != None:
		# print json.dumps(cookie)
		for k,v in cookie.items():
			response.set_cookie(key=COOKIE_NAME+k, value=v)

	if status_code != None:
		response.status_code = status_code

	return response


def getCookie(Operation_str):

	COOKIE ={}
	print request.cookies.keys()
	for name in COOKIE_NAMES:
		if name in request.cookies.keys():

			if name == COOKIE_NAMES[0]:
				COOKIE['author_id'] = request.cookies[name]
			elif name == COOKIE_NAMES[1]:
				COOKIE['session_id'] = request.cookies[name]
			elif name == COOKIE_NAMES[2]:
				COOKIE['github_id'] = request.cookies[name]

	if COOKIE == {}:
		print "WARNING! Cookie not found during %s!"%(Operation_str)
		return getResponse(custom_headers=[("status", "CLIENT_FAILURE")], status_code=400)

	return COOKIE


@app.route("/login", methods=['POST'])
def Login():
	"""	
	Responsible for loggin in user. Creates a session ID and sends back all the information as a cookie.
	Header "status" value meaning:
		1 if no match found
		2 if input data(login_name and password) is larger than specified in Authors schema
	   -1 failure for some other reason

	Example POST BODY after parsing:
		body["login_name"] = "touqir01"
		body["password"] = "123456"

	"""

	# global APP_state

	try:
		data=flask_post_json()

	except Exception as e:
		print "Failed to parse data from POST request during Login! : ", e
		result = {}
		result["status"] = "CLIENT_FAILURE"
		return getResponse(body=result, status_code=400)

	result=userLogin(data)
	if type(result) != dict:
		body = {}
		body["status"] = result 
		return getResponse(body=body, status_code=400)

	else:
		sessionID = uuid.uuid4().hex
		APP_state['session_ids'][sessionID] = result['author_id']
		cookie={}
		cookie["session_id"] = sessionID
		result["status"] = "SUCCESS"
		cookie["github_id"] = result["github_id"]
		cookie["author_id"] = result["author_id"]
		return getResponse(body=result, cookie=cookie, status_code=200)




@app.route("/logout", methods=['GET'])
def Logout():
	"""
	Responsible for logging out user
	Removes the sessionID at this request
	"""
	# global APP_state
	output = getCookie("Logout")
	if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =400 response is send back.
		return output

	cookie = output
	if "session_id" in cookie.keys():
		sessionID = cookie["session_id"]
		if sessionID in APP_state["session_ids"]:
			del APP_state["session_ids"][sessionID]
			result = {}
			result["status"] = "SUCCESS"
			return getResponse(body=result, status_code=200)

		else:
			print "WARNING! Session id not inside server!"
			result = {}
			result["status"] = "INVALID_SESSION_ID"
			return getResponse(body=result, status_code=400)

	else :

		print 'WARNING! "session_id" field is not found inside cookie!'
		result = {}
		result["status"] = "CLIENT_FAILURE"
		return getResponse(body=result, status_code=400)



@app.route("/register", methods=['POST'])
def Register():
	"""
	Responsible for User Registration

	Example POST body after parsing:

		body["login_name"] = "touqir"
		body["name"] = "Touqir Sajed"
		body["password"] = "123456"

	"""
	# global APP_state
	try:
		data=flask_post_json()

	except Exception as e:
		print "Failed to parse data from POST request during registration! : ", e
		return getResponse(custom_headers=[("status", "CLIENT_FAILURE")], status_code=400)

	result = userRegistration(data)

	if type(result) == dict:
		sessionID = uuid.uuid4().hex
		APP_state['session_ids'][sessionID] = result['author_id']
		cookie={}
		cookie["session_id"] = sessionID
		cookie["author_id"] = result["author_id"]
		# cookie["github_id"] = result["github_id"]
		result["status"] = "SUCCESS"
		return getResponse(body=result, cookie = cookie, status_code=200)

	else :
		body={}
		body["status"] = result
		return getResponse(body=body, status_code=400)



# @app.route("/acceptFriendRequest", methods=['POST'])
# def AcceptFriendRequest():
# 	"""
# 	User sends a friend request approval request using this API

# 		Example POST body after parsing:

# 		body["login_name"] = "touqir"
# 		body["name"] = "Touqir Sajed"
# 		body["password"] = "123456"

# 	"""

# 	try:
# 		data=flask_post_json()

# 	except Exception as e:
# 		print "Failed to parse data from POST request during Accepting Friend Request! : ", e
# 		return getResponse(custom_headers=[("status", "CLIENT_FAILURE")], status_code=400)

# 	result = beFriend(data)

# 	if result == True:
# 		return getResponse(custom_headers=[("status", "SUCCESS")], status_code=200)
# 	elif result == False:
# 		return getResponse(custom_headers=[("status", "DB_FAILURE")], status_code=400)
# 	elif result == "DUPLICATE"
# 		return getResponse(custom_headers=[("status", "DUPLICATE")], status_code=400)




@app.route("/editProfile", methods=['POST'])
def EditProfile():
	"""
	User makes modifications to his profile(name, password, etc) and sends them using this API
	"""
	try:
		data=flask_post_json()

	except Exception as e:
		print "Failed to parse data from PUT request during Profile Editing! : ", e
		body = {}
		body['status'] = 'CLIENT_FAILURE'
		return getResponse(body = body, status_code=400)


	output = getCookie("EditProfile")
	if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =400 response is send back.
		return output

	cookie = output
	if "session_id" in cookie.keys():
		sessionID = cookie["session_id"]
		if sessionID in APP_state["session_ids"]:
			userID = APP_state["session_ids"][sessionID]
			data["author"] = userID
			result = updateProfile(data)
			if result == True:
				return getResponse(body={"status" : "SUCCESS"}, status_code=200)
			elif result == "NO_MATCH":
				return getResponse(body={"status" : "NO_MATCH"}, status_code=400)
			elif result == "DB_FAILURE":
				return getResponse(body={"status" : "DB_FAILURE"}, status_code=400)

		else:
			print "WARNING! Session id not inside server!"
			return getResponse(body={"status" : "INVALID_SESSION_ID"}, status_code=400)

	else :

		print 'WARNING! "session_id" field is not found inside cookie!'
		return getResponse(body={"status" : "CLIENT_FAILURE"}, status_code=400)



@app.route("/author/<AUTHOR_ID>", methods=['GET'])
def FetchAuthor(AUTHOR_ID):
	
	param = {}
	print AUTHOR_ID
	param["author"] = AUTHOR_ID
	fetched_author=getAuthor(param)
	if fetched_author == {}:
		return getResponse(body={"status" : "NO_MATCH"}, status_code=400)
	else:
		fetched_author["status"] = "SUCCESS"
		return getResponse(body=fetched_author, status_code=200)


# @app.route("/getFriendRequests", methods=['GET'])
# def GetFriendRequests():
# 	"""
# 	User wants the current list of friend requests that have been sent to him.
# 	"""

# 	output = getCookie("GetFriendRequest")
# 	if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =400 response is send back.
# 		return output

# 	if "session_id" in cookie.keys():
# 		sessionID = cookie["session_id"]
# 		if sessionID in APP_state["session_ids"]:
# 			userID = APP_state["session_ids"][sessionID]
# 			param = {}
# 			param["author"] = userID
# 			param["server_Obj"] = APP_state["server_Obj"]
# 			result = getFriendRequestList(param)

# 			if result == "NO_MATCH":
# 				return getResponse(custom_headers=[("status", "NO_MATCH")], status_code=400)

# 			elif result == True:
# 				return getResponse(body=result, custom_headers=[("status", "SUCCESS")], status_code=200)


# 		else:
# 			print "WARNING! Session id not inside server!"
# 			return getResponse(custom_headers=[("status", "INVALID_SESSION_ID")], status_code=400)

# 	else :

# 		print 'WARNING! "session_id" field is not found inside cookie!'
# 		return getResponse(custom_headers=[("status", "CLIENT_FAILURE")], status_code=400)




# @app.route("/unFriend", methods=['POST'])
# def RemoveFriend():
# 	"""
# 	User wants to unfriend someone
# 	"""

# 	try:
# 		data=flask_post_json()

# 	except Exception as e:
# 		print "Failed to parse data from PUT request during Unfriending! : ", e
# 		return getResponse(custom_headers=[("status", "CLIENT_FAILURE")], status_code=400)

# 	output = getCookie("GetFriendRequest")
# 	if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =400 response is send back.
# 		return output

# 	result = unFriend(data)

# 	if "session_id" in cookie.keys():
# 		sessionID = cookie["session_id"]
# 		if sessionID in APP_state["session_ids"]:
# 			userID = APP_state["session_ids"][sessionID]
# 			param = {}
# 			param["author1"] = userID
# 			param["server_1_address"] = APP_state["server_Obj"].IP
# 			param["author2"] = data["author"]
# 			param["server_2_address"] = data["server_address"]
# 			result = unFriend(param)

# 			if result == "CLIENT_FAILURE":
# 				return getResponse(custom_headers=[("status", result)], status_code=400)

# 			elif result == False :
# 				return getResponse(custom_headers=[("status", "DB_FAILURE")], status_code=400)

# 			elif result == True :
# 				return getResponse(custom_headers=[("status", "SUCCESS")], status_code=200)

# 		else:
# 			print "WARNING! Session id not inside server!"
# 			return getResponse(custom_headers=[("status", "INVALID_SESSION_ID")], status_code=400)

# 	else :

# 		print 'WARNING! "session_id" field is not found inside cookie!'
# 		return getResponse(custom_headers=[("status", "CLIENT_FAILURE")], status_code=400)


# 	pass


# @app.route("/toFollow", methods=['POST'])
# def FollowUser():
# 	"""
# 	User wants to follow someone, aka wants to send a friend request.
# 	TODO:         #################
# 	"""

# 	output = getCookie("FollowUser")
# 	if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =400 response is send back.
# 		return output

# 	try:
# 		data=flask_post_json()

# 	except Exception as e:
# 		print "Failed to parse data from PUT request during sending friend Request! : ", e
# 		return getResponse(custom_headers=[("status", "CLIENT_FAILURE")], status_code=400)


# 	if "session_id" in cookie.keys():
# 		sessionID = cookie["session_id"]
# 		if sessionID in APP_state["session_ids"]:
# 			userID = APP_state["session_ids"][sessionID]

# 		else:
# 			print "WARNING! Session id not inside server!"
# 			return getResponse(custom_headers=[("status", "INVALID_SESSION_ID")], status_code=400)

# 	else :

# 		print 'WARNING! "session_id" field is not found inside cookie!'
# 		return getResponse(custom_headers=[("status", "CLIENT_FAILURE")], status_code=400)






@app.route('/login.html')
@app.route('/')
def login():
    return app.send_static_file('login.html')


@app.route('/index.html')
def start():
    return app.send_static_file('index.html')


@app.route('/profile.html')
def profile():
    return app.send_static_file('profile.html')



def run():
	app.run(debug=True)

if __name__ == "__main__":
	app.run(debug=True)
	# print "HOST IS: ", request.host




