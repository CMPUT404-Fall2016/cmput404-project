import flask
import json
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, abort, reqparse
from model import *
from pch import *
import random, os


handler = RestHandlers()
COOKIE_NAME = "cookie_cmput404_"
COOKIE_NAMES = ["cookie_cmput404_author_id","cookie_cmput404_session_id","    cookie_cmput404_github_id"]
VIEW_PER = ["", "PUBLIC", "PRIVATE", "FRIENDS", "FOAF", "SERVERONLY"]
if 'local_server_Obj' in APP_state.keys():
    myip = APP_state['local_server_Obj'].IP
else:
    myip = None



def makeAuthorJson(author):
    rt = {
        "id"	:	author.author_id,
        "host"	:	myip,
        "displayName"	:	author.name,
        "url"	:	myip +"/author/" + author.author_id,
        "github"	:	author.github_id
    }
    return rt


def makeCommentJson(data, args):
   #Init
    rt = {
			"query"	:	"comments",
			"count"	:	len(data),
            "size"	:	5,
            "comments"	:	[]
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
                "author"	:	{
                                    "id"	:	data[i].author_id,
                                    "host"	:	data[i].author_host,
                                    "displayName"	:	data[i].author_name,
                                    "url"	:	data[i].author_url,
                                    "github"	:	data[i].author_github
                                },
                "comment"	:	data[i].comment_text,
                "contentType"	:	data[i].content_type,
                "published"	:	data[i].creation_time,
                "id"	: data[i].comment_id
            })

    return rt




def makePostJson(data, args):
    #Init
    rt = {
			"query"	:	"posts",
			"count"	:	len(data),
            "size"	:	5,
            "posts"	:	[]
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
                "title"	:	data[i][0].title,
                "source"	:	"",
                "origin"	:	"",
                "author"	:	makeAuthorJson(data[i][1]),
                "description"	:	data[i][0].description,
                "contentType"	:	data[i][0].content_type,
                "content"	:	data[i][0].content,
                "categories"	:	"abram bear",
                "published"	:	data[i][0].creation_time,
                "visibility"	:	VIEW_PER[data[i][0].view_permission],
                "id"	:	data[i][0].post_id,
                "count"	:	len(data[i][2]),
                "size"	:	5,
                "next"	:	myip + "/posts/"+data[i][0].post_id+"/comments",
                "comments"	:	makeCommentJson(data[i][2], {"size":None, "page":None})["comments"]
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
                        nodes = handler.getConnectedNodes()
                        params = {}
                        params["author_id"] = APP_state["session_ids"][sessionID]
                        params["post_id"] = post_id
                        for node in nodes:
                            rst += requests.get(node + "/posts/" + post_id, params = params).json()
                        if	len(rst) != 0:
                            return rst[0]

                    paras = {}
                    paras["page"] = request.args.get('page')
                    paras["size"] = request.args.get('size')
                    return jsonify(makePostJson(rst, paras))

                return {"Response" : "session error"}

            else:
                return {"Response" : "Session not found"}

        #Remote Request
        else:
        #Assume we passed server to server auth
        #Assume this is the place we do remote get
            pid = request.args.get("post_id")
            got = handler.getPost(pid)
            if len(got) != 0:
                localAuthor = got[0][1].author_id
                if	got[0] in handler.getVisiblePosts(request.args.get(author_id)):
                    return jsonify(makePostJson(got), {"page":None, "size":None})
                else:
                    if got[0][0].view_permission == 4:
                        pfriends = requests.get(request.remote_addr + "/friends/" + request.args.get(author_id)).json()["authors"]
                        if(handler.atlOneFriend(localAuthor, pfriends)):
                    		return jsonify(makePostJson(got), {"page":None, "size":None})


    def delete(self, post_id):
        output = getCookie("delete_post")
        if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code = 200 response is send back.
            return output

        cookie = output
        if "session_id" in cookie:
            sessionID = cookie["session_id"]
            if sessionID in APP_state["session_ids"]:

                if handler.delete_post(post_id):
                    return '', 201
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
                agre.append(requests.get(node + "/posts").json())
            # Each json object contains all public posts from a server
            return agre

        #Remote
        else:
        #Assume we passed server to server auth
        #Assume this is the place we do remote get
            paras = {}
            paras["page"] = request.args.get('page')
            paras["size"] = request.args.get('size')
            return jsonify(makePostJson(handler.getAllPosts(), paras))


    def post(self):
		#'''
        output = getCookie("post_post")
        if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
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
                    return {"query" : "addPost", "success" : "true", "message" : "Post created"}
                else:
                    return {"query"	: "addPost", "success" : "false", "message" : "Fail to create post"}

            else:
                return "Invalid Session", 403
        else:
            return "No Session", 403


class AuthorPost(Resource):
    def get(self):
        if  request.args.get("Foreign-Host") == "false":

            output = getCookie("get_available_posts")
            if type(output) == flask.wrappers.Response:
                return output

            cookie = output
            if "session_id" in cookie:
                sessionID = cookie["session_id"]

                if sessionID in APP_state["session_ids"]:
                    paras = {}
                    paras["page"] = request.args.get('page')
                    paras["size"] = request.args.get('size')
                    rt.append(jsonify(makePostJson(handler.getVisiblePosts(APP_statep["session_ids"][sessionID]), paras)))
                    nodes = handler.getConnectedNodes()

                    params = {
                                 "author_id"	:	APP_state["session_ids"][sessionID]
                             }
                    for node in nodes:
                        rt.append(requests.get(node + "/author/posts"), params = params).json()

                    return rt
                return []

            else:
                return "SESSION_ERROR", 403
        else:
            #Remote
            allP = handler.getVisiblePosts(request.args.get("author_id"))
            pfriends = requests.get(request.remote_addr + "/friends/" + request.args.get(author_id)).json()["authors"]
            #Get all remaining foaf posts, check for each one, if the author is atlOneFriend of pfriends





# gets all post made by AUTHOR_ID for current author to view.
class AuthorToAuthorPost(Resource):

    def get(self, author_id):

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
                return jsonify(makePostJson(handler.getVisiblePostsByAuthor(APP_statep["session_ids"][sessionID], author_id), paras))

        else:
            return "SESSION_ERROR", 403


class Comment(Resource):

    def get(self, post_id):
        if	request.args.get("Foreign-Host") == "false":
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
        if "session_id" in cookie:
            sessionID = cookie["session_id"]
            if sessionID in APP_state["session_ids"]:

                data = request.json
                comment["post_id"] = data["post_id"]
                comment["author_id"] = data["author_id"]
                comment["comment_text"] = data["comment_text"]

                if handler.make_comment(comment):
                    return {"query" : "addComment", "success" : "true", "message" : "Comment created"}
                else:
                    return {"query"	: "addComment", "success" : "false", "message" : "Fail to create comment"}

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
