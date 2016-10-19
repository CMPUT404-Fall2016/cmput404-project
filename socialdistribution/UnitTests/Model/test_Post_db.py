import unittest
from db import db
from sample_data.data1 import *
from Model.Posts import Posts






class test_Posts(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_post1(self, willClear=True, willQuery=True):
        
        print "Testing post..."
        
        
        myPost = Posts(post1)
        
        #myPost=Posts.query.get(3)
        
        print post1
        
        self.assertTrue(myPost != None), "ORM object should not be None!"
        
        self.matchFields(post1, myPost)
        self.printDatum(post1, myPost)
        
        db.session.add(myPost)
        db.session.commit()
        
        if willQuery is True:
            
            myPosts=Posts.query.all()
            self.assertTrue(len(myPosts) == 1), "Number of records should be 1!"
            self.matchFields(post1, myPosts[0])
            self.printDatum(post1, myPosts[0])
        
        if willClear is True:
            
            if willQuery is True:
                db.session.delete(myPosts[0])
            else:
                db.session.delete(myPost)
            
            db.session.commit()



    def test_NoPostID(self):
        
        print "Testing post with empty Datum"
        myPost=Posts(post_empty)
        self.assertTrue(myPost == None), "ORM object should be none!"
        
        
    
    def test_post2(self, willClear=True, willQuery=True):
        
        print "Testing post2..."
        myPost=Posts(post2)
        self.assertTrue(myPost != None), "ORM object should not be None!"
        
        self.matchFields(post2, myPost)
        self.printDatum(post2, myPost)
        
        db.session.add(myPost)
        db.session.commit()
        
        if willQuery is True:
            
            myPosts=Posts.query.all()
            self.assertTrue(len(myPosts) == 1), "Number of records should be 1!"
            self.matchFields(post2, myPosts[0])
            self.printDatum(post2, myPosts[0])
    
        if willClear is True:
            
            if willQuery is True:
                db.session.delete(myPosts[0])
            else:
                db.session.delete(myPost)
            
            db.session.commit()



    def SaveAllToDB(self):
        
        for post in posts:
            myPost=Posts(post)
            db.session.add(myPost)
            
        db.session.commit()
        
    
    
    def test_query(self):
        
        self.SaveAllToDB()
        
        myPost=Posts.query.get(1)
        self.matchFields(post1, myPost)
        
        myPost=Posts.query.get(2)
        self.matchFields(post2, myPost)
        
        myPosts=Posts.query.get(3)
        self.matchFields(post3, myPost)
        
        myPost=Posts.query.get(4)
        self.matchFields(post4, myPost)
        
        db.session.query(Posts).delete()
        db.session.commit()



    def matchFields(self, test_data, ORM_object):

        #In case of empty datum dictionary, ORM object should be None!
        if test_data=={}:
            self.assertTrue(ORM_object == None), "ORM Object should be None!"
            return

        # If author_id which is the primary key is not present ORM object should be None!
        if "post_id" not in test_data.keys():
            self.assertTrue(ORM_object == None), "ORM Object should be None!"
            return

        print ORM_object
        
        self.assertTrue(ORM_object.post_id == test_data["post_id"]), "ORM object's author_id field doesnt match!"
        self.assertTrue(ORM_object.title == test_data["title"]), "ORM object's name field doesnt Match!"
        self.assertTrue(ORM_object.text == test_data["text"]), "ORM object's password field doesnt Match"
        self.assertTrue(ORM_object.creation_time == test_data["creation_time"]), "ORM object's birthdate field doesnt Match"

        self.assertTrue(ORM_object.author_id == test_data["author_id"]),


        if "view_permission" not in test_data.keys():
            self.assertTrue(ORM_object.view_permission == 0), "ORM object's numberOf_friends field should have default value of 0"
        else:
            self.assertTrue(ORM_object.view_permission == test_data["view_permission"]), "ORM object's numberOf_friends field value doesnt match!"

        if "post_type" not in test_data.keys():
            self.assertTrue(ORM_object.post_type == 0), "ORM object's numberOf_followers field should have default value of 0"
        else:
            self.assertTrue(ORM_object.post_type == test_data["post_type"]), "ORM object's numberOf_followers field value doesnt match!"

        if "numberOf_comments" not in test_data.keys():
            self.assertTrue(ORM_object.numberOf_comments == 0), "ORM object's numberOf_followees field should have default value of 0"
        else:
            self.assertTrue(ORM_object.numberOf_comments == test_data["numberOf_comments"]), "ORM object's numberOf_followees field value doesnt match!"

        if "numberOf_URL" not in test_data.keys():
            self.assertTrue(ORM_object.numberOf_URL == 0), "ORM object's numberOf_friendRequests field should have default value of 0"
        else:
            self.assertTrue(ORM_object.numberOf_URL == test_data["numberOf_URL"]), "ORM object's numberOf_friendRequests field value doesnt match!"

        if "numberOf_images" not in test_data.keys():
            self.assertTrue(ORM_object.numberOf_images == 0), "ORM object's numberOf_friendRequests field should have default value of 0"
        else:
            self.assertTrue(ORM_object.numberOf_images == test_data["numberOf_images"]), "ORM object's numberOf_friendRequests field value doesnt match!"


    def printDatum(self, test_data, ORM_object):

        print "test_data for post: "
        print test_data
        print "Corresponding ORM post data below: "
        print "post['author_id'] = " + str(ORM_object.author_id)
        print "post['post_id'] = " + str(ORM_object.post_id)
        print "post['title'] = " + str(ORM_object.title)
        print "post['text'] = " + str(ORM_object.text)
        print "post['creation_time'] = " + str(ORM_object.creation_time)
        print "post['view_permission'] = " + str(ORM_object.view_permission)
        print "post['post_type'] = " + str(ORM_object.post_type)
        print "post['numberOf_comments'] = " + str(ORM_object.numberOf_comments)
        print "post['numberOf_URL'] = " + str(ORM_object.numberOf_URL)
        print "post['numberOf_images'] = " + str(ORM_object.numberOf_images)


def runTest():
    # unittest.main()
    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_Posts)
    
    testRunner = unittest.TextTestRunner()
    test_Result = testRunner.run(test_suite)

