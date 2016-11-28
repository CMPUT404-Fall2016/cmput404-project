import uuid
from model import *
import requests
import json
from base64 import b64encode
from Nodes import *

"""
THINGS TO DO:

* Make sure the servers db contains an entry of our server.


"""


def isFriend(param):
  """
  This will be called in response to :
  GET http://service/friends/<authorid1>/<authorid2>  Checks whether the author1 is friends with author 2. 

  Refer to line : 156-169     

  param["author1"] = authorid1
  param["author2"] = authorid2
  """

  author_id1 = param["author1"]
  author_id2 = param["author2"]
  query_param={}
  query_param['areFriends'] = [author_id1, author_id2]
  results=Author_Relationships.query(query_param)
  if len(results) > 0 :
      # print results[0].relationship_type  
      # assert(len(results) == 1), "Duplicate author_relationships entry found!"
    return True

  query_param['areFriends'] = [author_id2, author_id1] # Search with reverse query
  results=Author_Relationships.query(query_param)
  if len(results) > 0 :
      # print results[0].relationship_type  
      # assert(len(results) == 1), "Duplicate author_relationships entry found!"
      return True

  return False


def createAuthHeaders(host_name):

    server_obj = db.session.query(Servers).filter(Servers.IP == host_name).all()[0]
    auth_str = b"%s:%s"%(server_obj.user_name, server_obj.password)
    userAndPass = b64encode(auth_str).decode("ascii")
    headers = { 'Authorization' : 'Basic %s' %  userAndPass }
    return headers

def fetchForeignAuthor(param):

    """
    param['id'] = author_id
    param['url'] = url for getting the author
    param['host'] = host name for the author
    """



    headers = createAuthHeaders(param['host'])
    headers['Content-type'] = 'application/json'
    r = requests.get(param['url'], headers = headers)
    print "url : " + param['url']
    if r.status_code != 200:
        print "status code : %s"%(r.status_code)
        return None
    if r.text == "":
        print "found empty body from foreign server during searching author"
        return None
    # print r.text
    try:
        body = r.json()
        return body

    except Exception as e:
        print "Failed to parse JSON sent from url : " + param['url'] + "...Error: " + e
        return None



def getFriendList(param, APP_state):


    """
    This will be called in response to :
    GET http://service/friends/<authorid>  returns friendlist of author with authorid 

    Refer to line : 144-154     

    param["author"] = author_id
    param["local_server_Obj"] = local server obj

    TODO: add code for handling in Author_Relationships.query() when server and author id are given instead of objects
    """

    author_id = param["author"]
    server_index = param["local_server_Obj"].server_index
    relationship_type = 3 #FOR FRIENDS
    
    query_param={}
    query_param["server_author_1"] = [server_index, author_id] 
    results1 = Author_Relationships.query(query_param)
    results1 = updateFriendship(results1, author_id, server_index)
    # print results1
    friendList = serializeFriendList(results1, 2)

    query_param={}   
    query_param["server_author_2"] = [server_index, author_id] #Reverse query, posing the author as the second user in the table
    results2 = Author_Relationships.query(query_param)
    # print results2
    results2 = updateFriendship(results2, author_id, server_index)
    friendList = serializeFriendList(results2, 1) + friendList


    # for friend in friendList:
    #     if friend['host'] == APP_state["local_server_Obj"].IP:            
    #         results = db.session.query(Authors).filter(Authors.author_id == friend['id']).all()
    #         if len(results) != 0:
    #             friend['displayName'] = results[0].name
    #         else:
    #             friend['displayName'] = "User Not found locally"

    #     else:
    #         author = fetchForeignAuthor(friend)
    #         if author != None :
    #             friend['displayName'] = author['displayName']
    #         else:
    #             friend['displayName'] = "User Not found in host : " + friend['host']

    return friendList


def updateFriendship(friendList, author_id, server_index):

    for friend in friendList:
        print "from updateFriendship"
        print "%d and %d"%(friend.authorServer1_id, friend.authorServer2_id)
        if (friend.authorServer1_id != server_index):

            server = db.session.query(Servers).filter(Servers.server_index == friend.authorServer1_id).all()[0]
            foreign_host = server.IP
            isFriend = checkForeignFriends(foreign_host, author_id, friend.author1_id)
            if isFriend != None:
                if isFriend == True:
                    if friend.relationship_type == 2:
                        friend.relationship_type = 3
                else:
                    if friend.relationship_type == 3: 
                        friend.relationship_type = 2
                    elif friend.relationship_type == 1:
                        friendList.remove(friend)
                        db.session.delete(friend)


        if (friend.authorServer2_id != server_index):

            server = db.session.query(Servers).filter(Servers.server_index == friend.authorServer2_id).all()[0]
            foreign_host = server.IP
            isFriend = checkForeignFriends(foreign_host, author_id, friend.author2_id)
            if isFriend != None:
                if isFriend == True:
                    if friend.relationship_type == 1:
                        friend.relationship_type = 3
                else:
                    if friend.relationship_type == 3: 
                        friend.relationship_type = 1
                    elif friend.relationship_type == 2:
                        friendList.remove(friend)
                        db.session.delete(friend)

      
        db.session.commit()
    
    return friendList


def checkForeignFriends(host_name, author_ID, friend_ID):

    [prefix, suffix] = getAPI(host_name, 'GET/friends/A1/A2')
    url = prefix + author_ID + '/' + friend_ID + suffix
    print "from checkForeignFriends, url : %s"%(url)
    headers['Content-type'] = 'application/json'
    r = requests.get(url, headers = headers)
    if r.status_code == 200:
        if r.text == "":
            print "from checkForeignFriends, empty respond body found"
            return None
        recvJSON = r.json()
        if 'friends' in recvJSON.keys():
            isFriend = recvJSON['friends']
            if type(isFriend) == bool:
                print "Friends with %s from %s is %s: "%(friend_ID, host_name, str(isFriend))
                return isFriend
            else:
                print "from checkForeignFriends, friends key is not boolean!"
                return None
        else:
            print "from checkForeignFriends, friends key is not present!"
            return None

    else :
        print "from checkForeignFriends, status code is not 200"
        return None



def serializeFriendList(FriendList, number):

    friendlist = []
    for friendship in FriendList:
        if friendship.relationship_type != 3:
            continue
            
        temp={}
        if number == 1:
            host = db.session.query(Servers).filter(Servers.server_index == friendship.authorServer1_id).all()[0].IP
            temp['host']=host
            temp['id']=friendship.author1_id
            temp['displayName']=friendship.author1_name
            [prefix, suffix] = getAPI(host,'GET/author/A')
            temp['url'] =  prefix + temp['id'] + suffix 

        elif number == 2:
            host = db.session.query(Servers).filter(Servers.server_index == friendship.authorServer2_id).all()[0].IP
            temp['host']=host
            temp['id']=friendship.author2_id
            temp['displayName']=friendship.author2_name
            [prefix, suffix] = getAPI(host,'GET/author/A')
            temp['url'] =  prefix + temp['id'] + suffix 

        friendlist.append(temp)

    # print friendlist
    return friendlist


def areFriends_LIST(param):
  """
  This will be called in response to :
  POST http://service/friends/<authorid>  POSTS a JSON containing lists of authorids and returns with a list containing those IDs 
  who are friend with authorid author

  Refer to line : 171-196

  param["author"] = authorid in query
  param["authorsForQuery"] = [author_id1, author_id2 ,...., author_idn]
  """

  author_id_List = param["authorsForQuery"]
  my_author_id = param["author"]
  my_friends=[]

  for other_author_id in author_id_List :

      query_param = {}
      query_param["author1"] = my_author_id
      query_param["author2"] = other_author_id
      if isFriend(query_param) is True:
          my_friends.append(other_author_id)

  return my_friends


def addNewServer():
    pass

def processFriendRequest(param, APP_state):

    """
    This will be called in response to :
    POST http://service/friendrequest  POSTS a JSON containing author info and the to be friended author's info and this sends a friendrequest

    refer to line 227-244

    param["from_author"] = author id who send the request
    param["from_author_name"] = from author name
    param["to_author"] = the author to whom the request is sent to
    param["to_author_name"] = to author name
    param["from_serverIP"] = server IP hosting the from_author
    param["to_serverIP"] = obj of our local server 
    """

    # result = db.session.query(Authors).filter(Authors.author_id == param["to_author"]).all()
    # if len(result) == 0:
    #     return False


    to_serverIP = param["to_serverIP"]
    to_server_index=db.session.query(Servers).filter(Servers.IP == to_serverIP).all()[0].server_index

    from_serverIP = param["from_serverIP"]
    from_server_index=db.session.query(Servers).filter(Servers.IP == from_serverIP).all()[0].server_index

    print ".."
    # query_param = {}
    # query_param['server_author_1'] = [from_server_index, param['from_author']]
    # results = Author_Relationships.query(query_param) 
    # print type(results), len(results)
    results = db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == param['from_author'],
                                                            Author_Relationships.author2_id == param['to_author']
                                                            ).all()
    if len(results) >0 :
        if results[0].relationship_type == 2:
            print "came 1"
            results[0].relationship_type = 3
            db.session.commit()
        return True
    
    print "...."
    # query_param = {}
    # query_param['server_author_2'] = [from_server_index, param['from_author']]
    results = db.session.query(Author_Relationships).filter(Author_Relationships.author2_id == param['from_author'],
                                                            Author_Relationships.author1_id == param['to_author']
                                                            ).all()
    if len(results) >0 :
        if results[0].relationship_type == 1:
            print "came 2"
            results[0].relationship_type = 3
            query_param = {}
            query_param['sendTo'] = [from_server_index, param['from_author']]
            results = Friend_Requests.query(query_param)
            if results != []:
                db.session.delete(results[0])
            db.session.commit()
        return True

    # print "....."
    if APP_state['local_server_Obj'].IP == from_serverIP:
        print "process 1"
        datum={}
        datum = {
                'AuthorRelationship_id' : uuid.uuid4().hex,
                'authorServer1_id' : from_server_index,
                'author1_id': param["from_author"],
                'author1_name': param["from_author_name"],
                'authorServer2_id' : to_server_index,
                "author2_id" : param["to_author"],
                'author2_name' : param["to_author_name"],
                'relationship_type' : 1
                }

        new_relationship = Author_Relationships(datum)
        db.session.add(new_relationship)
        db.session.commit()

    # print "......"
    if to_serverIP == APP_state['local_server_Obj'].IP :
        datum={}
        datum = {
                'friendrequests_id' : uuid.uuid4().hex, 
                'fromAuthor_id' : param['from_author'], 
                'fromAuthorServer_id' : from_server_index,
                'fromAuthorDisplayName' : param['from_author_name'],
                'toAuthor_id' : param["to_author"],
                'toAuthorServer_id' : to_server_index,
                'isChecked' : False
                 }

        query_param = {}
        query_param['server_author_1'] = [to_server_index, param['to_author']]
        results=db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == param['to_author'],
                                                              Author_Relationships.authorServer1_id == to_server_index,
                                                              Author_Relationships.relationship_type == 1
                                                              ).all()
        # print type(results), len(results)
        if len(results) >0 :
            results[0].relationship_type = 3
            db.session.commit()

        else:
            new_friendRequest = Friend_Requests(datum)
            try :
                db.session.add(new_friendRequest)
                db.session.commit()

            except Exception as e:
                print "Error occured while saving new friend request: ", e
                return False
    
    else:
        # to_server is a remote server not the local one
        print "here"
        sendFriendRequest(param)

    return True


def sendFriendRequest(param):
    """
    Sends FR on behalf of client to another host

    param["from_author"] = author id who send the request
    param["from_author_name"] = from author name
    param["to_author"] = the author to whom the request is sent to
    param["to_author_name"] = to author name
    param["from_serverIP"] = server IP hosting the from_author
    param["to_serverIP"] = obj of our local server 

    """

    body = {}
    body['query'] = 'friendrequest'
    body["author"] = {}
    body["author"]['id'] = param['from_author']
    body["author"]["host"] = param['from_serverIP']
    body['author']['displayName'] = param['from_author_name'] 
    body['friend'] = {}
    body['friend']['id'] = param['to_author']
    body['friend']['host'] = param['to_serverIP']
    body['friend']['displayName'] = param['to_author_name']

    [prefix, suffix] = getAPI(param['to_serverIP'], 'GET/author/A')
    body['friend']['url'] = prefix + body['friend']['id'] + suffix

    headers = createAuthHeaders(param['to_serverIP'])
    headers['Content-type'] = 'application/json'
    [prefix, suffix] = getAPI(param['to_serverIP'], 'POST/friendrequest')
    url = prefix + suffix
    r = requests.post(url, data=json.dumps(body), headers=headers)
    print "Sent a friend request to %s. Status code %d: "%(url, r.status_code) 
    return 


def serializeFriendRequestList(requestList):

  results = []
  for request in requestList:
      result = {}
      result["friendRequest_id"] = request.friendrequests_id
      result["fromAuthor_id"] = request.fromAuthor_id
      result["fromAuthorDisplayName"] = request.fromAuthorDisplayName
      result["fromServerIP"] = db.session.query(Servers).filter(Servers.server_index == request.fromAuthorServer_id).all()[0].IP
      result["isChecked"] = request.isChecked
      [prefix, suffix] = getAPI(result["fromServerIP"], 'GET/author/A')
      result["url"] = prefix + request.fromAuthor_id + suffix   
      results.append(result)

  return {"friendRequestList" : results}


def getFriendRequestList(param, APP_state):

  """
  CLIENT-SERVER API
  This will be called in response to :
  GET http://service/getFriendRequests  
    
  This is an API that is not in the assigned specifications but we created this for fetching friend requests.

  param["author"] = author1 id 
  param["server_Obj"] = Server object for the author being queried.
  """

  query_param = {}

  if "server_Obj" and "author" in param.keys():

      query_param['sendTo'] = [param["server_Obj"].server_index, param["author"]]
      results_FR = Friend_Requests.query(query_param)

      for FR in results_FR:
        if FR.fromAuthorServer_id == APP_state["local_server_Obj"].server_index:            
            results = db.session.query(Authors).filter(Authors.author_id == FR.fromAuthor_id).all()
            if len(results) != 0:
                FR.fromAuthorDisplayName = results[0].name
            else:
                FR.fromAuthorDisplayName = "User not found locally"
        else:
            host_name = db.session.query(Servers).filter(Servers.server_index == FR.fromAuthorServer_id).all()[0].IP
            friend = {}
            friend['id'] = FR.fromAuthor_id
            friend['host'] = host_name
            [prefix, suffix] = getAPI(host_name, 'GET/author/A')
            friend['url'] = prefix + friend['id'] + suffix 
            author = fetchForeignAuthor(friend)
            if author != None :
                FR.fromAuthorDisplayName = author['displayName']
            else:
                FR.fromAuthorDisplayName = "User Not found in host : " + host_name

      return serializeFriendRequestList(results_FR)
    
  else:
      print(' ERROR! ,"server_Obj" and "author" keys not found! please check GetFriendRequests function thats invoked for API : GET /getFriendRequests ')
      return None


def unFriend(param, APP_state):

    """
    CLIENT-SERVER API
    This will be called in response to :
    POST http://service/unfriend  POSTS a JSON containing author info and to be unfriended author's info and this unfriends.

    This is an API that is not in the assigned specifications but we created this for unfriending.

    param["author1"] = author1 id 
    param["author2"] = author2 id
    param["server_1_address"] = server1 IP  
    param["server_2_address"] = server2 IP 

    """

    # if ("author1" and "author2" and "server_1_address" and "server_2_address") not in param.keys():
    #   return "CLIENT_FAILURE"


    author1_id = param["author1"]
    author2_id = param["author2"]
    server1_IP = param["server_1_address"] 
    server2_IP = param["server_2_address"]
    server1_index = db.session.query(Servers).filter(Servers.IP == server1_IP).all()[0].server_index
    server2_index = db.session.query(Servers).filter(Servers.IP == server2_IP).all()[0].server_index


    query_param={}
    query_param["server_author_id1"]=[server1_index, author1_id]
    query_param["server_author_id2"]=[server2_index, author2_id]  
    results1 = Author_Relationships.query(query_param)

    query_param={}
    query_param["server_author_id1"]=[server2_index, author2_id] #In reversed order   
    query_param["server_author_id2"]=[server1_index, author1_id]
    results2 = Author_Relationships.query(query_param)

    results = results1 + results2
    # assert(len(results) == 1), "there should 1 row for each relationships"

    # if server1_index == APP_state["local_server_Obj"].server_index and server2_index == APP_state["local_server_Obj"].server_index:
        
    if results1 != []:
        friend_obj = results1[0]
        friend_obj.relationship_type = 2
        
        try:
            db.session.commit()
        except Exception as e:
            print("Error while unfriending! :", e)
            return False

    elif results2 != []:
        friend_obj = results2[0]
        friend_obj.relationship_type = 1

        try:
            db.session.commit()
        except Exception as e:
            print("Error while unfriending! :", e)
            return False

    # else:
    #     # If the other author is from foreign server, we will not delete the entry, we will set the relationship type to 1 or 2 accordingly

    #     try:
    #         db.session.delete(results[0])
    #         db.session.commit()

    #     except Exception as e:
    #         print("Error while unfriending! :", e)
    #         return False

    return True


def beFriend(param):

    """
    CLIENT-SERVER API
    This will be called in response to :
    POST http://service/acceptFriendshipRequest  POSTS a JSON containing author info and to be friended(accepting a request) author's info and this unfriends.

    This is an API that is not in the assigned specifications but we created this for friending.

    param["author1"] = author1 id 
    param["author2"] = author2 id
    param["server_1_address"] = server1 IP  
    param["server_2_address"] = server2 IP 
    param["author1_name"] = author 1 name
    param["author2_name"] = author 2 name
    """

    if isFriend(param) is True:
        return "DUPLICATE"

    author1_id = param["author1"]
    author2_id = param["author2"]
    server1_IP = param["server_1_address"] 
    server2_IP = param["server_2_address"]
    server1_index = db.session.query(Servers).filter(Servers.IP == server1_IP).all()[0].server_index
    server2_index = db.session.query(Servers).filter(Servers.IP == server2_IP).all()[0].server_index

    query_param={}
    query_param['server_author_id1'] = [server1_index, author1_id]
    query_param['server_author_id2'] = [server2_index, author2_id]
    results1=Author_Relationships.query(query_param)
    # print query_param

    query_param={}
    query_param['server_author_id1'] = [server2_index, author2_id]
    query_param['server_author_id2'] = [server1_index, author1_id]
    results2=Author_Relationships.query(query_param)
    # print query_param

    results = results1 + results2
    if len(results) == 0:
        print "GOT 1"
        datum={}
        datum["AuthorRelationship_id"] = uuid.uuid4().hex
        datum["authorServer1_id"] = server1_index
        datum["authorServer2_id"] = server2_index
        datum["author1_id"] = author1_id
        datum["author2_id"] = author2_id
        datum["author1_name"] = param["author1_name"]
        datum["author2_name"] = param["author2_name"]
        datum["relationship_type"] = 3 # Mutual friendship
        print "During accepting friend request, here is the datum dictionary for creating the entry : "
        print datum
        new_relationship = Author_Relationships(datum)

        try:

            db.session.add(new_relationship)
            db.session.commit()

        except Exception as e:
            print("Error while saving a relationship entry! : ", e)
            return False

        # param = {}
        # param["from_author"] = author2_id
        # param["to_author"] = author1_id
        # param["from_author_name"] = db.session.query(Authors).filter(Authors.author_id == author2_id).all()[0].name
        # param["to_author_name"] = Friend_Requests.query({"sendTo": [server2_index, author2_id]})[0].fromAuthorDisplayName
        # param["from_serverIP"] = server2_IP
        # param["to_serverIP"] = server1_IP 
        # sendFriendRequest(param)


    else:

        print "GOT 2"
        relationship = results[0]
        relationship.relationship_type = 3

        try:
            # db.session.add(relationship)
            db.session.commit()

        except Exception as e:
            print("Error while saving a relationship entry! : ", e)
            return False

    try :
        query_param={}
        query_param['sendTo'] = [server1_index, author1_id]
        query_param['sendFrom'] = [server2_index, author2_id]
        Friend_Requests.deleteRowsByQuery(query_param)

        query_param={}
        query_param['sendTo'] = [server2_index, author2_id]
        query_param['sendFrom'] = [server1_index, author1_id]
        Friend_Requests.deleteRowsByQuery(query_param)

    except Exception as e:
        print("Error while saving a relationship entry! : ", e)
        return False


    return True


def searchForeignAuthor(author_id):
    servers = db.session.query(Servers).filter(Servers.server_index > 0).all()
    author = None
    for server in servers:
        if server.shareWith == True:        
            param = {}
            param['id'] = author_id
            [prefix, suffix] = getAPI(server.IP, 'GET/author/A')
            param['url'] = prefix + author_id + suffix
            param['host'] = server.IP
            author = fetchForeignAuthor(param)
            if (author != None) and (author != {}) and (author != ''):
                print 'GOT author from %s'%(param['host'])
                return author

    return author

def getAuthor(param, foreign_host, APP_state):

    """
    This will be called in response to :
    GET http://service/author/<AUTHOR_ID>  Retrieves profile information about AUTHORID author. 

    Refer to line 248-273

    param["author"] = author_id
    param["local_server_Obj"] = local server obj
    """

    query_results = {}
    final_results = []
    using_author_name = False
    if "author" in param.keys():
        author_id = param["author"]
        results=db.session.query(Authors).filter(Authors.author_id == author_id).all()
    
    if "author_name" in param.keys():
        name = param["author_name"]
        results=db.session.query(Authors).filter(Authors.name == name).all()
        using_author_name = True

    
    if (len(results) == 0) :
        if (foreign_host == False) and (using_author_name == False):
            print "looking in foreign hosts"
            return searchForeignAuthor(param["author"])
        else:
            return None
    
    else:
        for author in results:
            # param["local_server_Obj"] = APP_state['local_server_Obj']
            param["local_server_Obj"] = getLocalServer()
            param['author'] = author.author_id
            query_results["id"] = author.author_id
            query_results["host"] = APP_state['local_server_Obj'].IP
            [prefix, suffix] = getAPI(APP_state['local_server_Obj'].IP, 'GET/author/A')
            query_results["url"] = prefix + author.author_id + suffix
            query_results["displayName"] = author.name
            query_results["bio"] = author.bio
            query_results["friends"] = getFriendList(param, APP_state)
            if author.github_id==None:
                query_results["githubUsername"] = ""
            else:
                query_results["githubUsername"] = author.github_id
            final_results.append(query_results)
            print "found author " + query_results["displayName"] + " id: " + query_results['id']

    if "author_name" in param.keys():
        return {"authors":final_results}
  
    elif "author" in param.keys():
        return final_results[0]


def getLocalServer():
    return db.session.query(Servers).filter(Servers.server_index == 0).all()[0]

def verifyAdmin(param):
    
    APP_state = loadGlobalVar()
    if APP_state['admin_credentials'] == None:
        print "NO admin exists"
        return False

    if param == APP_state['admin_credentials']:
        return True
    else:
        return False


def userLogin(param):

    """
    This will be called in response to :
    POST http://service/login  Used for login.

    example POST body:
    {
        login_name : "touqir",
        password : "123456"
    } 


    param["login_name"] = Name used for login
    param["password"] = password for authentication

    return values:
    returns a dictionary containing author info if successful
    1 if no match found
    2 if input data(login_name and password) is larger than specified in Authors schema
    -1 failure for some other reason
    """

    if "login_name" and "password" in param.keys():
        login_name = param["login_name"]
        password = param["password"]
    else:
        return "CLIENT_FAILURE"

    if len(password) > 30:
        return "BAD_INPUT"

    if len(login_name) > 60:
        return "BAD_INPUT"

    if verifyAdmin([login_name, password]):
        return "ADMIN"

    results=db.session.query(Authors).filter(Authors.login_name == login_name).all()

    if len(results) == 0:
        return "NO_MATCH"
    
    else :
        author = results[0]
        if author.password == password:
            if author.authorized == True:
                return serializeAuthors([author])[0]
            else:
                return "NOT_AUTHORIZED"

        else:
            return "NO_MATCH"



def serializeAuthors(authors):

    results = []
    for author in authors:
        datum = {}
        datum["author_id"]  = author.author_id
        datum["name"]       = author.name
        # datum["login_name"] = author.login_name
        # datum["password"]   = author.password
        # datum["address"]    = "edmonton, alberta, Canada"
        # datum["birthdate"]  = author.birthdate
        # datum["bio"]        = author.bio
        if author.github_id == None:
            datum["github_id"]  = ""
        else:
            datum["github_id"] = author.github_id
        # datum["numberOf_friends"] = author.numberOf_friends  
        # datum["numberOf_followers"] = author.numberOf_followers  
        # datum["numberOf_followees"] = author.numberOf_followees  
        # datum["numberOf_friendRequests"] = author.numberOf_friendRequests
        results.append(datum)

    return results  




def userRegistration(param):

    """
    This will be called in response to :
    POST http://service/register  Used for registration.

    example POST body:
    {
        login_name : "touqir",
        name : "Touqir Sajed",
        password : "123456",
    } 


    param["login_name"] = login name
    param["name"]   = user's name
    param["password"] = password

    """

    if ("login_name" and "name" and "password") not in param.keys():
        return "CLIENT_FAILURE"

    login_name = param["login_name"]
    if len(db.session.query(Authors).filter(Authors.login_name == login_name).all()) != 0 :
        return "DUPLICATE"

    name = param["name"]
    password = param["password"]

    if len(login_name) > 60 :
        return "BAD_INPUT"

    if len(name) > 60 :
        return "BAD_INPUT"

    if len(password) > 30 :
        return "BAD_INPUT" 

    # try:
    #   birthdate = datetime.datetime.strptime(birthdate_str, '%d-%m-%Y')
    # except Exception as e:
    #   print "Failed to convert birthdate to datetime object! : ", e
    #   return 2
   
    if verifyAdmin([login_name, password]):
        return "DUPLICATE"

    datum = {}
    datum["author_id"]  = uuid.uuid4().hex
    datum["name"]       = name
    datum["login_name"] = login_name
    datum["password"]   = password
    # datum["address"]    = "edmonton, alberta, Canada"
    # datum["birthdate"]  = birthdate
    # datum["bio"]        = bio
    # datum["github_id"]  = github_id

    datum["authorized"] = True
    new_author = Authors(datum)
    print "newly created ID : " + datum["author_id"]

    try:
        db.session.add(new_author)
        db.session.commit()

    except Exception as e:
        print "Failed to save new registered user! : ", e
        # str_ = "DB_FAILURE"
        return 'DB_FAILURE' 


    del datum["password"]
    del datum["login_name"]
    return datum



def userlogout(param):

    """
    Not sure if this necessary
    """

    pass



def updateProfile(param):

    """
    CUSTOM client-server API

    POST http://service/editProfile 

    param["author"]     = author id
    param["name"]       = user's name
    param["password"]   = password
    param["birthdate"]  = birthdate
    param["bio"]        = bio
    param["github_id"]  = github_id

    """

    if len(param.keys()) <= 1:
        return True

    results = db.session.query(Authors).filter(Authors.author_id == param["author"]).all()
    if len(results) == 0:
        return "NO_MATCH"

    author = results[0]

    if "name" in param.keys():
        author.name = param["name"]

    if "password" in param.keys():
        author.password = param["password"]

    if "birthdate" in param.keys():
        author.birthdate = param["birthdate"]

    if "bio" in param.keys():
        author.bio = param["bio"]

    if 'github_id' in param.keys():
        author.github_id = param['github_id']

    try:
        db.session.commit()

    except Exception as e:
        print "ERROR! Failed to update author's profile information! : ", e
        return "DB_FAILURE"

    return True


