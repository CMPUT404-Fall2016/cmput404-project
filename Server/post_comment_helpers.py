import flask
import json
from flask import Flask, jsonify, request, Response
import requests
from flask_restful import Resource, Api, abort, reqparse
from model import *
from post_comment_handlers import *
import random, os
from model import *

from functools import wraps


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


#the is for server to server basic auth
def check_auth_post(username, password):
    """This function is called to check if a username /
        password combination is valid.
        """
    return username == 'servertoserver' and password == '654321'

def authenticate_post():
    """Sends a 401 response that enables basic auth"""
    return Response(
                    'Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth_post(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth_post(auth.username, auth.password):
            return authenticate_post()
        return f(*args, **kwargs)
    return decorated
#the is for server to server basic auth
#-----------------------------------------need @requires_auth




def makeAuthorJson(author):
    rt = {
        "id"    :   author.author_id,
        "host"  :   myip,
        "displayName"   :   author.name,
        "url"   :   myip +"/author/" + author.author_id,
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
        rt["previous"] = myip + "/posts/" + data[0].post_id + "comments?page=" + str(pg-1)
    if (pg+1)*rt["size"] < rt["count"]:
        rt["next"] = myip + "/posts/" + data[0].post_id + "/comments?page=" + str(pg+1)

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
                "published" :   data[i].creation_time,
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
        rt["previous"] = myip + "/posts?page=" + str(pg-1)
    if (pg+1)*rt["size"] < rt["count"]:
        rt["next"] = myip + "/posts?page=" + str(pg+1)

    #Posts
    if pg*rt["size"] < rt["count"]:
        for i in range(pg*rt["size"], (pg+1)*rt["size"]):
            if i == rt["count"]:
                break
            rt["posts"].append({
                "title" :   data[i][0].title,
                "source"    :   "",
                "origin"    :   "",
                "author"    :   makeAuthorJson(data[i][1]),
                "description"   :   data[i][0].description,
                "contentType"   :   data[i][0].content_type,
                "content"   :   data[i][0].content,
                "categories"    :   "abram bear",
                "published" :   data[i][0].creation_time,
                "visibility"    :   VIEW_PER[data[i][0].view_permission],
                "id"    :   data[i][0].post_id,
                "count" :   len(data[i][2]),
                "size"  :   5,
                "next"  :   myip + "/posts/"+data[i][0].post_id+"/comments",
                "comments"  :   makeCommentJson(data[i][2], {"size":None, "page":None})["comments"]
            })

    return rt



def getCookie(Operation_str):
    COOKIE ={}
    # print request.cookies.keys()
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
    def get(self, post_id):
        APP_state = loadGlobalVar()
        #Local Request
        if(request.args.get("Foreign-Host") == "false"):
            output = getCookie("get_one_post")
            if type(output) == flask.wrappers.Response:
                return output

            cookie = output
            if "session_id" in cookie:
                sessionID = cookie["session_id"]
                #print sessionID
                if sessionID in APP_state["session_ids"]:
                    rst = []
                    got = handler.getPost(post_id)
                    if len(got) != 0:
                        if got[0] in handler.getVisiblePosts(APP_state["session_ids"][sessionID]):
                            rst = got
                        else:
                            #No permission
                    else:
                        #The post is in other server
                        nodes = handler.getConnectedNodes()
                        params = {}
                        params["author_id"] = APP_state["session_ids"][sessionID]
                        params["post_id"] = post_id
                        for node in nodes:
                            rst += requests.get(node + "/posts/" + post_id, params = params).json
                        if  len(rst) != 0:
                            return rst[0]

                    paras = {}
                    paras["page"] = request.args.get('page')
                    paras["size"] = request.args.get('size')
                    return jsonify(makePostJson(rst, paras))

                else:
                    return {"Response" : "sessionID error"}
            else:
                return {"Response" : "Session not found"}

        #Remote Request
        else:
        #Assume we passed server to server auth
        #Assume this is the place we do remote get
            pid = request.args.get("post_id")
            remoteAuthor = request.args.get("author_id")
            got = handler.getPost(pid)

            if len(got) != 0:
                localAuthor = got[0][1].author_id
                if  got[0] in handler.getVisiblePosts(remoteAuthor):
                    return jsonify(makePostJson(got), {"page":None, "size":None})
                else:
                    if got[0][0].view_permission == 4:
                        pfriends = requests.get(request.remote_addr + "/friends/" + remoteAuthor).json["authors"]
                        if(handler.atlOneFriend(localAuthor, pfriends)):
                            return jsonify(makePostJson(got), {"page":None, "size":None})
                        else:
                            #No permission coz the requesting remote user is not foaf of the post author in my server
                    else:
                        #No permission coz either this post is private or serveronly
            else:
                #Post Not in my server



    def delete(self, post_id):
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



class All_Post(Resource):
    def get(self):
        #Local Request
        if(request.args.get("Foreign-Host") == "false"):
            paras = {}
            paras["page"] = request.args.get('page')
            paras["size"] = request.args.get('size')
            nodes = handler.getConnectedNodes()
            agre = []
            agre.append(jsonify(makePostJson(handler.getAllPosts(), paras)))
            for node in nodes:
                agre.append(requests.get(node + "/posts", paras).json)
            # Each json object contains all public posts from a server
            return agre

        #Remote
        else:
        #Assume we passed server to server auth
        #Assume this is the place we respond to remote get
            paras = {}
            paras["page"] = request.args.get('page')
            paras["size"] = request.args.get('size')
            return jsonify(makePostJson(handler.getAllPosts(), paras))


    def post(self):
        APP_state = loadGlobalVar()
        output = getCookie("post_post")
        if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code = 200 response is send back.
            return output

        cookie = output
        if "session_id" in cookie:
            sessionID = cookie["session_id"]

            if sessionID in APP_state["session_ids"]:

                data = request.json
                post = {}
                post["author_id"] = data["author_id"]
                post["title"] = data["title"]
                post["content"] = data["content"]
                post["content_type"] = data["content_type"]
                post["description"] = data["description"]
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

                if handler.make_post(post):
                    return {"query" : "addPost", "success" : "true", "message" : "Post Added"}
                else:
                    return {"query" : "addPost", "success" : "false", "message" : "Post not allowed"}

            else:
                return "Invalid Session ID", 403
        else:
            return "No Session", 403



class AuthorPost(Resource):
    def get(self):
        APP_state = loadGlobalVar()
        if  request.args.get("Foreign-Host") == "false":
            output = getCookie("get_available_posts")
            if type(output) == flask.wrappers.Response:
                return output
            cookie = output
            if "session_id" in cookie:
                sessionID = cookie["session_id"]
                if sessionID in APP_state["session_ids"]:
                    paras = {}
                    rt = []
                    paras["page"] = request.args.get('page')
                    paras["size"] = request.args.get('size')
                    rt.append(jsonify(makePostJson(handler.getVisiblePosts(APP_statep["session_ids"][sessionID]), paras)))
                    nodes = handler.getConnectedNodes()

                    paras["author_id"] = APP_state["session_ids"][sessionID]

                    for node in nodes:
                        rt.append(requests.get(node + "/author/posts"), paras = paras).json
                    return rt
                else:
                    return "Session_ID Error", 403

            else:
                return "SESSION_ERROR", 403

        else:
            #Remote
            remoteUsr = request.args.get("author_id")
            allPosts = handler.getVisiblePosts(remoteUsr)
            pfriends = requests.get(request.remote_addr + "/friends/" + remoteUsr).json["authors"]
            #Get all remaining foaf posts, check for each one, if the author is a friend of at least one usr in pfriends
            foafPosts = handler.getAllFoafPosts()

            for post in foafPosts:
                if  atlOneFriend(post.author_id, pfriends):
                    allPost.append(post)

            paras = {}
            paras["page"] = request.args.get('page')
            paras["size"] = request.args.get('size')

            return jsonify(makePostJson(allPosts), paras)
            


# gets all post made by AUTHOR_ID for current author to view.
class AuthorToAuthorPost(Resource):
    def get(self, author_id):
        APP_state = loadGlobalVar()
        if  request.args.get("Foreign-Host") == "false":
            output = getCookie("view_author_id_post")
            if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
                return output

            cookie = output
            if "session_id" in cookie:
                sessionID = cookie["session_id"]
                if sessionID in APP_state["session_ids"]:
                    paras = {}
                    paras["page"] = request.args.get('page')
                    paras["size"] = request.args.get('size')
                    if  author_id in handler.getAllUsers():
                        return jsonify(makePostJson(handler.getVisiblePostsByAuthor(APP_state["session_ids"][sessionID], author_id), paras))
                    else:
                        nodes = handler.getConnectedNodes()
                        paras["author_id"] = APP_state["session_ids"][sessionID]
                        for node in nodes:
                           rt = requests.get(node + "/author/" + str(author_id) + "/posts", paras).json
                           if rt["count"] > 0:    
                               return jsonify(makePostJson(rt), paras)
                        #No such author in any of the connecting servers
                else:
                    return "SESSION_ID_ERROR", 403

            else:
                return "SESSION_ERROR", 403
        else:
        #Remote
            if author_id in handler.getAllUsers():
                remoteUsr = request.args.get("author_id")
                allPosts = handler.getVisiblePostsByAuthor(remoteUsr, author_id)
                foafPosts = handler.getAllFoafPostsByUsr(author_id)                
                pfriends = requests.get(request.remote_addr + "/friends/" + remoteUsr).json["authors"]
                for post in foafPosts:
                    if(atlOneFriend(post.author_id, pfriends):
                        allPosts.append(post)

                paras = {}
                paras["page"] = request.args.get('page')
                paras["size"] = request.args.get('size')

                return jsonify(makePostJson(allPosts), paras)
                
            else:
                #We don't have this requested user in our server 

class Comment(Resource):

    def get(self, post_id):
        APP_state = loadGlobalVar()
        if  request.args.get("Foreign-Host") == "false":
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
                    return jsonify(makeCommentJson(handler.getComments(post_id), paras))

                return []

            else:
                 return "SESSION_ERROR", 403




    def post(self):
        output = getCookie("comment_post")
        if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
            return output

        cookie = output
        #For both local and remote request
        if "session_id" in cookie:
            sessionID = cookie["session_id"]
            if sessionID in APP_state["session_ids"]:

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
                    return requests.post(data["post"]+"/comments", data)

        else:
            return "SESSION_ERROR", 403



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
