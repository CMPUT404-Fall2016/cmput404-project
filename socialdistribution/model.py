from .db import db

class Authors(db.Model):
    #    __tablename__ = 'users'
    
    author_id = Column(db.Integer, primary_key=True)
    
    name = Column(db.String(60))
    
    login_name = Column(db.String(60), unique=True)
    
    password = Column(db.String(100))
    
    address = Column(db.String(100))
    
    birthdate = Column(db.DateTime)
    
    bio = Column(db.String(200))
    
    numberOf_friends = Column(db.Integer)
    
    numberOf_followers = Column(db.Integer)
    
    numberOf_followees = Column(db.Integer)
    
    numberOf_friendRequests = Column(db.Integer)
    
    
    
    def __init__(self, login_name, password):
        self.login_name = login_name
        self.password = password
    
    def __repr__(self):
        return '<User %r>' % (self.login_name)

class Author_Relationships(db.Model):

    Author_Relationships = Column(db.Integer, primary_key=True)
    
    authorServer1_id = Column(db.Integer, unique= True)
    
    author1_id = Column(db.Integer, unique = True, db.ForignKey('Authors.author_id'))
    
    authorServer2_id = Column(db.Integer, unique=True)
    
    author2_id = Column(db.Integer, unique=True,db.ForignKey('Authors.author_id'))
    
    relationship_type = Column(db.Integer)


class Friend_Requests(db.Model):
    
    friendrequests = Column(db.Integer, unique=True, primary_key = True)
    
    fromAuthor_id = Column(db.Integer, unique=True, db.ForignKey('Authors.author_id'))
    
    fromAuthorServer_index = Column(db.Integer, unique=True)
    
    toAuthor_id = Column(db.Integer, unique=True, db.ForignKey('Authors.author_id'))
    
    toAuthorServer_index = Column(db.Integer, unique=True)
    
    isChecked = Column(db.Boolean)


class Server(db.Model):

    server_id = Column(db.BigInteger, unique=True, primary_key=True)
    IP = Column(db.String(128), unique=True)
    server_index = Column(db.Integer)


class Post(db.Model):

    post_id = Column(db.Integer, unique=True, primary_key=True)
    
    title = Column(db.String(64))
    
    text = Column(db.String(800))
    
    creation_time = Column(db.DateTime)
    
    view_permission = Column(db.Integer)
    
    post_type = Column(db.Integer)
    
    numberOf_comments = Column(db.Integer)
    
    numberOf_URL = Column(db.Integer)
    
    numberOf_images = Column(db.Integer)



class Comments(db.Model):

    comment_id = Column(db.Integer, primary_key=True)
    
    post_id = Column(db.Integer, unique=True, db.ForignKey('post.post_id'))
    
    comment_text = Column(db.String(800))
    
    creation_time = Column(db.DateTime)


class Images(db.Model):

    image_id = Column(db.Integer, unique=True, primary_key=True)
    
    post_id = Column(db.Integer, unique=True, db.ForignKey('Post.post_id'))
    
    comment_id = Column(db.Integer, db.ForignKey('Comments.comment_id'))
    
    image = Column(db.LargeBinary)


class URL(db.Model):
    
    URL_id = Column(db.Integer, unique=True, primary_key=True)
    
    post_id = Column(db.Integer, unique=True, db.ForignKey('Post.post_id'))
    
    comment_id = Column(db.Integer, db.ForignKey('Comments.comment_id'))
    
    URL_link = Column(db.String(2048))
    
    URL_type = Column(db.Integer)
