import unittest
from db import db
from sample_data.data1 import *
from Model.Servers import Servers


class test_Servers(unittest.TestCase):

    def setUp(self):
        pass


    def SaveAllToDB(self):

        # print servers
        for server in servers:
            # print(server, it)
            myServer=Servers(server)
            self.matchFields(server, myServer)
            self.assertTrue(myServer != None), server
            db.session.add(myServer)

        db.session.commit()



    def test_emptyServer(self):

        myServer=Servers(server_empty)
        self.matchFields(server_empty, myServer)



    def test_Servers(self):

        self.SaveAllToDB()
        myServers=Servers.query.filter_by(server_index=1).all()
        self.assertTrue(len(myServers) == 1), "Query should return one server/row!"
        self.matchFields(server1, myServers[0])

        myServers=Servers.query.filter_by(server_index=2).all()
        self.assertTrue(len(myServers) == 1), "Query should return one server/row!"
        self.matchFields(server2, myServers[0])

        myServers=Servers.query.filter_by(server_index=3).all()
        self.assertTrue(len(myServers) == 1), "Query should return one server/row!"
        self.matchFields(server3, myServers[0])

        db.session.query(Servers).delete()
        db.session.commit()



    def matchFields(self, test_data, ORM_object):

        if ('server_id' and 'IP' and 'server_index') not in test_data.keys():
            self.assertTrue(ORM_object == None), "ORM object should be none!"
            return 
        else:
            self.assertTrue(ORM_object != None), "ORM object should not be none!"

        self.assertTrue(ORM_object.server_id == test_data['server_id']), "ORM object's server_id field's value mismatched!"
        self.assertTrue(ORM_object.IP == test_data['IP']), "ORM object's IP field's value mismatched!"
        self.assertTrue(ORM_object.server_index == test_data['server_index']), "ORM object's server_index field's value mismatched!"


    def printDatum(self, test_data, ORM_object):

        print test_data
        print "Below is the ORM object"
        print "ORM_object['server_id'] =" +str(ORM_object.server_id)
        print "ORM_object['IP'] =" +str(ORM_object.IP)
        print "ORM_object['server_index'] =" +str(ORM_object.server_index)


def runTest():
    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_Servers)

    testRunner = unittest.TextTestRunner()
    test_Result = testRunner.run(test_suite)

