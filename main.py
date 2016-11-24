import flask
from flask import Flask, request, Response, session, render_template, redirect
from flask_restful import reqparse, abort, Api, Resource
# from Server.REST_handlers import REST_handlers
import json
import uuid
from model import *
from Server.author_endpointHandlers import *
import urlparse
from Server.post_comment_handlers import * 
from Server.post_comment_helpers import *
from gevent.wsgi import WSGIServer

#http basic auth
from functools import wraps

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
api = Api(app)

app.config['SECRET_KEY'] = 'hi_this_is_cmput404'

def printSessionIDs(APP_state):
    print APP_state['session_ids']

#this is for server to server basic auth
def check_auth(username, password, forign_server):
    """This function is called to check if a username /
    password combination is valid.
    """

    print "foreign server : "
    print forign_server
    db_server = db.session.query(Servers).filter(Servers.IP == forign_server).all()
    
    if len(db_server) == 0:
        return False
    else:
        print forign_server
        print db_server
        
        return username == db_server.user_name and password == db_server.password

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password, request.environ['REMOTE_ADDR']):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
#this is for server to server basic auth
#-----------------------------------------need @requires_auth

# quick fix for build_in flask

class ModelView(flask_admin.contrib.sqla.ModelView):
    def is_accessible(self):
        auth = request.authorization or request.environ.get('REMOTE_USER')  # workaround for Apache
        
        if not auth or not check_auth(auth.username, auth.password, request.environ['REMOTE_ADDR']):
            raise HTTPException('', Response(
                "Please log in.", 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            ))
    
        return True




#@requires_auth
class UserView(ModelView):
    can_create = True

#@requires_auth
class PostView(ModelView):
    can_create = True

#@requires_auth
class ImageView(ModelView):
    can_create = True

#@requires_auth
class URLView(ModelView):
    can_create = True

#@requires_auth
class ServerView(ModelView):
    can_create = True

#@requires_auth
class GlobalView(ModelView):
    can_create = True

#@requires_auth
class FriendRelationshipsView(ModelView):
    can_create = True

#@requires_auth
class FriendRequestsView(ModelView):
    can_create = True

class Back(BaseView):
    @expose('/')
    def index(self):
        return app.send_static_file('./admin/index.html')



admin = Admin(app, name='Welcome to Admin', template_mode='bootstrap3')

# Add views
admin.add_view(UserView(Authors, db.session))
admin.add_view(PostView(Posts, db.session))
admin.add_view(ImageView(Images, db.session))
admin.add_view(ServerView(Servers, db.session))
admin.add_view(GlobalView(Global_var, db.session))
admin.add_view(FriendRelationshipsView(Author_Relationships, db.session))
admin.add_view(FriendRequestsView(Friend_Requests, db.session))

admin.add_view(Back(name='Back', endpoint='back'))


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


@app.route("/cleanSessions", methods=['GET'])
def cleanSessions():
    APP_state = loadGlobalVar()
    print "from cleanSessions"
    printSessionIDs(APP_state)
    APP_state['session_ids'] = {}
    saveGlobalVar(APP_state)
    return "SUCCESS"

@app.route("/getSessionIds", methods=['GET'])
def getSessionIds():
    APP_state = loadGlobalVar()
    return getResponse(body=APP_state['session_ids'], status_code=200)    

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

    APP_state = loadGlobalVar()

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
        saveGlobalVar(APP_state)
        cookie={}
        cookie["session_id"] = sessionID
        result["status"] = "SUCCESS"
        s=result["github_id"]
        cookie["github_id"] = result["github_id"]
        cookie["author_id"] = result["author_id"]

        print "From Login .."
        printSessionIDs(APP_state)

        return getResponse(body=result, cookie=cookie, status_code=200)





@app.route("/logout", methods=['GET'])
def Logout():
    """
    Responsible for logging out user
    Removes the sessionID at this request
    """
    APP_state = loadGlobalVar()
    output = getCookie("Logout")
    if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
        return output
    print "from logout!"
    printSessionIDs(APP_state)

    cookie = output
    if "session_id" in cookie.keys():
        sessionID = cookie["session_id"]
        if sessionID in APP_state["session_ids"]:
            del APP_state["session_ids"][sessionID]
            saveGlobalVar(APP_state)
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
    try:
        data=flask_post_json()

    except Exception as e:
        print "Failed to parse data from POST request during registration! : ", e
        return getResponse(body={"status" : "CLIENT_FAILURE"}, status_code=200)

    result = userRegistration(data)

    if type(result) == dict:
        result["status"] = "NOT_AUTHORIZED"
        return getResponse(body=result, status_code=200)

    else :
        body={}
        body["status"] = result
        return getResponse(body=body, status_code=200)




@app.route("/editProfile", methods=['POST'])
def EditProfile():
    """
    User makes modifications to his profile(name, password, etc) and sends them using this API
    """
    APP_state = loadGlobalVar()
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
    print "from EditProfile!"
    printSessionIDs(APP_state)

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
#@requires_auth
def FetchAuthor(AUTHOR_ID):
    
    APP_state = loadGlobalVar()
    param = {}
    print "<<<"
    print "Author ID : " + AUTHOR_ID
    print ">>>"
    param["author"] = AUTHOR_ID
    foreign_host = True
    # print list(request.headers.keys())
    if "Foreign-Host" in list(request.headers.keys()):
        foreign_host = request.headers.get("Foreign-Host")
        if foreign_host.strip() == "false":
            foreign_host = False

    fetched_author=getAuthor(param, foreign_host, APP_state)
    if fetched_author == None:
        return getResponse(status_code=200)

    if fetched_author == {}:
        return getResponse(body={"status" : "NO_MATCH"}, status_code=200)
    elif fetched_author != None:
        fetched_author["status"] = "SUCCESS"
        return getResponse(body=fetched_author, status_code=200)



@app.route("/authorByName/", methods=['GET'])
def FetchAuthorByName():

    APP_state = loadGlobalVar()
    first=""
    last=""
    if request.args.has_key("first"):
        first=request.args.get("first")
    if request.args.has_key("last"):
        last=request.args.get("last")
    name = first+' '+last
    param = {}
    param["author_name"] = name
    results = getAuthor(param, False, APP_state)
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
    APP_state = loadGlobalVar()

    output = getCookie("GetFriendRequest")
    if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
        return output

    cookie = output

    print "from GetFriendRequests!"
    printSessionIDs(APP_state)


    if "session_id" in cookie.keys():
        sessionID = cookie["session_id"]
        if sessionID in APP_state["session_ids"]:
            userID = APP_state["session_ids"][sessionID]
            param = {}
            param["author"] = userID
            param["server_Obj"] = APP_state['local_server_Obj']
            result = getFriendRequestList(param, APP_state)

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
    APP_state = loadGlobalVar()

    try:
        data=flask_post_json()

    except Exception as e:
        print "Failed to parse data from POST request during Accepting Friend Request! : ", e
        return getResponse(body={"status" : "CLIENT_FAILURE"}, status_code=200)

    output = getCookie("AcceptFriendRequest")
    if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
        return output

    print "AcceptFriendRequest!"
    printSessionIDs(APP_state)

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
    APP_state = loadGlobalVar()

    try:
        data=flask_post_json()

    except Exception as e:
        print "Failed to parse data from PUT request during Unfriending! : ", e
        return getResponse(body={"status" : "CLIENT_FAILURE"}, status_code=200)

    output = getCookie("GetFriendRequest")
    if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
        return output

    print "from RemoveFriend!"
    printSessionIDs(APP_state)

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
            result = unFriend(param, APP_state)

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
#@requires_auth
def FollowUser():
    """
    User wants to follow someone, aka wants to send a friend request.
    """
    APP_state = loadGlobalVar()

    try:
        data=flask_post_json()

    except Exception as e:
        print "Failed to parse data from PUT request during sending friend Request! : ", e
        return getResponse(body={"status": "CLIENT_FAILURE"}, status_code=200)

    print "from FollowUser!"
    printSessionIDs(APP_state)
    try :
        param={}
        param["from_author"] = data["author"]["id"]
        param["from_author_name"] = data["author"]["displayName"]
        param["from_serverIP"] = data["author"]["host"]
        param["to_author"] = data["friend"]["id"]
        param["to_author_name"] = data["friend"]["displayName"]
        param["to_serverIP"] = data["friend"]["host"]
        
        print data
        result = processFriendRequest(param, APP_state)

        return getResponse(status_code=200)

    except Exception as e:

        return getResponse(status_code=400)

    # if result == True:
    #     return getResponse(body={"status": "SUCCESS"}, status_code=200)
    # else:
    #     return getResponse(body={"status": "DB_FAILURE"}, status_code=200)





@app.route("/friends/<AUTHOR_ID>", methods=['GET'])
#@requires_auth
def GetFriendList(AUTHOR_ID):
    """
    """

    APP_state = loadGlobalVar()

    param = {}
    param["author"] = AUTHOR_ID
    param["local_server_Obj"] = APP_state["local_server_Obj"]
    results=getFriendList(param, APP_state)
    print results
    body = {}
    body["query"] = "friends"
    body["authors"] = [result["id"] for result in results] 
    return getResponse(body=body, status_code=200)



@app.route("/friends/<AUTHOR_ID>", methods=['POST'])
#@requires_auth
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
#@requires_auth
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
    APP_state = loadGlobalVar()
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

    # index = 0
    # for author in APP_state['pending_authors']:
    #     author['webID'] = "element_3_" + str(index)
    #     author['value'] = str(index)
    #     pending_authors.append(author)
    #     index += 1

    return [shared_nodes, shared_nodes_posts, shared_nodes_images]


def init_admin():
    APP_state = loadGlobalVar()

    user1={"login_name":"Amaral", "name":"amaral Dcosta"}
    user2={"login_name":"Tully", "name":"Tully Dcosta"}
    user3={"login_name":"Eddy", "name":"Eddy Dcosta"}
    APP_state["pending_authors"] = [user1, user2, user3]
    APP_state["pending_authors"] += APP_state["pending_authors"] + APP_state["pending_authors"] + APP_state["pending_authors"] + APP_state["pending_authors"] 
    APP_state["shared_nodes"] = ["http://1", "http://2"]
    APP_state["shared_nodes_images"] = ["http://3", "http://4"]
    APP_state["shared_nodes_posts"] = ["http://5", "http://6"]

@app.route('/restart')
def restart():
    # init_admin()
    init_server()
    if init_server() == True:
        return "SUCCESS"
    else:
        return "FAILURE"


def init_server():
    APP_state = loadGlobalVar()
    servers = db.session.query(Servers).filter(Servers.server_index == 0).all()
    server = None
    if len(servers) != 0:
        server = servers[0]
        APP_state['local_server_Obj'] = server
        saveGlobalVar(APP_state)
        return True

    return False


@app.route('/admin_settings.html')
def admin_settings():
    global APP_state
    auth = request.authorization or request.environ.get('REMOTE_USER')  # workaround for Apache
        
    if not auth or [auth.username, auth.password] != APP_state['admin_credentials']:
        raise HTTPException('', Response(
                                         "Please log in.", 401,
                                         {'WWW-Authenticate': 'Basic realm="Login Required"'}
                                         ))
    
    """
        This leads to the admin settings form page
    """
    method_action = APP_state["local_server_Obj"].IP + '/settings'
    [shared_nodes, shared_nodes_posts, shared_nodes_images]=admin_settings_helper()
    checked = None
    if APP_state["nodes_with_authentication"]:
        checked = "checked"


    # print shared_nodes
    return render_template("admin_form.html",
                            users=[],
                            action_endpoint = method_action,
                            shared_nodes = shared_nodes,
                            shared_nodes_images = shared_nodes_images,
                            shared_nodes_posts = shared_nodes_posts,
                            isChecked = checked
                            )


@app.route('/settings', methods=['GET'])
def settings():
    APP_state = loadGlobalVar()
    updateSettings(request.form)
    redirectURL = APP_state["local_server_Obj"].IP + '/admin_settings.html'
    return redirect(redirectURL, code=302)


def updateSettings(dict):

    APP_state = loadGlobalVar()
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

    updateForeignHosts()
    # parseAuthors(dict)


def updateForeignHosts():
    APP_state = loadGlobalVar()
    for host in APP_state["shared_nodes"]:
        servers = db.session.query(Servers).filter(Servers.IP == host).all()
        if len(servers) == 0:
            param = {}
            param["server_id"] = uuid.uuid4().hex
            param["IP"] = host
            param["server_index"] = APP_state["no_servers"]
            APP_state["no_servers"] += 1
            server = Servers(param)
            db.session.add(server)

    db.session.commit()

def parseAuthors(dict):
    APP_state = loadGlobalVar()
    new = []
    indices = []
    for k in dict.keys():
        if k[:10] == "element_3_":
            login_name=APP_state["pending_authors"][int(k[10:])]["login_name"]
            author = db.session.query(Authors).filter(Authors.login_name == login_name).all()[0]
            author.authorized = True
            db.session.commit()
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

@app.route("/secretAuthorization/<AUTHOR_ID>", methods=['GET'])
def authorizeAuthors(AUTHOR_ID):
    author = db.session.query(Authors).filter(Authors.author_id == AUTHOR_ID)[0]
    author.authorized = True
    db.session.commit()


def run():
    app.run(debug=True)


api.add_resource(Post, '/posts/<string:post_id>')
api.add_resource(All_Post, '/posts')
api.add_resource(AuthorPost, '/author/posts')
api.add_resource(AuthorToAuthorPost, '/author/<string:author_id>/posts')
api.add_resource(Comment, '/posts/<string:post_id>/comments')

# for i in range(1, 100):
#     currentTime = datetime.now()
#     post1 = {}
#     post1["post_id"] = i
#     post1["author_id"] = i
#     post1["title"] = "test" + str(i)
#     post1["content"]="TEXT" + str(i)
#     post1["creation_time"]=currentTime 
#     post1["description"] = "abram eat bear"
#     post1["view_permission"]=1
#     post1["content_type"]="text/plain"
#     apost = Posts(post1)
#     db.session.add(apost)
#     db.session.commit()        

# aut = {}
# aut["author_id"] = "98"
# aut["name"] = "Boyuan"
# aaut = Authors(aut)
# db.session.add(aaut)
# db.session.commit()


# com = {}
# com["author_id"] = "110"
# com["post_id"] = "98"
# com["comment_text"] = "nma"
# com["creation_time"] = currentTime
# acomment = Comments(com)
# db.session.add(acomment)
# db.session.commit()

if __name__ == "__main__":
    # init_admin()
    #app.run(debug=True)
    # print "HOST IS: ", request.host
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()





