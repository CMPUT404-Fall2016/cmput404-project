from db import db

class Author_Relationships(db.Model):

    AuthorRelationship_id = Column(db.Integer, primary_key=True)
    
    authorServer1_id = Column(db.Integer)
    
    author1_id = Column(db.Integer)
    
    authorServer2_id = Column(db.Integer)
    
    author2_id = Column(db.Integer)
    
    relationship_type = Column(db.Integer)

    ForeignKeyConstraint([authorServer1_id, author1_id],['Servers.server_index', 'Authors.author_id'])
    ForeignKeyConstraint([authorServer2_id, author2_id],['Servers.server_index', 'Authors.author_id'])


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


    
    def __init__(self, datum):
        """
        Input:
            datum is a dictionary with keys as column names and values as their corresponding values.
            eg, datum['author1_id']=3, etc
        
        Description:
            This constructor sets the values of fields based on datum dictionary. If any field
            is missing from datum, its default value will be inserted.

        TODO:

        """

        self.AuthorRelationship_id = datum['AuthorRelationship_id']
        self.author1_id = datum['author1_id']
        self.author2_id = datum['author2_id']
        self.authorServer1_id = datum['authorServer1_id']
        self.authorServer2_id = datum['authorServer2_id']
        self.relationship_type = datum['relationship_type']

