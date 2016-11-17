from db import db
from Model.Authors import Authors
from Model.Servers import Servers
from model import *

class Friend_Requests(db.Model):

    __tablename__ = 'friend_requests'
    
    friendrequests_id = db.Column(db.String(33), unique=True, primary_key = True)
    
    fromAuthor_id = db.Column(db.String(33))
    
    fromAuthorServer_id = db.Column(db.Integer)

    fromAuthorDisplayName = db.Column(db.String(60))
    
    toAuthor_id = db.Column(db.String(33))
    
    toAuthorServer_id = db.Column(db.Integer)
    
    isChecked = db.Column(db.Boolean)


    db.PrimaryKeyConstraint(fromAuthorServer_id, fromAuthor_id)
    db.PrimaryKeyConstraint(toAuthorServer_id, toAuthor_id)


    def __new__(cls, datum=None):

        """
        Input: For datum, see comments in __init__
        
        Description:
            Checks whether the keys are inside datum dictionary.
            If not found, then it returns None 
        """

        # When the DB will query and retrieve objects, __new__ will have to called to create the objects and datum wont be provided
        if datum == None: 
            return super(Friend_Requests, cls).__new__(cls)
        
        if ('friendrequests_id' and 'fromAuthor_id' and 'fromAuthorServer_id' and 'toAuthor_id' and 'toAuthorServer_id' and 'isChecked') not in datum.keys():
            return None
        else:
            return super(Friend_Requests, cls).__new__(cls)


    def __init__(self, datum=None):

        """
        Input:
            datum is a dictionary with keys as column names and values as their corresponding values.
            eg, datum['isChecked']=False, etc
        
        Description:
            This constructor sets the values of fields based on datum dictionary. If any field
            is missing from datum, its default value will be inserted.

        TODO:

        """
        if datum == None:
            self.friendrequests_id = uuid.uuid4().hex
            return


        self.friendrequests_id = datum['friendrequests_id']
        self.fromAuthor_id = datum['fromAuthor_id']
        self.fromAuthorServer_id = datum['fromAuthorServer_id']
        self.toAuthor_id = datum['toAuthor_id']
        self.toAuthorServer_id = datum['toAuthorServer_id']
        self.isChecked = datum['isChecked']
        if "fromAuthorDisplayName" in datum.keys():
            self.fromAuthorDisplayName = datum["fromAuthorDisplayName"]


    def insert(self):
        """
        Call this method to save an instance of this class into the DB.
        TODO: This may need to change depending on the full specifications.
        """
        db.session.add(self)
        db.session.commit()
        return True


    def updateRow(self):

        """
        Call this method to update any changes made to any rows in the DB, such as changing the relationship type.
        """
        self.insert()



    @staticmethod
    def query(query_param):
        """
        query param is a dictionary containing query information.
        
        Types of queries:

        1) query_param={} // This gives back all the rows

        2) query_param['friendrequests_id']=[friendrequests_id]

        3) query_param['sendTo']=[toAuthorServer_id, toAuthor_id]

        4) query_param['sendFrom']=[fromAuthorServer_id, fromAuthor_id]

        5) query_param['sendTo']=[toAuthorServer_id, toAuthor_id]
           query_param['sendFrom']=[fromAuthorServer_id, fromAuthor_id]        
        
        """

        if query_param=={}:
            return db.session.query(Friend_Requests).all()


        if 'friendrequests_id' in query_param.keys():

            friendrequests_id = query_param['friendrequests_id']
            results=db.session.query(Friend_Requests).filter(Friend_Requests.friendrequests_id == friendrequests_id,
                                                             ).all()
            return results


        if ('sendTo' in query_param.keys()) and ('sendFrom' in query_param.keys()) :

            toAuthorServer_id, toAuthor_id = query_param['sendTo']
            fromAuthorServer_id, fromAuthor_id = query_param['sendFrom']
            results=db.session.query(Friend_Requests).filter(Friend_Requests.toAuthor_id == toAuthor_id,
                                                             Friend_Requests.toAuthorServer_id == toAuthorServer_id,
                                                             Friend_Requests.fromAuthor_id == fromAuthor_id,
                                                             Friend_Requests.fromAuthorServer_id == fromAuthorServer_id
                                                             ).all()
            return results

        if 'sendTo' in query_param.keys():

            toAuthorServer_id, toAuthor_id = query_param['sendTo']
            results=db.session.query(Friend_Requests).filter(Friend_Requests.toAuthor_id == toAuthor_id,
                                                             Friend_Requests.toAuthorServer_id == toAuthorServer_id
                                                             ).all()
            return results


        if 'sendFrom' in query_param.keys():

            fromAuthorServer_id, fromAuthor_id = query_param['sendFrom']
            results=db.session.query(Friend_Requests).filter(Friend_Requests.fromAuthor_id == fromAuthor_id,
                                                             Friend_Requests.fromAuthorServer_id == fromAuthorServer_id
                                                             ).all()
            return results



    @staticmethod
    def deleteRowsByQuery(query_param):

        """
        Read query method's description for query_param.
        
        This method uses static method query for first retrieving a set of rows that matches the query given in query_param
        and then deletes  
        """
        rows=Friend_Requests.query(query_param)
        if rows==[]:
            return

        for row in rows:
            db.session.delete(row)

        db.session.commit()

