import unittest
from db import db
from sample_data.data1 import *
# from Model.Friend_Requests import Friend_Requests
# from Model.Servers import Servers
# from Model.Authors import Authors
from model import *

class test_Friend_Requests(unittest.TestCase):


    def setUp(self):
        pass


    def saveServers(self):

        self.server1=Servers(server1)
        self.server2=Servers(server2)
        db.session.add(self.server1)
        db.session.add(self.server2)
        db.session.commit()


    def saveAuthors(self):

        self.author1=Authors(author1)
        self.author2=Authors(author2) #Wont save author 2 now!
        db.session.add(self.author1)
        db.session.add(self.author2)
        db.session.commit()


    def SaveAllToDB(self):

        self.FR2=Friend_Requests(FR2)
        self.assertTrue(self.FR2 != None), "Should not return None!"
        self.matchFields(FR2, self.FR2)
        self.assertTrue(self.FR2.insert()), "Should return True"

        self.FR1=Friend_Requests(FR1)
        self.assertTrue(self.FR1 != None), "Should not return None!"
        self.matchFields(FR1, self.FR1)
        self.assertTrue(self.FR1.insert()), "Should return True"


    def test_FriendRequests(self):

        self.saveServers()
        self.saveAuthors()
        self.SaveAllToDB()

        myFR=Friend_Requests(FR_empty)
        self.matchFields(FR_empty, myFR)

        query_param = {}
        query_param['friendrequests_id']="1"
        results=Friend_Requests.query(query_param)
        self.assertTrue(len(results) == 1), "Should return a single row"
        if len(results) == 1:
            self.matchFields(FR1,results[0]) 

        query_param = {}
        query_param['sendTo']=[self.server2.server_index, self.author1.author_id]
        results=Friend_Requests.query(query_param)
        self.assertTrue(len(results) == 1), "Should return a single row"
        if len(results) == 1:
            self.matchFields(FR1,results[0]) 


        query_param = {}
        query_param['sendFrom']=[self.server1.server_index, self.author1.author_id]
        results=Friend_Requests.query(query_param)
        self.assertTrue(len(results) == 2), "Should return two rows"
        if len(results) == 2:
            if FR1["friendrequests_id"] == results[0].friendrequests_id:
                self.matchFields(FR1,results[0]) 

            elif FR1["friendrequests_id"] == results[1].friendrequests_id: 
                self.matchFields(FR1,results[1]) 

            if FR2["friendrequests_id"] == results[0].friendrequests_id:
                self.matchFields(FR2,results[0]) 

            elif FR2["friendrequests_id"] == results[1].friendrequests_id: 
                self.matchFields(FR2,results[1]) 


    def matchFields(self, test_data, ORM_object):

        if ('friendrequests_id' and 'fromAuthor_id' and 'fromAuthorServer_id' and 'toAuthor_id' and 'toAuthorServer_id' and 'isChecked') not in test_data.keys():
            self.assertTrue(ORM_object == None), "ORM_object should be None"
            return 

        self.assertTrue(ORM_object.friendrequests_id == test_data['friendrequests_id'])
        self.assertTrue(ORM_object.fromAuthor_id == test_data['fromAuthor_id'])
        self.assertTrue(ORM_object.fromAuthorServer_id == test_data['fromAuthorServer_id'])
        self.assertTrue(ORM_object.toAuthor_id == test_data['toAuthor_id'])
        self.assertTrue(ORM_object.toAuthorServer_id == test_data['toAuthorServer_id'])
        self.assertTrue(ORM_object.isChecked == test_data['isChecked'])


def runTest():
    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_Friend_Requests)

    testRunner = unittest.TextTestRunner()
    test_Result = testRunner.run(test_suite)
