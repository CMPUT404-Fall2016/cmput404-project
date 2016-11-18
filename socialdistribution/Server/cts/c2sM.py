from flask import Flask, jsonify
from flask_restful import Resource, Api, abort, reqparse
from model import *
from pch import *
import random, os

app = Flask(__name__)
api = Api(app)

handler = RestHandlers()

class Post(Resource):
	def get(self, post_id):
		data = handler.getPost(post_id)
		rt =	{
							"post_id"	: data[0].post_id,
							"title" :	data[0].title,
							"text"	:	data[0].text,	
							"creation_time" : data[0].post.creation_time
					}

		return jsonify(rt)



	def delete(self, post_id):
		if handler.delete_post(post_id):
			return '', 201



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
		data = request.form
		return handler.make_post(data), 201	



class Comment(Resource):
	def post(self):
		data = request.form
		return handler.make_comment(data), 201


api.add_resource(Post, '/<string:post_id>')
api.add_resource(Comment, '/api/comment')
api.add_resource(All_Post, '/service/posts')

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



