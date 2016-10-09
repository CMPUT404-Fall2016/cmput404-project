# from .db import db

class Servers(db.Model):

    server_id = Column(db.BigInteger, unique=True, primary_key=True)

    IP = Column(db.String(128), unique=True)
    
    server_index = Column(db.Integer)
