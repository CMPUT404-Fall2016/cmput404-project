import unittest
from sample_data.data1 import *

class test_Authors(unittest.TestCase):

	def test1(self):
		self.assertTrue(author1["author_id"]==1), "Assertion error"

	def test_NoAuthorID(self):
		pass

def runTest():
	unittest.main()

