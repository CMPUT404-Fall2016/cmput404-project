# from .db import db

class Authors(db.Model):
    #    __tablename__ = 'users'
    
    author_id = Column(db.Integer, primary_key=True)
    
    name = Column(db.String(60))
    
    login_name = Column(db.String(60), unique=True)
    
    password = Column(db.String(30))
    
    address = Column(db.String(100))
    
    birthdate = Column(db.DateTime)
    
    bio = Column(db.String(200))
    
    numberOf_friends = Column(db.Integer)
    
    numberOf_followers = Column(db.Integer)
    
    numberOf_followees = Column(db.Integer)
    
    numberOf_friendRequests = Column(db.Integer)
    
    
    def __new__(cls, datum):

        """
        Input: See comments in __init__
        
        Description:
            Checks whether author_id is inside datum dictionary.
            If not found, then it returns None 
        """
        if 'author_id' not in datum.keys():
            return None
        else:
            return super(Authors, cls).__new__(cls)

    
    def __init__(self, datum):
        """
        Input:
            datum is a dictionary with keys as column names and values as their corresponding values.
            eg, datum['author_id']=3, datum['name']=touqir, datum['password']="123456"
        
        Description:
            This constructor sets the values of fields based on datum dictionary. If any field
            is missing from datum, its default value will be inserted.

        TODO:
            * What to do about default birthdate??
        """

        empty_string=""

        self.author_id = datum["author_id"]

        if "name" in datum.keys():
            self.name = datum["name"]

        if "login_name" in datum.keys():
            self.login_name = datum["login_name"]

        if "password" in datum.keys():
            self.password = datum["password"]

        if "address" in datum.keys():
            self.address = datum["address"]
        else:
            self.address = empty_string

        if "birthdate" in datum.keys():
            self.birthdate = datum["birthdate"]

        if "bio" in datum.keys():
            self.bio = datum["bio"]

        if "numberOf_friends" in datum.keys():
            self.numberOf_friends = datum["numberOf_friends"]
        else:
            self.numberOf_friends = 0

        if "numberOf_followers" in datum.keys():
            self.numberOf_followers = datum["numberOf_followers"]
        else:
            self.numberOf_followers = 0

        if "numberOf_followees" in datum.keys():
            self.numberOf_followees = datum["numberOf_followees"]
        else:
            self.numberOf_followees = 0

        if "numberOf_friendRequests" in datum.keys():
            self.numberOf_friendRequests = datum["numberOf_friendRequests"]
        else:
            self.numberOf_friendRequests = 0


    def __repr__(self):
        return '<User %r>' % (self.login_name)
