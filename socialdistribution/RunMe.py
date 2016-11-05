import init_location 
from model import *
import UnitTests.Model.test_Authors_db as test_Authors_db
import UnitTests.Model.test_comments_db as test_comments_db
import UnitTests.Model.test_Post_db as test_Post_db
import UnitTests.Model.test_Images_db as test_Images_db
import UnitTests.Model.test_URL_db as test_URL_db
import UnitTests.Model.test_Friend_Requests_db as test_Friend_Requests_db
import UnitTests.Model.test_Author_Relationships_db as test_Author_Relationships_db 
import UnitTests.Model.test_Servers_db as test_Servers_db
import Server.main


def runServer():
	Server.main.run()

def runTests():
	test_Authors_db.runTest()
	DELETE_ALL()
	test_Post_db.runTest()
	DELETE_ALL()
	test_comments_db.runTest()
	DELETE_ALL()
	test_Images_db.runTest()
	DELETE_ALL()
	test_URL_db.runTest()
	DELETE_ALL()
	test_Friend_Requests_db.runTest()
	DELETE_ALL()
	test_Author_Relationships_db.runTest()
	DELETE_ALL()
	test_Servers_db.runTest()
	DELETE_ALL()


if __name__=="__main__":
	runServer()
