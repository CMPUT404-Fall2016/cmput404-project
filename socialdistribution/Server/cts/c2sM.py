from flask import Flask, jsonify
from flask_restful import Resource, Api, abort, reqparse
from model import *
from pch import *

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



class Post_List(Resource):
	def get(self):
		rtl = [] 
		data = handler.getVisiblePosts(request.form)
		for entry in data:
			rtl.append({
									"post_id" :	entry[0].post_id,
									"title" :	entry[0].title,
									"text"	:	entry[0].text,
									"creation_time" : entry[0].creation_time
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
api.add_resource(Post_List, '/')

if __name__ == '__main__':
	for i in range(1, 2):
		currentTime = datetime.now()
		post1 = {}
		post1["post_id"] = i
		post1["author_id"] = 1
		post1["title"] = "test1"
		post1["text"]="TEXT1"
		post1["creation_time"]=currentTime 
		post1["view_permission"]=1
		post1["post_type"]=1
		post1["numberOf_comments"]=1
		post1["numberOf_URL"]=2
		post1["numberOf_images"]=2
		apost = Posts(post1)
		db.session.add(apost)
		db.session.commit()

	app.run(debug=True)



