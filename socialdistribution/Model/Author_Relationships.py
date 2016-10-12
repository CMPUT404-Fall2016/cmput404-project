from .db import db

class Author_Relationships(db.Model):

    AuthorRelationship_id = Column(db.Integer, primary_key=True)
    
    authorServer1_id = Column(db.Integer)
    
    author1_id = Column(db.Integer)
    
    authorServer2_id = Column(db.Integer)
    
    author2_id = Column(db.Integer)
    
    relationship_type = Column(db.Integer)

    ForeignKeyConstraint([authorServer1_id, author1_id],['Servers.server_index', 'Authors.author_id'])
    ForeignKeyConstraint([authorServer2_id, author2_id],['Servers.server_index', 'Authors.author_id'])


    def __new__(cls, datum):

        """
        Input: For datum, see comments in __init__
        
        Description:
            Checks whether the keys are inside datum dictionary.
            If not found, then it returns None 
        """
        
        if 'AuthorRelationship_id' or 'authorServer1_id' or 'author1_id' or 'authorServer2_id' or 'author2_id' or 'relationship_type' not in datum.keys():
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

        AuthorRelationship_id = datum['AuthorRelationship_id']
        author1_id = datum['author1_id']
        author2_id = datum['author2_id']
        authorServer1_id = datum['authorServer1_id']
        authorServer2_id = datum['authorServer2_id']
        relationship_type = datum['relationship_type']

