import init_location 
import UnitTests.Model.test_Authors_db as test_Authors_db
import UnitTests.Model.test_comments_db as test_comments_db
import UnitTests.Model.test_Post_db as test_Post_db
import UnitTests.Model.test_Images_db as test_Images_db
import UnitTests.Model.test_URL_db as test_URL_db


if __name__=="__main__":

	test_Authors_db.runTest()
	test_Post_db.runTest()
	test_comments_db.runTest()
	test_Images_db.runTest()
	test_URL_db.runTest()
