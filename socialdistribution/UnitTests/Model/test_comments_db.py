import unittest
from db import db
from sample_data.data1 import *
from Model.Comments import Comments


class test_Comments(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_comment1(self, willClear=True, willQuery=True):
        
        print "Testing comment1..."
        myComment = Comments(comment1)
        
        print comment1
        self.assertTrue(myComment != None), "ORM object should not be None!"
        
        self.matchFields(comment1, myComment)
        self.printDatum(comment1, myComment)
        
        db.session.add(myComment)
        db.session.commit()
        
        if willQuery is True:
            
            myComment=Comments.query.all()
            self.assertTrue(len(myComment) == 1), "Number of records should be 1!"
            self.matchFields(comment1, myComment[0])
            self.printDatum(comment1, myComment[0])
        
        if willClear is True:
            
            if willQuery is True:
                db.session.delete(myComment[0])
            else:
                db.session.delete(myComment)
            
            db.session.commit()



        def test_NoCommentID(self):

            print "Testing comment with empty Datum"
            myComment=Comments(comment_empty)
            self.assertTrue(myComment == None), "ORM object should be none!"



    def test_comment2(self, willClear=True, willQuery=True):
    
        print "Testing comment2..."
        myComment=Comments(comment2)
        self.assertTrue(myComment != None), "ORM object should not be None!"
        
        self.matchFields(comment2, myComment)
        self.printDatum(comment2, myComment)
        
        db.session.add(myComment)
        db.session.commit()
        
        if willQuery is True:
            
            myComment=Comments.query.all()
            self.assertTrue(len(myComment) == 1), "Number of records should be 1!"
            self.matchFields(comment2, myComment[0])
            self.printDatum(comment2, myComment[0])
        
        if willClear is True:
            
            if willQuery is True:
                db.session.delete(myComment[0])
            else:
                db.session.delete(myComment)
        
            db.session.commit()



    def SaveAllToDB(self):
        
        for comment in comments:
            myComment=Comments(comment)
            db.session.add(myComment)
            
        db.session.commit()
        
    
    
    def test_query(self):
        
        self.SaveAllToDB()
        
        myComment=Comments.query.get(1)
        self.matchFields(comment1, myComment)
        
        myComment=Comments.query.get(2)
        self.matchFields(comment2, myComment)


        myComment=Comments.query.get(3)
        self.matchFields(comment3, myComment)

        myComment=Comments.query.get(4)
        self.matchFields(comment4, myComment)


        
        db.session.query(Comments).delete()
        db.session.commit()



    def matchFields(self, test_data, ORM_object):
    
        #In case of empty datum dictionary, ORM object should be None!
        if test_data=={}:
            self.assertTrue(ORM_object == None), "ORM Object should be None!"
            return

        # If author_id which is the primary key is not present ORM object should be None!
        if "comment_id" not in test_data.keys():
            self.assertTrue(ORM_object == None), "ORM Object should be None!"
            return
        
        print "test Test TEST"
        print ORM_object
        print str(test_data["comment_text"])
        
        self.assertTrue(ORM_object.comment_id == test_data["comment_id"]),

        self.assertTrue(ORM_object.post_id == test_data["post_id"]), "ORM object's author_id field doesnt match!"
        self.assertTrue(ORM_object.comment_text == test_data["comment_text"]), "ORM object's password field doesnt Match"
        self.assertTrue(ORM_object.creation_time == test_data["creation_time"]), "ORM object's birthdate field doesnt Match"


    def printDatum(self, test_data, ORM_object):
    
        print "test_data for comments: "
        print test_data
        print "Corresponding ORM comment data below: "
        print "comment['comment_id'] = " + str(ORM_object.comment_id)
        print "comment['post_id'] = " + str(ORM_object.post_id)
        print "comment['comment_text'] = " + str(ORM_object.comment_text)
        print "comment['creation_time'] = " + str(ORM_object.creation_time)

def runTest():
    # unittest.main()
    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_Comments)
    
    testRunner = unittest.TextTestRunner()
    test_Result = testRunner.run(test_suite)

