import unittest
from db import db
from sample_data.data1 import *
from Model.Authors import Authors


class test_Authors(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_author1(self, willClear=True, willQuery=True):

        print "Testing author1..."
        myAuthor = Authors(author1)
        self.assertTrue(myAuthor != None), "ORM object should not be None!"

        self.matchFields(author1, myAuthor)
        self.printDatum(author1, myAuthor)
        
        db.session.add(myAuthor)
        db.session.commit()
        
        if willQuery is True:

            myAuthors=Authors.query.all()
            self.assertTrue(len(myAuthors) == 1), "Number of records should be 1!"
            self.matchFields(author1, myAuthors[0])
            self.printDatum(author1, myAuthors[0])
        
        if willClear is True:
        
            if willQuery is True:
                db.session.delete(myAuthors[0])
            else:
                db.session.delete(myAuthor)
        
            db.session.commit()

    

    def test_NoAuthorID(self):
        
        print "Testing author with empty Datum"
        myAuthor=Authors(author_empty)
        self.assertTrue(myAuthor == None), "ORM object should be none!"



    def test_author2(self, willClear=True, willQuery=True):

        print "Testing author2..."
        myAuthor=Authors(author2)
        self.assertTrue(myAuthor != None), "ORM object should not be None!"

        self.matchFields(author2, myAuthor)
        self.printDatum(author2, myAuthor)
        
        db.session.add(myAuthor)
        db.session.commit()
        
        if willQuery is True:

            myAuthors=Authors.query.all()
            self.assertTrue(len(myAuthors) == 1), "Number of records should be 1!"
            self.matchFields(author2, myAuthors[0])
            self.printDatum(author2, myAuthors[0])
        
        if willClear is True:

            if willQuery is True:
                db.session.delete(myAuthors[0])
            else:
                db.session.delete(myAuthor)
            
            db.session.commit()



    def SaveAllToDB(self):

        for author in authors:
            myAuthor=Authors(author)
            db.session.add(myAuthor)

        db.session.commit()



    def test_query(self):

        self.SaveAllToDB()

        myAuthor=Authors.query.get(1)
        self.matchFields(author1, myAuthor)
        
        myAuthor=Authors.query.get(2)
        self.matchFields(author2, myAuthor)

        myAuthor=Authors.query.get(3)
        self.matchFields(author3, myAuthor)

        myAuthor=Authors.query.get(4)
        self.matchFields(author4, myAuthor)

        db.session.query(Authors).delete()
        db.session.commit()



    def matchFields(self, test_data, ORM_object):

        #In case of empty datum dictionary, ORM object should be None!
        if test_data=={}:
            self.assertTrue(ORM_object == None), "ORM Object should be None!"
            return 

        # If author_id which is the primary key is not present ORM object should be None!
        if "author_id" not in test_data.keys():
            self.assertTrue(ORM_object == None), "ORM Object should be None!"
            return 

        self.assertTrue(ORM_object.author_id == test_data["author_id"]), "ORM object's author_id field doesnt match!"
        self.assertTrue(ORM_object.name == test_data["name"]), "ORM object's name field doesnt Match!"
        self.assertTrue(ORM_object.password == test_data["password"]), "ORM object's password field doesnt Match"
        self.assertTrue(ORM_object.birthdate == test_data["birthdate"]), "ORM object's birthdate field doesnt Match"

        if "address" not in test_data.keys():
            self.assertTrue(ORM_object.address == ""), "ORM object's Address field should be empty string"
        else:
            self.assertTrue(ORM_object.address == test_data["address"]), "ORM object's Address field doesnt match!"

        if "bio" not in test_data.keys():
            self.assertTrue(ORM_object.bio == ""), "ORM object's bio field should be empty"
        else:
            self.assertTrue(ORM_object.bio == test_data["bio"]), "ORM object's bio field doesnt match!"

        if "numberOf_friends" not in test_data.keys():
            self.assertTrue(ORM_object.numberOf_friends == 0), "ORM object's numberOf_friends field should have default value of 0"
        else:
            self.assertTrue(ORM_object.numberOf_friends == test_data["numberOf_friends"]), "ORM object's numberOf_friends field value doesnt match!"

        if "numberOf_followers" not in test_data.keys():
            self.assertTrue(ORM_object.numberOf_followers == 0), "ORM object's numberOf_followers field should have default value of 0"
        else:
            self.assertTrue(ORM_object.numberOf_followers == test_data["numberOf_followers"]), "ORM object's numberOf_followers field value doesnt match!"

        if "numberOf_followees" not in test_data.keys():
            self.assertTrue(ORM_object.numberOf_followees == 0), "ORM object's numberOf_followees field should have default value of 0"
        else:
            self.assertTrue(ORM_object.numberOf_followees == test_data["numberOf_followees"]), "ORM object's numberOf_followees field value doesnt match!"

        if "numberOf_friendRequests" not in test_data.keys():
            self.assertTrue(ORM_object.numberOf_friendRequests == 0), "ORM object's numberOf_friendRequests field should have default value of 0"
        else:
            self.assertTrue(ORM_object.numberOf_friendRequests == test_data["numberOf_friendRequests"]), "ORM object's numberOf_friendRequests field value doesnt match!"



    def printDatum(self, test_data, ORM_object):

        print "test_data for author: "
        print test_data
        print "Corresponding ORM author data below: "
        print "author['author_id'] = " + str(ORM_object.author_id)
        print "author['name'] = " + str(ORM_object.name)
        print "author['login_name'] = " + str(ORM_object.login_name)
        print "author['password'] = " + str(ORM_object.password)
        print "author['address'] = " + str(ORM_object.address)
        print "author['birthdate'] = " + str(ORM_object.birthdate)
        print "author['bio'] = " + str(ORM_object.bio)
        print "author['numberOf_friends'] = " + str(ORM_object.numberOf_friends)
        print "author['numberOf_followers'] = " + str(ORM_object.numberOf_followers)
        print "author['numberOf_followees'] = " + str(ORM_object.numberOf_followees)
        print "author['numberOf_friendRequests'] = " + str(ORM_object.numberOf_friendRequests)


def runTest():
    # unittest.main()
    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_Authors)

    testRunner = unittest.TextTestRunner()
    test_Result = testRunner.run(test_suite)

