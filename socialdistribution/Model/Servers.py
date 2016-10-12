from .db import db

class Servers(db.Model):

    server_id = Column(db.BigInteger, primary_key=True)

    IP = Column(db.String(128), unique=True)
    
    server_index = Column(db.Integer, unique=True)


    def __new__(cls, datum):

        """
        Input: For datum, see comments in __init__
        
        Description:
            Checks whether the keys for column names are inside datum dictionary.
            If not found, then it returns None 
        """
        
        if 'server_id' or 'IP' or 'server_index' not in datum.keys():
            return None
        else:
            return super(Servers, cls).__new__(cls)

    
    def __init__(self, datum):
        """
        Input:
            datum is a dictionary with keys as column names and values as their corresponding values.
            eg, datum['server_index']=3, etc
        
        Description:
            This constructor sets the values of fields based on datum dictionary. If any field
            is missing from datum, its default value will be inserted.

        TODO:

        """

        server_id = datum['server_id']
        IP = datum['IP']
        server_index = datum['server_index']
