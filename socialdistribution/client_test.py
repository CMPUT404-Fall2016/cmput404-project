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
    
    s=requests.Session()
    def setUp(self):
        global firstTime
        self.serverURL = URL
        # if firstTime:
        #     self.s = requests.Session()
        #     firstTime = False


    def test(self):
        self.login_()
        self.friend_()

    def login_(self):
        author1_log["author_id"] = self.sample_Registration(author1_reg)
        # self.sample_Logout()
        self.authorize(author1_log['author_id'])
        self.sample_Login(author1_log)
        self.sample_Logout()
        self.sample_Login(author1_log)
        self.sample_EditProfile()
        self.sample_Logout()
        self.sample_FetchAuthor()
        self.sample_FetchAuthorByName()


    def authorize(self, ID):
        url = URL + "/secretAuthorization/" + ID
        requests.get(url)

    def parseCookie(self, cookies):
        new={}

        for name in COOKIE_NAMES:
            if name in cookies.keys():
                new[name]=cookies.get(name)
            else:
                new[name]=None

        self.cookies = new

    def prepCookie(self, prepped):
        new = {}
        for name in self.s.cookies.keys():
            if name in COOKIE_NAMES:
                new[name] = self.s.cookies.get(name)
                # s=s+self.s.cookies.get(name)+'; '

        prepped.prepare_cookies(new)
        return prepped

    def cookie_assert(self, cookies, author=None, opt=None):
        print cookies.keys()
        self.parseCookie(cookies)
        assert(self.cookies[COOKIE_NAMES[0]] != None), "there must be some author_id"
        assert(self.cookies[COOKIE_NAMES[1]] != None), "there must be some session_id"
        if opt == "github_id_present":
            assert(self.cookies[COOKIE_NAMES[2]] != None), "there must be some github_id"
        if author != None:
            assert(self.cookies[COOKIE_NAMES[0]] == author['author_id']), "author_ids must match"

    def sample_Login(self, author):

        url = self.serverURL + "/login"
        headers = {'Content-type': 'application/json'}
        req1 = requests.Request('POST', url, data=json.dumps(author), headers=headers)
        prepp1 = req1.prepare()
        # prepp1 = self.prepCookie(prepp1)
        resp = self.s.send(prepp1)
        # print(resp.text)
        body = json.loads(resp.text)
        print body["status"]
        assert(body["status"] == "SUCCESS"), "Should be a success!"
        assert(body["name"] != None), "A display name should be there"
        self.cookie_assert(resp.cookies, author=author)


    def sample_Registration(self, author):

        url = self.serverURL + "/register"
        headers = {'Content-type': 'application/json'}
        req1 = requests.Request('POST', url, data=json.dumps(author), headers=headers)
        # req1 = self.prepCookie(req1)
        prepp1 = req1.prepare()
        resp = self.s.send(prepp1)
        body = json.loads(resp.text)
        assert(body["status"] == "NOT_AUTHORIZED")
        assert(body["name"] != None), "A display name should be there"
        # self.cookie_assert(resp.cookies)
        return body['author_id']



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
        # print body["status"]
        assert(body["status"] == "SUCCESS"), "Should be a success!"


    def sample_FetchAuthor(self):
        
        headers = {"Foreign_host" : "false"}
        url = self.serverURL + "/author/"+ author1_log["author_id"]
        req1 = requests.Request('GET', url, headers = headers)
        prepp1 = req1.prepare()
        # prepp1 = self.prepCookie(prepp1)
        resp = self.s.send(prepp1)
        body = json.loads(resp.text)
        print body["status"]
        print "author_id: ", author1_log["author_id"]
        assert(body["status"] == "SUCCESS"), "Should be a success!"
        self.match_author1(body)


    def sample_FetchAuthorByName(self):
        
        names=author1_reg['name'].split()
        first = ""
        last = ""
        if len(names) == 1:
            first=names[0]
        if len(names) == 2:
            first=names[0]
            last=names[1]

        if len(names) > 2:
            first=names[0]
            last = "".join(names[1:])

        url = self.serverURL + "/authorByName/?first=%s&last=%s"%(first,last)
        req1 = requests.Request('GET', url)
        prepp1 = req1.prepare()
        # prepp1 = self.prepCookie(prepp1)
        resp = self.s.send(prepp1)
        body = json.loads(resp.text)
        print body["status"]
        # print "author_id: ", author1_log["author_id"]
        assert(body["status"] == "SUCCESS"), "Should be a success!"
        assert("authors" in body.keys())
        print body
        self.match_author1(body['authors'][0])

    def match_author1(self, body):

        # print body.keys()
        assert(body['id'] == author1_log['author_id'])
        assert(body['host'] == URL)
        assert(body['displayName'] == author1_reg['name'])
        assert(body['url'] == (URL+'/author/'+author1_log['author_id']))
        assert(len(body['friends']) == 0)
        assert(body['githubUsername'] == author1_edit['github_id'])
        assert(body['bio'] == author1_edit['bio'])


    def friend_(self):
        # self.sample_Registration(author1_reg)
        # author1_log["author_id"] = self.cookies[COOKIE_NAMES[0]]
        self.sample_Login(author1_log)
        author1_log["author_id"] = self.cookies[COOKIE_NAMES[0]]
        self.sample_Logout()
        author2_log["author_id"] = self.sample_Registration(author2_reg)
        self.authorize(author2_log["author_id"])
        FR1 = createFriendRequest()
        self.sample_Login(author1_log)
        self.sample_friendrequest(author1_log, author2_log, FR1)
        self.sample_Logout()
        self.sample_Login(author2_log)
        received_FR = self.sample_getFriendRequests(author1_log)
        self.sample_AcceptFriendRequests(FR1)
        POST_body = {}
        POST_body['query'] = 'friends'
        POST_body['author'] = author2_log['author_id']
        POST_body['authors'] = [author1_log['author_id']]
        self.sample_ifFriends(author2_log, author1_log, POST_body)

        FL_body = self.sample_getFriendList(author2_log)
        self.matchFriendList(FL_body, [author1_log['author_id']])

        self.sample_Unfriend(author1_log['author_id'])
        FL_body = self.sample_getFriendList(author2_log)
        self.matchFriendList(FL_body, [])
        self.sample_Logout()



    def sample_friendrequest(self, from_, to, req):

        url = self.serverURL + "/friendrequest"
        headers = {'Content-type': 'application/json'}
        req1 = requests.Request('POST', url, data=json.dumps(req), headers=headers)
        prepp1 = req1.prepare()
        prepp1 = self.prepCookie(prepp1)
        resp = self.s.send(prepp1)
        body = json.loads(resp.text)
        # print body["status"]
        assert(body["status"] == "SUCCESS"), "Should be a success!"


    def sample_getFriendRequests(self, from_author):

        url = self.serverURL + "/getFriendRequests"
        req1 = requests.Request('GET', url)
        prepp1 = req1.prepare()
        prepp1 = self.prepCookie(prepp1)
        resp = self.s.send(prepp1)
        body = json.loads(resp.text)
        # print body
        assert(len(body['friendRequestList']) == 1)
        FR = body['friendRequestList'][0]
        assert(FR['fromAuthor_id'] == from_author['author_id'])
        return FR


    def sample_AcceptFriendRequests(self, FR):

        url = self.serverURL + "/acceptFriendRequest"
        headers = {'Content-type': 'application/json'}
        data = {}
        data['author'] = FR['author']['id']
        data['server_address'] = FR['author']['host']
        req1 = requests.Request('POST', url, data=json.dumps(data), headers=headers)
        prepp1 = req1.prepare()
        prepp1 = self.prepCookie(prepp1)
        resp = self.s.send(prepp1)
        body = json.loads(resp.text)
        assert(body["status"] == "SUCCESS")


    def sample_getFriendList(self, logged_author):

        url = self.serverURL + "/friends/" + logged_author['author_id']
        req1 = requests.Request('GET', url)
        prepp1 = req1.prepare()
        # prepp1 = self.prepCookie(prepp1)
        resp = self.s.send(prepp1)
        body = json.loads(resp.text)
        return body

    def sample_ifFriends(self, author1, author2, POST_request):
        url = self.serverURL + "/friends/" + str(author1['author_id']) + "/" + str(author2['author_id'])
        req1 = requests.Request('GET', url)
        prepp1 = req1.prepare()
        # prepp1 = self.prepCookie(prepp1)
        resp = self.s.send(prepp1)
        body_duo = json.loads(resp.text)

        url = self.serverURL + "/friends/" + author1['author_id']
        headers = {'Content-type': 'application/json'}
        req1 = requests.Request('POST', url, data=json.dumps(POST_request), headers=headers)
        prepp1 = req1.prepare()
        # prepp1 = self.prepCookie(prepp1)
        resp = self.s.send(prepp1)
        body_multiple = json.loads(resp.text)

        self.matchIfFriends(body_duo, body_multiple, author1['author_id'], [author2['author_id']])


    def matchIfFriends(self, response_duo, response_multiple, logged_author, TrueFriends):

        assert(response_duo['query'] == 'friends')
        # print response_duo['authors']
        assert(set(response_duo['authors']) == set([logged_author]+TrueFriends))
        assert(response_duo['friends'] == True)

        assert(response_multiple['query'] == 'friends')
        assert(response_multiple['author'] == logged_author)
        print response_multiple["authors"]
        assert(set(response_multiple['authors']) == set(TrueFriends))

    def matchFriendList(self, response, TrueFriends):

        assert(response['query'] == 'friends')
        assert(response['authors'] == TrueFriends)


    def sample_Unfriend(self, toUnfriend_id):

        url = self.serverURL + "/unFriend"
        headers = {'Content-type': 'application/json'}
        data = {}
        data['author'] = toUnfriend_id
        data['server_address'] = self.serverURL
        req1 = requests.Request('POST', url, data=json.dumps(data), headers=headers)
        prepp1 = req1.prepare()
        prepp1 = self.prepCookie(prepp1)
        resp = self.s.send(prepp1)
        body = json.loads(resp.text)
        assert(body['status'] == 'SUCCESS')





if __name__ == '__main__':
    unittest.main()