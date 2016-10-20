import unittest
from db import db
from sample_data.data1 import *
from Model.Images import Images

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
			rows = db.session.query(url).count()
			self.assertTrue(rows == count, "Adding Failure")
			count += 1



	def test_Added(self):
		print "Testing Added Images"
		for i in range(4):
			spec = images[i]
			orm = Images.query.get(i+1)
			#Bad Style. Should Loop Through Keys And Use A Loop
			self.assertTrue(spec["image_id"] == orm.image_id, "Wrong Image")
			self.assertTrue(spec["post_id"] == orm.post_id, "Wrong Image")
			self.assertTrue(spec["comment_id"] == orm.comment_id, "Wrong Image")
			self.assertTrue(spec["image"] == orm.image, "Wrong Image")


	def test_Delete(self):
		print "Testing Delete Images"
		blob = os.urandom(10000)
		img = Images({"image_id" : 5, "post_id": 50, "comment_id" : 500, "image": blob})	
		db.session.add(img)
		db.session.commit()
		db.session.delete(img)
		db.session.commit()	
		rows = db.session.query(Images).count()
		self.assertTrue(rows == 4, "Deletion Failure")



	# Test Setter
	def test_ModLink(self):
		link = ""
		print "Testing Modify URLs"
		url = db.session.query(URL).get(1)
		url.set_link(link)
		self.assertTrue(url.link == link, "Modification Failed")
		
		


def runTest():
    # unittest.main()
    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_URL)

    testRunner = unittest.TextTestRunner()
    test_Result = testRunner.run(test_suite)

