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
        output = getCookie("get_one_post")
        if type(output) == flask.wrappers.Response:
            return output

        cookie = output
        if "session_id" in cookie:
            sessionID = cookie["session_id"]
            #print sessionID
            if sessionID in APP_state["session_ids"]:

                rt = []
                data = handler.getPost(post_id)
                rt.append({
                                    "post_id"	: data[0].post_id,
                                    "title" :	data[0].title,
                                    "text"	:	data[0].text,
                                    "creation_time" : data[0].creation_time
                            })
                return jsonify(rt) #, 200
                #return json.dumps(rt), 200
            return "nothing"

        else:
            return "SESSION_ERROR", 403


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
        rtl = []
        data = handler.getAllPosts()
        for entry in data:
            rtl.append({
									"post_id" :	entry[0].post_id,
									"title" :	entry[0].title,
									"text"	:	entry[0].text,
									"creation_time" : entry[0].creation_time,
									"author_id"	: entry[0].author_id
								})
        return jsonify(rtl)

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
                post["text"] = data["content"]
                perm = data["visibility"]
                if perm =="Public":
                    perm = 1
                elif perm =="Private":
                    perm = 2
                elif perm == "Friends":
                    perm = 3 
                elif perm == "FOAF":
                    perm = 4
                else:
                    perm = 5
                post["view_permission"]= perm
				
                if handler.make_post(post):
                    return {"query" : "post a post", "success" : "true", "message" : "Post created"}
                else:
                    return {"query"	: "post a post", "success" : "failure", "message" : "Fail to create post"}

            else:
                return "SESSION_ERROR_Inner", 403
        else:
            return "SESSION_ERROR", 403
# gets all post made by AUTHOR_ID for current author to view.
class AuthorToAuthorPost(Resource):

    def get(self, AUTHOR_ID):

        output = getCookie("view_author_id_post")
        if type(output) == flask.wrappers.Response: #In case if cookie is not found a status code =200 response is send back.
            return output

        cookie = output
        if "session_id" in cookie:
            sessionID = cookie["session_id"]
            if sessionID in APP_state["session_ids"]:

            	data = handler.getVisiblePostsByAuthor(AUTHOR_ID)

            if selected_post == []:
                return "status : NO_MATCH", 200
            else:
                for entry in data:
                    rtl.append({
                               "post_id" :	entry[0].post_id,
                               "title" :	entry[0].title,
                               "text"	:	entry[0].text,
                               "creation_time" : entry[0].creation_time,
                               "author_id"	: entry[0].author_id
                               })

                return jsonify(rtl)
        else:
            return "SESSION_ERROR", 403


class Comment(Resource):
    def get(self):
        output = getCookie("get_comments")
        if type(output) == flask.wrappers.Response:
            return output
        
        cookie = output
        if "session_id" in cookie:
            sessionID = cookie["session_id"]
            #print sessionID
            if sessionID in APP_state["session_ids"]:
                rt = [] 
                data = handler.getComments(post_id)
                for entry in data:
                    rt.append({
					                "comment_id" : entry.comment_id,
	                                "author_id" : entry.author_id,
                                    "post_id"	: entry.post_id,
                                    "comment_text" :	entry.comment_text,
                                    "creation_time" : entry.creation_time
                              })
                return jsonify(rt) #, 200
                #return json.dumps(rt), 200
            return "nothing"

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


                return handler.make_comment(comment), 201

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






'''
if __name__ == '__main__':
	for i in range(1, 55):
		currentTime = datetime.now()
		post = {}
		post["author_id"] = i
		post["title"] = "test" + str(i)
		post["text"]="TEXT" + str(i)
		post["view_permission"]=random.randint(1, 5)
		post["post_type"]=1
		post["numberOf_comments"]=0
		post["numberOf_URL"]=0
		post["numberOf_images"]=0
		post["images"] = []
		post["images"].append(os.urandom(100000))
		handler.make_post(post)

	app.run(debug=True)
'''
