import unittest
from db import db
from sample_data.data1 import *
from Model.Author_Relationships import Author_Relationships


class test_Author_Relationships(unittest.TestCase):


	def setUp(self):
		pass


    def SaveAllToDB(self):

        for AR in author_relationships:
            myAR=Author_Relationships(AR)
            self.matchFields(AR, myAR)
            self.assertTrue(myServer != None), server
            db.session.add(myServer)

        db.session.commit()


    def test_emptyAR(self):

    	myAR=Author_Relationships(empty_AR)
    	self.matchFields()


	def matchFields(self, test_data, ORM_object):



	def printDatum(self, test_data, ORM_object):

		print test_data
		print "printing ORM_object"
		print "ORM_object['AuthorRelationship_id'] = " + str(ORM_object.Author_Relationships)
		print "ORM_object['authorServer1_id'] = " + str(ORM_object.authorServer1_id)
		print "ORM_object['author1_id'] = " + str(ORM_object.author1_id)
		print "ORM_object['authorServer2_id'] = " + str(ORM_object.authorServer2_id)
		print "ORM_object['author2_id'] = " + str(ORM_object.author2_id)
		print "ORM_object['relationship_type'] = " + str(ORM_object.relationship_type)

