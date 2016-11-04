import init_location
import requests
from sample_data.data_API import *
import unittest
import json
import re

URL = "http://127.0.0.1:5000"  
firstTime = True
"""
CS stands for Client-Server
"""

COOKIE_NAMES = ["cookie_cmput404_author_id","cookie_cmput404_session_id","cookie_cmput404_github_id"] 

class Test_CS_API(unittest.TestCase):
	
	def setUp(self):
		global firstTime
		if firstTime:
			self.serverURL = URL
			self.s = requests.Session()

			firstTime = False

	def test(self):
		self.sample_Registration()

	def parseCookie(self, cookies):
		new={}
		for name in COOKIE_NAMES:
			if name in cookies.keys():
				new[name]=cookies.get(name)

		self.cookies = new

	def prepCookie(self, prepped):
		new = {}
		for name in self.s.cookies.keys():
			if name in COOKIE_NAMES:
				new[name] = self.s.cookies.get(name)
				# s=s+self.s.cookies.get(name)+'; '

		prepped.prepare_cookies(new)
		return prepped

	def cookie_assert(self, cookies, author=None):
		print cookies.keys()
		# assert(COOKIE_NAME in cookies.keys()), "No cookies found!"
		self.parseCookie(cookies)
		assert(self.cookies[COOKIE_NAMES[0]] != None), "there must be some author_id"
		assert(self.cookies[COOKIE_NAMES[1]] != None), "there must be some session_id"
		# assert(cookie['github_id'] != None), "there must be some github_id"
		if author != None:
			assert(self.cookies[COOKIE_NAMES[0]] == author['author_id']), "author_ids must match"

	def sample_Login(self):

		url = self.serverURL + "/login"
		headers = {'Content-type': 'application/json'}
		req1 = requests.Request('POST', url, data=json.dumps(author1_log), headers=headers)
		prepp1 = req1.prepare()
		prepp1 = self.prepCookie(prepp1)
		resp = self.s.send(prepp1)
		# print(resp.text)
		body = json.loads(resp.text)
		assert(body["status"] == "SUCCESS"), "Should be a success!"
		assert(body["name"] != None), "A display name should be there"
		self.cookie_assert(resp.cookies, author1_log)


	def sample_Registration(self):

		url = self.serverURL + "/register"
		headers = {'Content-type': 'application/json'}
		req1 = requests.Request('POST', url, data=json.dumps(author1_reg), headers=headers)
		# req1 = self.prepCookie(req1)
		prepp1 = req1.prepare()
		resp = self.s.send(prepp1)
		body = json.loads(resp.text)
		assert(body["status"] == "SUCCESS"), "Should be a success!"
		assert(body["name"] != None), "A display name should be there"
		self.cookie_assert(resp.cookies)
		author1_log["author_id"] = self.cookies[COOKIE_NAMES[0]]

		self.sample_Logout()
		self.sample_Login()
		self.sample_Logout()
		self.sample_Login()
		self.sample_EditProfile()
		self.sample_FetchAuthor()
		self.sample_Logout()


	def sample_Logout(self):

		url = self.serverURL + "/logout"
		req1 = requests.Request('GET', url)
		prepp1 = req1.prepare()
		prepp1 = self.prepCookie(prepp1)
		resp = self.s.send(prepp1)
		body = json.loads(resp.text)
		assert(body["status"] == "SUCCESS"), "Should be a success!"


	def sample_EditProfile(self):

		url = self.serverURL + "/editProfile"
		headers = {'Content-type': 'application/json'}
		req1 = requests.Request('POST', url, data=json.dumps(author1_edit), headers=headers)
		prepp1 = req1.prepare()
		prepp1 = self.prepCookie(prepp1)
		resp = self.s.send(prepp1)
		body = json.loads(resp.text)
		print body["status"]
		assert(body["status"] == "SUCCESS"), "Should be a success!"


	def sample_FetchAuthor(self):
		
		url = self.serverURL + "/author/"+ author1_log["author_id"]
		req1 = requests.Request('GET', url)
		prepp1 = req1.prepare()
		# prepp1 = self.prepCookie(prepp1)
		resp = self.s.send(prepp1)
		body = json.loads(resp.text)
		print body["status"]
		print "author_id: ", author1_log["author_id"]
		assert(body["status"] == "SUCCESS"), "Should be a success!"
		self.match_author1(body)

	def match_author1(self, body):

		assert(body['id'] == author1_log['author_id'])
		assert(body['host'] == URL)
		assert(body['displayName'] == author1_reg['name'])
		assert(body['url'] == (URL+'/author/'+author1_log['author_id']))
		assert(len(body['friends']) == 0)
		assert(body['github_username'] == author1_edit['github_id'])
		assert(body['bio'] == author1_edit['bio'])


if __name__ == '__main__':
	unittest.main()