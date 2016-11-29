import flask
import json
from flask import Flask, jsonify, request, Response
import requests
from flask_restful import Resource, Api, abort, reqparse
from model import *
from post_comment_handlers import *
import random, os
from model import *
from werkzeug.exceptions import HTTPException


from Nodes import *
from functools import wraps
from author_endpointHandlers import *
from requests.auth import HTTPBasicAuth
from datetime import datetime
import time
import uuid

random.seed(time.time())


handler = RestHandlers()
COOKIE_NAME = "cookie_cmput404_"
COOKIE_NAMES = ["cookie_cmput404_author_id", "cookie_cmput404_session_id", "cookie_cmput404_github_id"]
VIEW_PER = ["", "PUBLIC", "PRIVATE", "FRIENDS", "FOAF", "SERVERONLY"]


APP_state = loadGlobalVar()
if 'local_server_Obj' in APP_state.keys():
    myip = APP_state['local_server_Obj'].IP
else:
    myip = None
del APP_state



#this is for server to server basic auth
def check_auth(username, password):
    """This function is called to check if a username /
        password combination is valid.
        """
    
    
    # print "This is an example wsgi app served from {} to {}".format(socket.gethostname(), request.url_root)
    # print username
    # print password
    # print "foreign server : "
    # print forign_server
    # forign_server = forign_server[:-1]
    db_server_list = db.session.query(Servers).filter(Servers.user_name == username).all()
    
    if len(db_server_list) == 0:
        return False
    else:
        
        db_server = db_server_list[0]
        # print forign_server
        # print db_server
        
        return username == db_server.user_name and password == db_server.password

#def authenticate():
#    """Sends a 401 response that enables basic auth"""
#    return Response(
#                    'Could not verify your access level for that URL.\n'
#                    'You have to login with proper credentials', 401,
#                    {'WWW-Authenticate': 'Basic realm="Login Required"'})
#
#def requires_auth(f):
#    @wraps(f)
#    def decorated(*args, **kwargs):
#        auth = request.authorization
#        print "this is auth for server____: "
#        print request.headers.get("Origin")
#        if not auth or not check_auth(auth.username, auth.password):
#            return authenticate()
#        return f(*args, **kwargs)
#    return decorated
##this is for server to server basic auth
##-----------------------------------------need @requires_auth
#
#






##this is for server to server basic auth
#def check_auth(username, password, forign_server):
#    """This function is called to check if a username /
#        password combination is valid.
#        """
#    
#    
#    # print "This is an example wsgi app served from {} to {}".format(socket.gethostname(), request.url_root)
#    # print username
#    # print password
#    # print "foreign server : "
#    # print forign_server
#    # forign_server = forign_server[:-1]
#    db_server_list = db.session.query(Servers).filter(Servers.IP == forign_server).all()
#    
#    if len(db_server_list) == 0:
#        return False
#    else:
#        
#        db_server = db_server_list[0]
#        # print forign_server
#        # print db_server
#        
#        return username == db_server.user_name and password == db_server.password
#
##this is for server to server basic auth
##-----------------------------------------need @requires_auth



def is_accessible():
    auth = request.authorization or request.environ.get('REMOTE_USER')  # workaround for Apache
    
    if not auth or not check_auth(auth.username, auth.password):
        raise HTTPException('', Response('NO AUTHENTICATION', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}))
    
    return True


#
##the is for server to server basic auth
#def check_auth_post(username, password):
#    """This function is called to check if a username /
#        password combination is valid.
#        """
#    return username == 'servertoserver' and password == '654321'
#
#def authenticate_post():
#    """Sends a 401 response that enables basic auth"""
#    return Response(
#                    'Could not verify your access level for that URL.\n'
#                    'You have to login with proper credentials', 401,
#                    {'WWW-Authenticate': 'Basic realm="Login Required"'})
#
#def requires_auth_post(f):
#    @wraps(f)
#    def decorated(*args, **kwargs):
#        auth = request.authorization
#        if not auth or not check_auth_post(auth.username, auth.password):
#            return authenticate_post()
#        return f(*args, **kwargs)
#    return decorated
##the is for server to server basic auth
##-----------------------------------------need @requires_auth




def makeAuthorJson(author):
    rt = {
        "id"    :   author.author_id,
        "host"  :   myip,
        "displayName"   :   author.name,
        "url"   :   myip +"author/" + author.author_id,
        "github"    :   author.github_id
    }
    return rt


def makeCommentJson(data, args):
   #Init
    rt = {
            "query" :   "comments",
            "count" :   len(data),
            "size"  :   5,
            "comments"  :   []
         }

    if(args["size"]):
        rt["size"] = int(args["size"])
    pg = 0
    if args["page"]:
        pg = int(args["page"])
    if pg>0:
        rt["previous"] = myip + "posts/" + data[0].post_id + "comments?page=" + str(pg-1)
    if (pg+1)*rt["size"] < rt["count"]:
        rt["next"] = myip + "posts/" + data[0].post_id + "/comments?page=" + str(pg+1)

    #comments
    if pg*rt["size"] < rt["count"]:
        for i in range(pg*rt["size"], (pg+1)*rt["size"]):
            if i == rt["count"]:
                break
            rt["comments"].append({
                "author"    :   {
                                    "id"    :   data[i].author_id,
                                    "host"  :   data[i].author_host,
                                    "displayName"   :   data[i].author_name,
                                    "url"   :   data[i].author_url,
                                    "github"    :   data[i].author_github
                                },
                "comment"   :   data[i].comment_text,
                "contentType"   :   data[i].content_type,
                "published" :   data[i].creation_time.isoformat(),
                "id"    : data[i].comment_id
            })

    return rt



def makePostJson(data, args):
    #Init
    rt = {
            "query" :   "posts",
            "count" :   len(data),
            "size"  :   5,
            "posts" :   []
         }

    if(args["size"]):
        rt["size"] = int(args["size"])
    pg = 0
    if args["page"]:
        pg = int(args["page"])
    if pg>0:
        rt["previous"] = myip + "posts?page=" + str(pg-1)
    if (pg+1)*rt["size"] < rt["count"]:
        rt["next"] = myip + "posts?page=" + str(pg+1)

    #Posts
    if pg*rt["size"] < rt["count"]:
        for i in range(pg*rt["size"], (pg+1)*rt["size"]):
            if i == rt["count"]:
                break
            rt["posts"].append({
                "title" :   data[i][0].title,
                "source"    :   myip + "posts/" + data[i][0].post_id,
                "origin"    :   myip + "posts/" + data[i][0].post_id,
                "author"    :   makeAuthorJson(data[i][1]),
                "description"   :   data[i][0].description,
                "contentType"   :   data[i][0].content_type,
                "content"   :   data[i][0].content,
                "categories"    :   "abram bear",
                "published" :   data[i][0].creation_time.isoformat(),
                "visibility"    :   VIEW_PER[data[i][0].view_permission],
                "id"    :   data[i][0].post_id,
                "image-url"	: handler.getImgUrl(data[i][0].post_id),
                "count" :   len(data[i][2]),
                "size"  :   5,
                "next"  :   myip + "posts/"+data[i][0].post_id+"/comments",
                "comments"  :   makeCommentJson(data[i][2], {"size":None, "page":None})["comments"]
            })

    return rt


def getCookie(Operation_str):
    COOKIE ={}
    print request.cookies.keys()

    for name in COOKIE_NAMES:
        if name in request.cookies:
            if name == COOKIE_NAMES[0]:
                COOKIE['author_id'] = request.cookies[name]
            elif name == COOKIE_NAMES[1]:
                COOKIE['session_id'] = request.cookies[name]
            elif name == COOKIE_NAMES[2]:
                COOKIE['github_id'] = request.cookies[name]

    if COOKIE == {}:
        print "WARNING! Cookie not found during %s!"%(Operation_str)
        return "status : CLIENT_FAILURE", 200

    return COOKIE



class Post(Resource):
#    @requires_auth
    def get(self, post_id):
        
        if is_accessible():
            APP_state = loadGlobalVar()
            #Local Request
            
            json_return = {}
            json_return["count"] = 0
            json_return["size"] = 0
            json_return["query"] = "posts"
            json_return["posts"] = []
            
            if "Foreign-Host" in request.headers.keys():
            
                if(request.headers.get("Foreign-Host") == "false"):
                
    #            output = getCookie("get_one_post")
    #            if type(output) == flask.wrappers.Response:
    #                return output
    #
    #            cookie = output
    #            if "session_id" in cookie:
    #                sessionID = cookie["session_id"]
    #                #print sessionID
    #                if sessionID in APP_state["session_ids"]:
    #                    rst = []
    #                    got = handler.getPost(post_id)
                        #if len(got) != 0:
                            #This post is in our server
                            #if got[0] in handler.getVisiblePosts(APP_state["session_ids"][sessionID]):
                                #if the user has permission to see it
                                #rst = got
                            # else:
                                #No permission
                        #else:
                            #The post is in other server?
                    nodes = handler.getConnectedNodes()
                    params = {}

    #                params["author_id"] = APP_state["session_ids"][sessionID]
    #                params["post_id"] = post_id
                    pid = request.args.get("post_id")
                    
                    print "checking OWN POST"
                    print post_id
                    print db.session.query(Posts).filter(Posts.post_id == post_id).first().author_id
                    print "checking OWN POST_end"
                    
                    own_post = handler.getPost(post_id)
                    
                    if len(own_post) > 0:
                    
                        own_post_return = makePostJson([own_post], {"page":None, "size":None})
                        
                        
                        json_return["posts"].extend(own_post_return["posts"])
                        return jsonify(json_return)
                    else:
                        for node in nodes:
                            
                            
                            print "Im searching posts in the server with address" + node
                            headers = createAuthHeaders(node)
                            headers['Content-type'] = 'application/json'
                            [prefix, suffix] = getAPI(node, 'GET/posts/P')
                            custom_url = prefix + post_id + suffix

                            
                            foreign_return = requests.get(custom_url, headers = headers)
                            
                            if foreign_return.status_code == 200:
                                recvJson = foreign_return.json()
                                json_return["posts"].extend(recvJson["posts"])

                                
                            json_return["posts"].extend(foreign_return["posts"])
                                #rst += requests.get(custom_url, auth = HTTPBasicAuth(node_user_name,node_user_pass), headers = headers).json()
                                    
                        #                        if  len(rst) != 0:
                        #                            return rst[0]

                        #                    paras = {}
                        #                    paras["page"] = request.args.get('page')
                        #                    paras["size"] = request.args.get('size')
                        return jsonify(json_return)
    #
    #                else:
    #                    return {"Response" : "sessionID error"}
    #            else:
    #                return {"Response" : "Session not found"}

            #Remote Request
            else:
                
                pid = request.args.get("post_id")
                
                paras = {}
                
                paras["page"] = request.args.get('page')
                paras["size"] = request.args.get('size')
                print "SERVERTOSERVER response"
                
                
                return jsonify(makePostJson([handler.getPost(post_id)], {"page":None, "size":None}))
                
    #        #Assume we passed server to server auth
    #        #Assume this is the place we do remote get
    #            pid = request.args.get("post_id")
    #            remoteAuthor = request.args.get("author_id")
    #            got = handler.getPost(pid)
    #
    #            if len(got) != 0:
    #                localAuthor = got[0][1].author_id
    #                if  got[0] in handler.getVisiblePosts(remoteAuthor):
    #                    return jsonify(makePostJson(got), {"page":None, "size":None})
    #                else:
    #                    if got[0][0].view_permission == 4:
    #                        pfriends = requests.get(request.remote_addr + "/friends/" + remoteAuthor).json()["authors"]
    #                        if(handler.atlOneFriend(localAuthor, pfriends)):
    #                            return jsonify(makePostJson(got), {"page":None, "size":None})
    #                        # else:
    #                            #No permission coz the requesting remote user is not foaf of the post author in my server
    #                    # else:
    #                        #No permission coz either this post is private or serveronly
    #            # else:
    #                #Post Not in my server

        else:
            return "NO AUTHENTICATION", 401
#    @requires_auth
    def delete(self, post_id):
        if is_accessible():
            APP_state = loadGlobalVar()
            output = getCookie("delete_post")
            if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code = 200 response is send back.
                return output

            cookie = output
            if "session_id" in cookie:
                sessionID = cookie["session_id"]
                if sessionID in APP_state["session_ids"]:

                    if handler.delete_post(post_id):
                        return {"Response"  : "deletion OK!"}, 200
                else:
                    return "SessionID ERROR", 403
            else:
                return "SESSION_ERROR", 403
        else:
            return "NO AUTHENTICATION", 401


# DONE - own server to server- working with one other server ------------------------------------
class All_Post(Resource):
#    @requires_auth
    def get(self):
        if is_accessible():

            #Local Request
            print request.headers.get("Foreign-Host")
            
            if "Foreign-Host" in request.headers.keys():
                
                if(request.headers.get("Foreign-Host") == "false"):
                    paras = {}
                    paras["page"] = request.args.get('page')
                    paras["size"] = request.args.get('size')
                    nodes = handler.getConnectedNodes()
                    print nodes
                    print "SERVERtoclient response"
                    json_return = {}
                    json_return["count"] = 0
                    json_return["size"] = 0
                    json_return["query"] = "posts"
                    json_return["posts"] = []
                    
                    json_return["posts"].extend(makePostJson(handler.getAllPosts(), paras)["posts"])
                    
                    #agre.append(makePostJson(handler.getAllPosts(), paras))
                    for node in nodes: 
                        print "Im searching posts in the server with address" + node
                        headers = createAuthHeaders(node)
                        headers['Content-type'] = 'application/json'
                        node_user = db.session.query(Servers).filter(Servers.IP == node).first()
                        node_user_name = node_user.user_name
                        node_user_pass = node_user.password
                        
                        [prefix, suffix] = getAPI(node, 'GET/posts')
                        custom_url = prefix + suffix
                        
                        
                        if request.args.get('page') == 0 and request.args.get('size') == 0:
                            foreign_return = requests.get(custom_url, headers = headers)
                        else:
                            foreign_return = requests.get(custom_url, headers = headers)
                        #auth = HTTPBasicAuth(node_user_name,node_user_pass),
                        
                        print foreign_return
                        print node_user_pass
                        print node_user_name
                        if foreign_return.status_code == 200:
                            recvJson = foreign_return.json()
                            
                            json_return["posts"].extend(recvJson["posts"])
                    
                    # Each json object contains all public posts from a server
                    
                    return jsonify(json_return)

            #Remote
            else:
            #Assume we passed server to server auth
            #Assume this is the place we respond to remote get
                paras = {}
                paras["page"] = request.args.get('page')
                paras["size"] = request.args.get('size')
                print "SERVERTOSERVER response"
                
                return jsonify(makePostJson(handler.getAllPosts(), paras))

        else:
            return "NO AUTHENTICATION", 401
#----------------------------------------------------------------------------------------------------
#    @requires_auth
    def post(self):
        if is_accessible():

            APP_state = loadGlobalVar()
            output = getCookie("post_post")
            if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code = 200 response is send back.
                return output

            cookie = output
            if "session_id" in cookie:
                sessionID = cookie["session_id"]

                if sessionID in APP_state["session_ids"]:

                    data = request.get_json(force=True)
                    post = {}
                    print data
                    post["author_id"] = data["author_id"]
                    post["title"] = data["title"]
                    post["content"] = data["content"]
                    print "The data we of the post json is: "
                    print data
                    print "End"
                                     
                    if data["description"] == None:
                        post["description"] = ""
                    else:
                        post["description"] = data["description"]
                    
                    post["content_type"] = data["contentType"]
                    
                    perm = data["visibility"]
                    if perm =="PUBLIC":
                        perm = 1
                    elif perm =="PRIVATE":
                        perm = 2
                    elif perm == "FRIEND":
                        perm = 3
                    elif perm == "FOAF":
                        perm = 4
                    else:
                        perm = 5
                    post["view_permission"]= perm

                    if("image" in data):                       
                        url = saveImage(data["image"], data["image-ext"])
                        post["img-url"] = url
                        
                    if handler.make_post(post):
                        return {"query" : "addPost", "success" : "true", "message" : "Post Added"}
                    else:
                        return {"query" : "addPost", "success" : "false", "message" : "Post not allowed"}

                else:
                    return "Invalid Session ID", 403
            else:
                return "No Session", 403

        else:
            return "NO AUTHENTICATION", 401



class AuthorPost(Resource):
#    @requires_auth
    def get(self):
        if is_accessible():

            APP_state = loadGlobalVar()
            
        
            json_return = {}
            json_return["count"] = 0
            json_return["size"] = 0
            json_return["query"] = "posts"
            json_return["posts"] = []
        
            if "Foreign-Host" in request.headers.keys():
                if  request.headers.get("Foreign-Host") == "false":
                    output = getCookie("get_available_posts")
                    if type(output) == flask.wrappers.Response:
                        return output
                    cookie = output
                    print "this is COOKIE: "
                    print cookie
                    if "session_id" in cookie:
                        sessionID = cookie["session_id"]
                        print sessionID
                        print "SESSIONID in appstate: "
                        print APP_state["session_ids"]
                        
                        if sessionID in APP_state["session_ids"]:
                            paras = {}
                            #rt = []
                            paras["page"] = request.args.get('page')
                            paras["size"] = request.args.get('size')
                            #rt.append(jsonify
                            
                            own_returns = makePostJson(handler.getVisiblePosts(APP_state["session_ids"][sessionID]), paras)
                            
                            
                            nodes = handler.getConnectedNodes()

                            paras["author_id"] = APP_state["session_ids"][sessionID]

                            for node in nodes:

                                headers = createAuthHeaders(node)
                                
                                headers['Content-type'] = 'application/json'
                                headers['author_id'] = APP_state["session_ids"][sessionID]
                                
                                [prefix, suffix] = getAPI(node, 'GET/author/posts')
                                custom_url = prefix + suffix
                                
                                foreign_return = requests.get(custom_url, headers=headers)
                
                
                                if foreign_return.status_code == 200:
                                    recvJson = foreign_return.json()
                                    
                                    own_returns["posts"].extend(recvJson["posts"])

                            print
                            return jsonify(own_returns)
                        else:
                            return "Session_ID Error", 403

                    else:
                        return "SESSION_ERROR", 403
                
            else:
                #Remote
                remoteUsr = request.headers.get("author_id")
                allPosts = handler.getVisiblePosts(remoteUsr)
                
                auth = db.session.query(Servers).filter(Servers.user_name == request.authorization.username).first().IP
                
                
                
                
                headers = createAuthHeaders(auth)

                headers['Content-type'] = 'application/json'
                
                [prefix, suffix] = getAPI(auth, 'GET/friends/A')
                custom_url = prefix + remoteUsr + suffix
                print "friend request url: "
                print custom_url

                pfriends = requests.get(custom_url, headers=headers).json()["authors"]
                #Get all remaining foaf posts, check for each one, if the author is a friend of at least one usr in pfriends
                foafPosts = handler.getAllFoafPosts()

                for post in foafPosts:
                    if  atlOneFriend(post.author_id, pfriends):
                        allPost.append(post)

                paras = {}
                paras["page"] = request.args.get('page')
                paras["size"] = request.args.get('size')

                return jsonify(makePostJson(allPosts, paras))
        else:
            return "NO AUTHENTICATION", 401


# gets all post made by AUTHOR_ID for current author to view.
class AuthorToAuthorPost(Resource):
#    @requires_auth
    #--------------new code--------------
    def get(self, author_id):
        
        if is_accessible():

            APP_state = loadGlobalVar()
            if "Foreign-Host" in request.headers.keys():
                if  request.headers.get("Foreign-Host") == "false":
                    output = getCookie("view_author_id_post")
                    if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
                        return output

                    cookie = output
                    print "cookie out dude: "
                    print cookie
                    if "session_id" in cookie:
                        sessionID = cookie["session_id"]
                        if sessionID in APP_state["session_ids"]:
                            paras = {}
                            paras["page"] = request.args.get('page')
                            paras["size"] = request.args.get('size')
                            print "I AM HERE 1"
                            print author_id
                            print handler.getAllUsers()
                            
                            if author_id in handler.getAllUsers():
                                print "I AM HERE 2"
                                own_post = makePostJson(handler.getVisiblePostsByAuthor(APP_state["session_ids"][sessionID], author_id), paras)
                                
                                print own_post
                                return jsonify(own_post)
                            
                            else:
                                print "I AM HERE 3"
                                nodes = handler.getConnectedNodes()
                                for node in nodes:
                                    headers = createAuthHeaders(node)


                                    headers['Content-type'] = 'application/json'
                                    headers['author_id'] = APP_state["session_ids"][sessionID]

                          
                                    [prefix, suffix] = getAPI(node, 'GET/author/A/posts')
                                    custom_url = prefix + author_id +suffix
    #                                foreign_return = requests.get(custom_url,auth = HTTPBasicAuth(node_user_name,node_user_pass),headers=headers)
                                    print "I AM HERE 4 "
                                    print node
                                    print author_id
                                    
                                    foreign_return = requests.get(custom_url, headers = headers)
                                    
                                    print foreign_return
                                    print foreign_return.json() # this return none
                                    
                                    
    #                                if foreign_return.status_code == 200:
    #                                    recvJson = foreign_return.json()
    #                                    if recvJson["size"] == 0:
    #                                        pass
    #                                    else:
    #                                        return jsonify(recvJson)
                                    if foreign_return.status_code == 200:
                                        if foreign_return.json() == None:
                                            pass
                                        else:
                                            recvJson = foreign_return.json()
                                            return jsonify(recvJson)

    #
    #                               if rt["count"] > 0:
    #                                   return rt
                                #No such author in any of the connecting servers
                        else:
                            return "SESSION_ID_ERROR", 403

                    else:
                        return "SESSION_ERROR", 403
            else:
            #Remote
                if author_id in handler.getAllUsers():
                    remoteUsr = request.headers.get("author_id")
                    allPosts = handler.getVisiblePostsByAuthor(remoteUsr, author_id)
                    foafPosts = handler.getAllFoafPostsByUsr(author_id)
                    
                    auth = db.session.query(Servers).filter(Servers.user_name == request.authorization.username).first().IP
                    
                    headers = createAuthHeaders(auth)

                    headers['Content-type'] = 'application/json'
                    
                    [prefix, suffix] = getAPI(auth, 'GET/friends/A')
                    custom_url = prefix + remoteUsr + suffix
                    print "friend request url: "
                    print custom_url

                    pfriends = requests.get(custom_url, headers=headers).json()["authors"]
                    for author in pfriends:
                        if(handler.isFriend(author, author_id)):
                            allPosts += foafPosts
                            break

                    paras = {}
                    paras["page"] = request.args.get('page')
                    paras["size"] = request.args.get('size')

                    return jsonify(makePostJson(allPosts, paras))
                    
                # else:
                    #We don't have this requested user in our server
        else:
            return "NO AUTHENTICATION", 401

class Comment(Resource):
#    @requires_auth
    def get(self, post_id):
        if is_accessible():

            APP_state = loadGlobalVar()
            
            return_comment = {}
            
            if "Foreign-Host" in request.headers.keys():
            
                if  request.headers.get("Foreign-Host") == "false":
                    output = getCookie("get_comments")
                    if type(output) == flask.wrappers.Response:
                        return output

                    cookie = output
                    if "session_id" in cookie:
                        sessionID = cookie["session_id"]
                        #print sessionID
                        if sessionID in APP_state["session_ids"]:
                            paras = {}
                            paras["page"] = request.args.get('page')
                            paras["size"] = request.args.get('size')
                            
                            if  handler.getPost(post_id):
                                return jsonify(makeCommentJson(handler.getComments(post_id), paras))
                            else:
                                #The post is in other server?
                                nodes = handler.getConnectedNodes()
                                paras["author_id"] = APP_state["session_ids"][sessionID]
                                paras["post_id"] = post_id
                                for node in nodes:

                                    headers = createAuthHeaders(node)
                                    headers['Content-type'] = 'application/json'
                                    [prefix, suffix] = getAPI(node, 'GET/posts/P/comments')
                                    custom_url = prefix + post_id + suffix


                                    foreign_return = requests.get(custom_url, headers = headers)
                                        
                                    if foreign_return.status_code == 200:
                                        
                                        if foreign_return.json() == None:
                                            pass
                                        
                                        else:
                                        
                                            return jsonify(foreign_return)
    #                                rst += requests.get(node + "/posts/" + post_id + "/comments", paras = paras).json()
    #                            if  len(rst) != 0:
    #                                return rst[0]

                            return jsonify(makeCommentJson([], paras))
                               

                        return {"Response"	: "SESSION_ID_ERROR"}, 403

                    else:
                        return {"Response"	:  "SESSION_ERROR"}, 403

            else:
            #Remote
            #Assume we passed server to server auth
            #Assume this is the place we do remote get
#                pid = request.args.get("post_id")
                remoteAuthor = request.headers.get("author_id")
                pg = request.args.get("page")
                sz = request.args.get("size")
                
                got = handler.getPost(post_id)

                if len(got) != 0:
                    localAuthor = got[0][1].author_id
                    if  got[0] in handler.getVisiblePosts(remoteAuthor):
                        return jsonify(makeCommentJson(got[0][2]), {"page":pg, "size":sz})
                    else:
                        if got[0][0].view_permission == 4:
                            
                            auth = db.session.query(Servers).filter(Servers.user_name == request.authorization.username).first().IP
                            
                            headers = createAuthHeaders(auth)

                            headers['Content-type'] = 'application/json'

                            [prefix, suffix] = getAPI(auth, 'GET/friends/A')
                            custom_url = prefix + remoteAuthor + suffix
                            print "friend request url: "
                            print custom_url

                            
                            pfriends = requests.get(custom_url, headers=headers).json()["authors"]
                            if(handler.atlOneFriend(localAuthor, pfriends)):
                                return jsonify(makeCommentJson(got[0][2]), {"page":pg, "size":sz})
                            # else:
                                #No permission coz the requesting remote user is not foaf of the post author in my server
                        # else:
                            #No permission coz either this post is private or serveronly, so cant access its comments
                # else:
                    #Post Not in my server, so does its corresponding comments

        else:
            return "NO AUTHENTICATION", 401


#    @requires_auth
    def post(self):
        if is_accessible():

            APP_state = loadGlobalVar()
            if  request.headers.get("Foreign-Host") == "false":
                output = getCookie("comment_post")
                if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
                    return output

                cookie = output
                #For both local and remote request
                if "session_id" in cookie:
                    sessionID = cookie["session_id"]
                    if sessionID in APP_state["session_ids"]:
                          
                        currentTime = datetime.now()
                        data = request.get_json(force=True)
                        comment["post_id"] = data["post"].split("/")[4]
                        comment["comment_text"] = data["comment"]["comment"]
                        comment["author_id"] = data["comment"]["author"]["id"]
                        comment["author_host"] = data["comment"]["author"]["host"]
                        comment["author_name"] = data["comment"]["author"]["displayName"]
                        comment["author_url"] = data["comment"]["author"]["url"]
                        comment["author_github"] = data["comment"]["author"]["github"]
                        #comment["comment_id"] = data["comment"]["guid"]
                        #comment["published"] = data["comment"]["published"]
                        data["comment"]["author"]["guid"] = uuid.uuid().hex
                        data["comment"]["published"] = currentTime.isoformat() 

                        start = data["post"].split("/")[0]
                        middle = data["post"].split("/")[1]
                        end = data["post"].split("/")[2]

                        addr = start + middle
                        addr += end
                      
                        if addr == myip:
                            if handler.make_comment(comment):
                                return {"query" : "addComment", "success" : "true", "message" : "Comment Added"}
                            else:
                                return {"query" : "addComment", "success" : "false", "message" : "Comment not allowed"}
                        else:
                            return requests.post(data["post"]+"/comments", data).json()

                    else:
                        return {"Response" : "SESSION_ID_ERROR"}, 403

                else:
                    return {"Response"  :  "SESSION_ERROR"}, 403

            else:
            #Remote
                data = request.json
                comment["post_id"] = data["post"].split("/")[4]
                comment["comment_text"] = data["comment"]["comment"]
                comment["author_id"] = data["comment"]["author"]["id"]
                comment["author_host"] = data["comment"]["author"]["host"]
                comment["author_name"] = data["comment"]["author"]["displayName"]
                comment["author_url"] = data["comment"]["author"]["url"]
                comment["author_github"] = data["comment"]["author"]["github"]
                comment["comment_id"] = data["comment"]["guid"]
                comment["published"] = data["comment"]["published"]

                
                if handler.make_comment(comment):
                    return {"query" : "addComment", "success" : "true", "message" : "Comment Added"}
                else:
                    return {"query" : "addComment", "success" : "false", "message" : "Error when add"}

        else:
            return "NO AUTHENTICATION", 401

'''
class Edit_Post(Resource):

    def post(self, post_id):

        output = getCookie("edit_post")
        if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
            return output

        cookie = output
        if "session_id" in cookie:
            sessionID = cookie["session_id"]
            if sessionID in APP_state["session_ids"]:
                userID = APP_state["session_ids"][sessionID]
                data = request.form

                post = {}
                post["author_id"] = request.form["author_id"]
                post["title"] = request.form["title"]
                post["text"] = request.form["text"]
                perm = request.form["view_permission"]
                if perm =="Public":
                    perm = 1
                    print "yeah"
                elif perm =="Private":
                    perm = 2
                elif perm == "Friends":
                    perm = 3
                elif perm == "FOAF":
                    perm = 4
                post["view_permission"]= perm

                return handler.make_post(post), 201

                result = handler.updateProfile(data)
                if result == True:
                    return "status : SUCCESS", 200
                elif result == "NO_MATCH":
                    return "status : NO_MATCH", 200
                elif result == "DB_FAILURE":
                    return "status : DB_FAILURE", 200

            else:
                print "WARNING! Session id not inside server!"
                return "status : INVALID_SESSION_ID", 200

        else :

            print 'WARNING! "session_id" field is not found inside cookie!'
            return "status : CLIENT_FAILURE", 200
'''
