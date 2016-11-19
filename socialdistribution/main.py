import flask
from flask import Flask, request, Response, session, render_template, redirect
from flask_restful import reqparse, abort, Api, Resource
# from Server.REST_handlers import REST_handlers
import json
import uuid
from model import *
from Server.author_endpointHandlers import *
import urlparse
from Server.cts.pch import * 
from Server.cts.c2sM import *


# admin stuff -----------------------------------
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask.ext.login import current_user

from werkzeug.exceptions import HTTPException
from datetime import timedelta


import os
import os.path as op
from db import db

from wtforms import validators



from flask_admin.contrib import sqla
import flask_admin.contrib.sqla
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


app.config['SECRET_KEY'] = 'hi_this_is_cmput404'


# quick fix for build_in flask
class ModelView(flask_admin.contrib.sqla.ModelView):
    def is_accessible(self):
        auth = request.authorization or request.environ.get('REMOTE_USER')  # workaround for Apache
        
        if not auth or [auth.username, auth.password] != APP_state['admin_credentials']:
            raise HTTPException('', Response(
                "Please log in.", 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            ))
        return True



class UserView(ModelView):
    can_create = True

class PostView(ModelView):
    can_create = True

class ImageView(ModelView):
    can_create = True

class URLView(ModelView):
    can_create = True

class Back(BaseView):
    @expose('/')
    def index(self):
        return app.send_static_file('./admin/index.html')


#@app.route('/admin/')
#@basic_auth.required
# Create admin

admin = Admin(app, name='Example: Admin', template_mode='bootstrap3')

# Add views
admin.add_view(UserView(Authors, db.session))
admin.add_view(PostView(Posts, db.session))
admin.add_view(ImageView(Images, db.session))
admin.add_view(URLView(URL, db.session))

admin.add_view(Back(name='Back', endpoint='back'))



# api = Api(app)
# parser = reqparse.RequestParser()
# api.add_resource(Login, '/login/')
# api.add_resource(Registration, '/register/')



    # parser.add_argument('task')



    # def run(self):

    #     app.run(debug=True)


# class AllPosts(Resource):

#   """
#   Implements functionality regarding URL : http://service/posts  (all posts marked as public on the server)
#   Refer to REST_handlers.py , method : getAllPosts
#   """
#   def get():
#       pass


# class VisiblePosts(Resource):

#   """
#   Implements functionality regarding URL : http://service/author/posts  (posts that are visible to the currently authenticated user)
#   Refer to REST_handlers.py , method : getVisiblePosts
#   """
#   def get():
#       pass


# class VisiblePostsByAuthor(Resource):

#   """
#   Implements functionality regarding URL : http://service/author/{AUTHOR_ID}/posts  (all posts made by {AUTHOR_ID} visible to the currently authenticated user)
#   Refer to REST_handlers.py , method : getVisiblePostsByAuthor
#   """
#   def get():
#       pass



# class Post(Resource):

#   """
#   Implements functionality regarding URL : http://service/posts/{POST_ID}  access to a single post with id = {POST_ID}    
#   Refer to REST_handlers.py , method : getPost
#   """
#   def get():
#       pass



# class Comments(Resource):

#   """
#   Implements functionality regarding URL : http://service/posts/{post_id}/comments    
#   Refer to REST_handlers.py , method : getComments
#   """
#   def get():
#       pass


# # TODO: Refer to method: isFriend.. Have a confusion so I leave it for later.



# class MutuallyFriend(Resource):

#   """
#   Implements functionality regarding URL : http://service/friends/<authorid1>/<authorid2>  Checks whether authorid1 author is friend with authorid2 author.   
#   Refer to REST_handlers.py , method : isBothFriends
#   """
#   def get():
#       pass



# class MultipleFriendship(Resource):

#   """
#   Implements functionality regarding URL : http://service/friends/<authorid>  POSTS a JSON containing lists of authorids and returns with a list containing those IDs
#   Refer to REST_handlers.py , method : areFriends_LIST
#   """
#   def post():
#       pass



# class MakeFriendship(Resource):

#   """
#   Implements functionality regarding URL : http://service/friendrequest  POSTS a JSON containing author info and the to be friended author's info and this sends a friendrequest
#   Refer to REST_handlers.py , method : makeFriendRequest
#   """
#   def post():
#       pass



# class RemoveFriend(Resource):

#   """
#   Implements functionality regarding URL : http://service/unfriend  POSTS a JSON containing author info and to be unfriended author's info and this unfriends.
#   Refer to REST_handlers.py , method : unFriend
#   """
#   def post():
#       pass



# class FetchAuthor(Resource):

#   """
#   Implements functionality regarding URL : http://service/author/<AUTHORID>  Retrieves profile information about AUTHORID author.
#   Refer to REST_handlers.py , method : getAuthor
#   """
#   def post():
#       pass



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
    # print request.cookies.keys()
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
        return getResponse(body={"status" : "CLIENT_FAILURE"}, status_code=200)

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
        return getResponse(body=result, status_code=200)

    result=userLogin(data)
    if type(result) != dict:
        body = {}
        body["status"] = result 
        return getResponse(body=body, status_code=200)

    else:
        sessionID = uuid.uuid4().hex
        APP_state['session_ids'][sessionID] = result['author_id']
        cookie={}
        cookie["session_id"] = sessionID
        result["status"] = "SUCCESS"
        s=result["github_id"]
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
    if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
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
            return getResponse(body=result, status_code=200)

    else :

        print 'WARNING! "session_id" field is not found inside cookie!'
        result = {}
        result["status"] = "CLIENT_FAILURE"
        return getResponse(body=result, status_code=200)



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
        return getResponse(body={"status" : "CLIENT_FAILURE"}, status_code=200)

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
        return getResponse(body=body, status_code=200)




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
        return getResponse(body = body, status_code=200)


    output = getCookie("EditProfile")
    if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
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
                return getResponse(body={"status" : "NO_MATCH"}, status_code=200)
            elif result == "DB_FAILURE":
                return getResponse(body={"status" : "DB_FAILURE"}, status_code=200)

        else:
            print "WARNING! Session id not inside server!"
            return getResponse(body={"status" : "INVALID_SESSION_ID"}, status_code=200)

    else :

        print 'WARNING! "session_id" field is not found inside cookie!'
        return getResponse(body={"status" : "CLIENT_FAILURE"}, status_code=200)



@app.route("/author/<AUTHOR_ID>", methods=['GET'])
def FetchAuthor(AUTHOR_ID):
    
    param = {}
    print AUTHOR_ID
    param["author"] = AUTHOR_ID
    fetched_author=getAuthor(param)
    if fetched_author == {}:
        return getResponse(body={"status" : "NO_MATCH"}, status_code=200)
    else:
        fetched_author["status"] = "SUCCESS"
        return getResponse(body=fetched_author, status_code=200)



@app.route("/authorByName/", methods=['GET'])
def FetchAuthorByName():

    first=""
    last=""
    if request.args.has_key("first"):
        first=request.args.get("first")
    if request.args.has_key("last"):
        last=request.args.get("last")
    name = first+' '+last
    param = {}
    param["author_name"] = name
    results = getAuthor(param)
    if len(results) == 0:
        return getResponse(body={"status" : "NO_MATCH"}, status_code=200)
    else:
        results["status"] = "SUCCESS"
        return getResponse(body=results, status_code=200)


@app.route("/getFriendRequests", methods=['GET'])
def GetFriendRequests():
    """
    User wants the current list of friend requests that have been sent to him.
    """

    output = getCookie("GetFriendRequest")
    if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
        return output

    cookie = output

    if "session_id" in cookie.keys():
        sessionID = cookie["session_id"]
        if sessionID in APP_state["session_ids"]:
            userID = APP_state["session_ids"][sessionID]
            param = {}
            param["author"] = userID
            param["server_Obj"] = APP_state['local_server_Obj']
            result = getFriendRequestList(param)

            if result != None:
                result['status'] = 'SUCCESS'
                return getResponse(body=result, status_code=200)

        else:
            print "WARNING! Session id not inside server!"
            return getResponse(body={"status" : "INVALID_SESSION_ID"}, status_code=200)

    else :

        print 'WARNING! "session_id" field is not found inside cookie!'
        return getResponse(body={"status" : "CLIENT_FAILURE"}, status_code=200)



@app.route("/acceptFriendRequest", methods=['POST'])
def AcceptFriendRequest():
    """
    User sends a friend request approval request using this API


    """

    try:
        data=flask_post_json()

    except Exception as e:
        print "Failed to parse data from POST request during Accepting Friend Request! : ", e
        return getResponse(body={"status" : "CLIENT_FAILURE"}, status_code=200)

    output = getCookie("AcceptFriendRequest")
    if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
        return output

    cookie = output
    if "session_id" in cookie.keys():
        sessionID = cookie["session_id"]
        if sessionID in APP_state["session_ids"]:
            userID = APP_state["session_ids"][sessionID]
            param = {}
            param["author1"] = data["author"] 
            param["author2"] = userID
            param["server_1_address"] = data["server_address"]  
            param["server_2_address"] = APP_state["local_server_Obj"].IP 
            result = beFriend(param)
            
            if result == True:
                return getResponse(body={"status" : "SUCCESS"}, status_code=200)
            elif result == "DUPLICATE":
                return getResponse(body={"status" : "DUPLICATE"}, status_code=200)
            elif result == False:
                return getResponse(body={"status" : "DB_FAILURE"}, status_code=200)

        else:
            print "WARNING! Session id not inside server!"
            return getResponse(body={"status" : "INVALID_SESSION_ID"}, status_code=200)

    else :

        print 'WARNING! "session_id" field is not found inside cookie!'
        return getResponse(body={"status" : "CLIENT_FAILURE"}, status_code=200)



@app.route("/unFriend", methods=['POST'])
def RemoveFriend():
    """
    User wants to unfriend someone
    """

    try:
        data=flask_post_json()

    except Exception as e:
        print "Failed to parse data from PUT request during Unfriending! : ", e
        return getResponse(body={"status" : "CLIENT_FAILURE"}, status_code=200)

    output = getCookie("GetFriendRequest")
    if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
        return output

    cookie = output
    if "session_id" in cookie.keys():
        sessionID = cookie["session_id"]
        if sessionID in APP_state["session_ids"]:
            userID = APP_state["session_ids"][sessionID]
            param = {}
            param["author1"] = userID
            param["server_1_address"] = APP_state['local_server_Obj'].IP
            param["author2"] = data["author"]
            param["server_2_address"] = data["server_address"]
            result = unFriend(param)

            if result == False :
                return getResponse(body={"status" : "DB_FAILURE"}, status_code=200)

            else :
                return getResponse(body={"status" : "SUCCESS"}, status_code=200)

        else:
            print "WARNING! Session id not inside server!"
            return getResponse(body={"status" : "INVALID_SESSION_ID"}, status_code=200)

    else :

        print 'WARNING! "session_id" field is not found inside cookie!'
        return getResponse(body={"status" : "CLIENT_FAILURE"}, status_code=200)



@app.route("/friendrequest", methods=['POST'])
def FollowUser():
    """
    User wants to follow someone, aka wants to send a friend request.
    """

    output = getCookie("FollowUser")
    if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
        return output

    try:
        data=flask_post_json()

    except Exception as e:
        print "Failed to parse data from PUT request during sending friend Request! : ", e
        return getResponse(body={"status": "CLIENT_FAILURE"}, status_code=200)

    cookie = output
    if "session_id" in cookie.keys():
        sessionID = cookie["session_id"]
        if sessionID in APP_state["session_ids"]:
            userID = APP_state["session_ids"][sessionID]
            param={}
            param["from_author"] = userID
            param["from_author_name"] = data["author"]["displayName"]
            param["from_serverIP"] = data["author"]["host"]
            param["to_author"] = data["friend"]["id"]
            param["to_author_name"] = data["friend"]["displayName"]
            param["to_serverIP"] = data["friend"]["host"]
            
            result = processFriendRequest(param)

            if result == True:
                return getResponse(body={"status": "SUCCESS"}, status_code=200)
            else:
                return getResponse(body={"status": "DB_FAILURE"}, status_code=200)


        else:
            print "WARNING! Session id not inside server!"
            return getResponse(body={"status" : "INVALID_SESSION_ID"}, status_code=200)

    else :

        print 'WARNING! "session_id" field is not found inside cookie!'
        return getResponse(body={"status" : "CLIENT_FAILURE"}, status_code=200)



@app.route("/friends/<AUTHOR_ID>", methods=['GET'])
def GetFriendList(AUTHOR_ID):
    """
    """

    param = {}
    param["author"] = AUTHOR_ID
    param["local_server_Obj"] = APP_state["local_server_Obj"]
    results=getFriendList(param)
    print results
    body = {}
    body["query"] = "friends"
    body["authors"] = [result["id"] for result in results] 
    return getResponse(body=body, status_code=200)



@app.route("/friends/<AUTHOR_ID>", methods=['POST'])
def checkIfFriendsList(AUTHOR_ID):
    """
    """
    try:
        data=flask_post_json()

    except Exception as e:
        print "Failed to parse data from PUT request during sending friend Request! : ", e
        return getResponse(body={}, status_code=200)

    param = {}
    param['author'] = AUTHOR_ID
    print type(data)
    param['authorsForQuery'] = data["authors"]
    results = areFriends_LIST(param)

    body = {}
    body['query'] = 'friends'
    body['author'] = AUTHOR_ID
    body['authors'] = results

    return getResponse(body=body, status_code=200)



@app.route("/friends/<AUTHOR_ID_1>/<AUTHOR_ID_2>", methods=['GET'])
def checkIfFriends(AUTHOR_ID_1, AUTHOR_ID_2):
    """
    """
    param={}
    param["author1"] = AUTHOR_ID_1
    param["author2"] = AUTHOR_ID_2
    results=isFriend(param)
    # print results
    body = {}
    body["query"] = "friends"
    body['authors'] = [AUTHOR_ID_1, AUTHOR_ID_2]
    if results == True:
        body["friends"] = True
    else:
        body["friends"] = False

    return getResponse(body=body, status_code=200)




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

def admin_settings_helper():
    shared_nodes = ""
    shared_nodes_posts = ""
    shared_nodes_images = ""
    pending_authors = []

    for node in APP_state["shared_nodes"]:
        shared_nodes = shared_nodes + '[' + node + ']'

    for node in APP_state["shared_nodes_posts"]:
        shared_nodes_posts = shared_nodes_posts + '[' + node + ']'

    for node in APP_state["shared_nodes_images"]:
        shared_nodes_images = shared_nodes_images + '[' + node + ']'

    index = 0
    for author in APP_state['pending_authors']:
        author['webID'] = "element_3_" + str(index)
        author['value'] = str(index)
        pending_authors.append(author)
        index += 1

    return [pending_authors, shared_nodes, shared_nodes_posts, shared_nodes_images]


def init_admin():
    user1={"login_name":"Amaral", "name":"amaral Dcosta"}
    user2={"login_name":"Tully", "name":"Tully Dcosta"}
    user3={"login_name":"Eddy", "name":"Eddy Dcosta"}
    APP_state["pending_authors"] = [user1, user2, user3]
    APP_state["pending_authors"] += APP_state["pending_authors"] + APP_state["pending_authors"] + APP_state["pending_authors"] + APP_state["pending_authors"] 
    APP_state["shared_nodes"] = ["http://1", "http://2"]
    APP_state["shared_nodes_images"] = ["http://3", "http://4"]
    APP_state["shared_nodes_posts"] = ["http://5", "http://6"]

@app.route('/restart.html')
def restart():
    init_admin()
    return ""

@app.route('/admin_settings.html')
def admin_settings():
    """
        This leads to the admin settings form page
    """
    method_action = APP_state["local_server_Obj"].IP + '/settings'
    [pending_authors, shared_nodes, shared_nodes_posts, shared_nodes_images]=admin_settings_helper()
    checked = None
    if APP_state["nodes_with_authentication"]:
        checked = "checked"


    # print shared_nodes
    return render_template("admin_form.html",
                            users=pending_authors,
                            action_endpoint = method_action,
                            shared_nodes = shared_nodes,
                            shared_nodes_images = shared_nodes_images,
                            shared_nodes_posts = shared_nodes_posts,
                            isChecked = checked
                            )


@app.route('/settings', methods=['POST'])
def settings():
    updateSettings(request.form)
    redirectURL = APP_state["local_server_Obj"].IP + '/admin_settings.html'
    return redirect(redirectURL, code=302)


def updateSettings(dict):

    print dict
    if 'element_6' in dict:
        if dict['element_6'].strip() == "":
            APP_state["shared_nodes"] = []
        else:
            APP_state["shared_nodes"] = parseHosts(dict['element_6'])
    else:
        APP_state["shared_nodes"] = []

    if "element_7_1" in dict:
        APP_state["nodes_with_authentication"] = True
    else:
        APP_state["nodes_with_authentication"] = False

    if "element_1" in dict:
        if dict['element_1'].strip() == "":
            APP_state["shared_nodes_posts"] = []
        else:
            APP_state["shared_nodes_posts"] = parseHosts(dict['element_1'])
    else:
        APP_state["shared_nodes_posts"] = []

    if "element_2" in dict:
        if dict['element_2'].strip() == "":
            APP_state["shared_nodes_images"] = []
        else:
            APP_state["shared_nodes_images"] = parseHosts(dict['element_2'])
    else:
        APP_state["shared_nodes_images"] = []

    parseAuthors(dict)


def parseAuthors(dict):

    new = []
    indices = []
    for k in dict.keys():
        if k[:10] == "element_3_":
            APP_state["pending_authors"][int(k[10:])] = None

    for i in APP_state["pending_authors"]:
        if i != None:
            new.append(i)

    APP_state["pending_authors"] = new


def parseHosts(host_text):

    result=[]
    splitted = host_text.split('][')
    if len(splitted) > 1:
        splitted[0] = splitted[0].strip()[1:]
        for split in splitted:
            result.append(split)

        result[-1] = splitted[-1].strip()[0:-1]

    if len(splitted) == 1:
        result.append(splitted[0].strip()[1:-1])

    return result


def run():
    app.run(debug=True)

if __name__ == "__main__":
    init_admin()
    app.run(debug=True)
    # print "HOST IS: ", request.host






