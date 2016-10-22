import unittest
from db import db
from sample_data.data1 import *
from Model.URL import URL

'''
	Testing URLs Model

'''
class test_URLs(unittest.TestCase):

	def setUp(self):
		#self.os = OS()
		pass


	def tearDown(self):
		pass


	def test_Add(self):
		print "Testing Adding URLs"
		count = 1
		for url in urls:
			myurl = URL(url)
			db.session.add(myurl)
			db.session.commit
			rows = db.session.query(URL).count()
			self.assertTrue(rows == count, "Adding Failure")
			count += 1



	def test_Added(self):
		print "Testing Added URLs"
		for i in range(4):
			spec = urls[i]
			orm = URL.query.get(i+1)
			#Bad Style. Should Loop Through Keys And Use A Loop
			self.assertTrue(spec["URL_id"] == orm.URL_id, "Wrong URL")
			self.assertTrue(spec["post_id"] == orm.post_id, "Wrong URL")
			self.assertTrue(spec["comment_id"] == orm.comment_id, "Wrong URL")
			self.assertTrue(spec["URL_link"] == orm.URL_link, "Wrong URL")
			self.assertTrue(spec["URL_type"] == orm.URL_type, "Wrong URL")


	def test_Delete(self):
		print "Testing Delete URLs"
		url = URL({"URL_id" : 5, "post_id": 50, "comment_id" : 500, "URL_link": "wtf", "URL_type": 5})	
		db.session.add(url)
		db.session.commit()
		db.session.delete(url)
		db.session.commit()	
		rows = db.session.query(URL).count()
		self.assertTrue(rows == 4, "Deletion Failure")



	# Test Setter
	def test_ModLink(self):
		link = "facebook.com"
		print "Testing Modify URLs"
		url = db.session.query(URL).get(1)
		url.set_link(link)
		self.assertTrue(url.URL_link == link, "Modification Failed")
		
		


def runTest():
    # unittest.main()
    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_URLs)

    testRunner = unittest.TextTestRunner()
    test_Result = testRunner.run(test_suite)

