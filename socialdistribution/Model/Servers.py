from db import db

class Servers(db.Model):

    __tablename__ = 'servers'

    server_id = db.Column(db.BigInteger, primary_key=True)

    IP = db.Column(db.String(40), unique=True)
    
    server_index = db.Column(db.Integer, unique=True)


    def __new__(cls, datum=None):

    #     """
    #     Input: For datum, see comments in __init__
        
    #     Description:
    #         Checks whether the keys for column names are inside datum dictionary.
    #         If not found, then it returns None 
    #     """

        # When the DB will query and retrieve objects, __new__ will have to called to create the objects and datum wont be provided
        if datum == None:
            return super(Servers, cls).__new__(cls)

        if ('server_id' and 'IP' and 'server_index') not in datum.keys():
            return None
        else:
            return super(Servers, cls).__new__(cls)

    
    def __init__(self, datum=None):
        """
        Input:
            datum is a dictionary with keys as column names and values as their corresponding values.
            eg, datum['server_index']=3, etc
        
        Description:
            This constructor sets the values of fields based on datum dictionary. If any field
            is missing from datum, its default value will be inserted.

        TODO:

        """
        if datum == None:
            self.server_id = uuid.uuid4().hex
            return

        self.server_id = datum['server_id']
        self.IP = datum['IP']
        self.server_index = datum['server_index']


