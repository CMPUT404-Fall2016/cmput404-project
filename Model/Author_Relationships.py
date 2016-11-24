from db import db
from Model.Authors import Authors
from Model.Servers import Servers
from model import *
from sqlalchemy import and_
import uuid

class Author_Relationships(db.Model):
    __tablename__ = 'author_relationships'

    # AuthorRelationship_id = db.Column(db.Integer, primary_key=True)
    AuthorRelationship_id = db.Column(db.String(100), primary_key=True)
    
    authorServer1_id = db.Column(db.Integer)
    
    author1_id = db.Column(db.String(100))
    
    author1_name = db.Column(db.String(60))

    authorServer2_id = db.Column(db.Integer)
    
    author2_id = db.Column(db.String(100))

    author2_name = db.Column(db.String(60))
    
    relationship_type = db.Column(db.Integer) # if 1, author1 is following author 2, if 2 then author2 is following author1, if 3 then both are friends

    # db.PrimaryKeyConstraint(authorServer1_id, author1_id)
    # db.PrimaryKeyConstraint(authorServer2_id, author2_id)


    def __new__(cls, datum=None):

        """
        Input: For datum, see comments in __init__
        
        Description:
            Checks whether the keys are inside datum dictionary.
            If not found, then it returns None 
        """

        # When the DB will query and retrieve objects, __new__ will have to called to create the objects and datum wont be provided
        if datum == None: 
            return super(Author_Relationships, cls).__new__(cls)
        
        if ('AuthorRelationship_id' and 'authorServer1_id' and 'author1_id' and 'authorServer2_id' and 'author2_id' and 'relationship_type') not in datum.keys():
            return None
        else:
            return super(Author_Relationships, cls).__new__(cls)



    def __init__(self, datum=None):
        """
        Input:
            datum is a dictionary with keys as column names and values as their corresponding values.
            eg, datum['author1_id']=3, etc
        
        Description:
            This constructor sets the values of fields based on datum dictionary. If any field
            is missing from datum, its default value will be inserted.

        TODO:

        """
        if datum == None:
            self.AuthorRelationship_id = uuid.uuid4().hex
            return

        self.AuthorRelationship_id = datum['AuthorRelationship_id']
        self.author1_id = datum['author1_id']
        self.author2_id = datum['author2_id']
        self.authorServer1_id = datum['authorServer1_id']
        self.authorServer2_id = datum['authorServer2_id']
        self.relationship_type = datum['relationship_type']
        if "author1_name" in datum.keys():
            self.author1_name = datum["author1_name"]
        if "author2_name" in datum.keys():
            self.author2_name = datum["author2_name"]


    def insert(self):

        """
        Call this method for inserting an Author_Relationships row into the DB. 
        Before inserting, it makes sure that the authors, servers are all present in their respective DB. 
        """
        willInsert = True

        if Authors.query.filter(Authors.author_id == self.author1_id).all() == []:
            willInsert = False

        if Authors.query.filter(Authors.author_id == self.author2_id).all() == []:
            willInsert = False

        if Servers.query.filter(Servers.server_index == self.authorServer1_id).all() == []:
            willInsert = False

        if Servers.query.filter(Servers.server_index == self.authorServer2_id).all() == []:
            willInsert = False

        if willInsert is True:
            db.session.add(self)
            db.session.commit()
            return True #Returns true as it succesfully inserted the row.

        return False #In case insertion failed


    def updateRow(self):

        """
        Call this method to update any changes made to any rows in the DB, such as changing the relationship type.
        """
        self.insert()


    @staticmethod
    def deleteRowsByQuery(query_param):

        """
        Read query method's description for query_param.
        
        This method uses static method query for first retrieving a set of rows that matches the query given in query_param
        and then deletes  
        """
        rows=Author_Relationships.query(query_param)
        if rows==[]:
            return

        for row in rows:
            db.session.delete(row)

        db.session.commit()



    @staticmethod
    def query(query_param):

        """
        query param is a dictionary containing query information.
        
        Types of queries:
        1) query_param['server_author_1']=[server1_obj, author1_obj]
           query_param['server_author_2']=[server2_obj, author2_obj]
 
        2) query_param['server_author_1']=[server1_obj, author1_obj]

        3) query_param['server_author_1']=[server1_obj, author1_obj]
           query_param['relationship_type']=relationship_type value

        4) query_param['server_author_2']=[server2_obj, author2_obj]

        5) query_param['server_author_2']=[server2_obj, author2_obj]
           query_param['relationship_type']=relationship_type value

        6) query_param['relationship_type']=relationship_type value

        7) query_param={} // This gives back all the rows

        8) query_param["author_ids"]=[author1_id, author2_id] #Add test later

        9) query_param["server_author_id1"]=[server1_index, author1_id, type]

        10) query_param["server_author_id2"]=[server2_index, author2_id, type]

        11) query_param["server_author_id1"]=[server1_index, author1_id]
            query_param["server_author_id2"]=[server2_index, author2_id]

        """

        
        if query_param=={}:
            return db.session.query(Author_Relationships).all()


        if "areFollowers" in query_param.keys():
            author1_id, author2_id = query_param["areFollowers"]
            results=db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == author1_id,
                                                                  Author_Relationships.author2_id == author2_id,
                                                                  Author_Relationships.relationship_type == 1
                                                                  ).all()

            results=db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == author1_id,
                                                                  Author_Relationships.author2_id == author2_id,
                                                                  Author_Relationships.relationship_type == 2
                                                                  ).all()

            return results

        if "areFriends" in query_param.keys():
            author1_id, author2_id = query_param["areFriends"]
            results=db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == author1_id,
                                                                  Author_Relationships.author2_id == author2_id,
                                                                  Author_Relationships.relationship_type == 3
                                                                  ).all()

            return results


        if "server_author_id1" in query_param.keys() and "server_author_id2" in query_param.keys():
            server1_id, author1_id = query_param["server_author_id1"]
            server2_id, author2_id = query_param["server_author_id2"]
            results=db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == author1_id,
                                                                  Author_Relationships.author2_id == author2_id,
                                                                  Author_Relationships.authorServer1_id == server1_id,
                                                                  Author_Relationships.authorServer2_id == server2_id,
                                                                  ).all()

            print "printing all!"
            print db.session.query(Author_Relationships).all()
            return results


        if "server_author_id1" in query_param.keys():
            server1_id, author1_id, relationship_type = query_param["server_author_id1"]
            results=db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == author1_id,
                                                                  Author_Relationships.authorServer1_id == server1_id,
                                                                  Author_Relationships.relationship_type == relationship_type
                                                                  ).all()

            return results


        if "server_author_id2" in query_param.keys():
            server2_id, author2_id, relationship_type = query_param["server_author_id2"]
            results=db.session.query(Author_Relationships).filter(Author_Relationships.author2_id == author2_id,
                                                                  Author_Relationships.authorServer2_id == server2_id,
                                                                  Author_Relationships.relationship_type == relationship_type
                                                                  ).all()

            return results


        if "server_author_1" and "server_author_2" in query_param.keys():
            server1, author1 = query_param["server_author_1"]
            server2, author2 = query_param["server_author_2"]
            results=db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == author1.author_id,
                                                                  Author_Relationships.author2_id == author2.author_id,
                                                                  Author_Relationships.authorServer1_id == server1.server_index,
                                                                  Author_Relationships.authorServer2_id == server2.server_index
                                                                  ).all()

            return results

        
        ###### For querying with author1

        if "server_author_1" in query_param.keys():
            server1, author1 = query_param["server_author_1"]

            if "relationship_type" in query_param.keys():
                
                relationship_type=query_param["relationship_type"]
                results=db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == author1.author_id,
                                                                      Author_Relationships.authorServer1_id == server1.server_index,
                                                                      Author_Relationships.relationship_type == relationship_type
                                                                      ).all()

            else:

                results=db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == author1.author_id,
                                                                      Author_Relationships.authorServer1_id == server1.server_index,
                                                                      ).all()

            return results


        ###### For querying with author2

        if "server_author_2" in query_param.keys():
            server2, author2 = query_param["server_author_2"]

            if "relationship_type" in query_param.keys():
                
                relationship_type=query_param["relationship_type"]
                results=db.session.query(Author_Relationships).filter(Author_Relationships.author2_id == author2.author_id,
                                                                      Author_Relationships.authorServer2_id == server2.server_index,
                                                                      Author_Relationships.relationship_type == relationship_type
                                                                      ).all()

            else:

                results=db.session.query(Author_Relationships).filter(Author_Relationships.author2_id == author2.author_id,
                                                                      Author_Relationships.authorServer2_id == server2.server_index,
                                                                      ).all()

            return results


        ###### For a given relationship_type get all the rows.
        if "relationship_type" in query_param.keys():
    
            relationship_type=query_param["relationship_type"]
            results=db.session.query(Author_Relationships).filter(Author_Relationships.relationship_type == relationship_type
                                                                  ).all()

            return results


        print "returning None"
        return None
    # _ANS = query.__func__()
