import unittest
from db import db
from sample_data.data1 import *
# from Model.Author_Relationships import Author_Relationships
# from Model.Servers import Servers
# from Model.Authors import Authors
from model import *

class test_Author_Relationships(unittest.TestCase):


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
        db.session.commit()


    def SaveAllToDB(self):

        self.AR2=Author_Relationships(AR2)
        self.assertTrue(self.AR2 != None), "Should not return None!"
        self.matchFields(AR2, self.AR2)
        self.assertTrue(self.AR2.insert()), "Should return True"

        self.AR1=Author_Relationships(AR1)
        self.assertTrue(self.AR1 != None), "Should not return None!"
        self.matchFields(AR1, self.AR1)
        self.assertTrue(self.AR1.insert() == False), "Should return False"


    def test_emptyAR(self):

        myAR=Author_Relationships(AR_empty)
        self.matchFields(AR_empty, myAR)


    def test_AuthorRelationships(self):

        self.saveServers()
        self.saveAuthors()
        self.SaveAllToDB()

        # myAR = Author_Relationships.query.filter_by(AuthorRelationship_id=1).all()
        # self.assertTrue(len(myAR) == 1), "Should return a single row!!"
        # self.matchFields(AR1, myAR[0])

        # myAR = Author_Relationships.query.filter_by(AuthorRelationship_id=2).all()
        # self.assertTrue(len(myAR) == 1), "Should return a single row!!"
        # self.matchFields(AR2, myAR[0])

        # myARs = Author_Relationships.query.filter_by(authorServer1_id = server1["server_index"], author1_id = author1["author_id"])
        # self.assertTrue(len(AR) == 2), "Should return 2 rows!"

        query_param={}
        query_param["server_author_1"]=[self.server1, self.author1]
        query_param["server_author_2"]=[self.server2, self.author1]
        results=Author_Relationships.query(query_param)
        self.assertTrue(len(results) == 1), "Should return a single row"
        if len(results) == 1:
            self.matchFields(AR2,results[0]) 

        # query_param["server_author_1"]=[self.server1, self.author1]
        # query_param["server_author_2"]=[self.server2, self.author2]
        query_param={}
        results=Author_Relationships.query(query_param)
        self.assertTrue(len(results) == 1), "Should return a single row"
        if len(results) == 1:
            self.matchFields(AR2,results[0]) 

        db.session.query(Author_Relationships).delete()
        db.session.commit()


    def matchFields(self, test_data, ORM_object):

        if ('AuthorRelationship_id' and 'authorServer1_id' and 'author1_id' and 'authorServer2_id' and 'author2_id' and 'relationship_type') not in test_data.keys():
            self.assertTrue(ORM_object == None), "ORM_object should be None"
            return 

        self.assertTrue(ORM_object.AuthorRelationship_id == test_data['AuthorRelationship_id'])
        self.assertTrue(ORM_object.author1_id == test_data['author1_id'])
        self.assertTrue(ORM_object.author2_id == test_data['author2_id'])
        self.assertTrue(ORM_object.authorServer1_id == test_data['authorServer1_id'])
        self.assertTrue(ORM_object.authorServer2_id == test_data['authorServer2_id'])
        self.assertTrue(ORM_object.relationship_type == test_data['relationship_type'])


    def printDatum(self, test_data, ORM_object):

        print test_data
        print "printing ORM_object"
        print "ORM_object['AuthorRelationship_id'] = " + str(ORM_object.Author_Relationships)
        print "ORM_object['authorServer1_id'] = " + str(ORM_object.authorServer1_id)
        print "ORM_object['author1_id'] = " + str(ORM_object.author1_id)
        print "ORM_object['authorServer2_id'] = " + str(ORM_object.authorServer2_id)
        print "ORM_object['author2_id'] = " + str(ORM_object.author2_id)
        print "ORM_object['relationship_type'] = " + str(ORM_object.relationship_type)



def runTest():
    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_Author_Relationships)

    testRunner = unittest.TextTestRunner()
    test_Result = testRunner.run(test_suite)
