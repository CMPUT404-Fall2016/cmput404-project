from db import db

from Model.Author_Relationships import Author_Relationships
from Model.Authors import Authors
from Model.Comments import Comments
from Model.Friend_Requests import Friend_Requests
from Model.Images import Images
from Model.Posts import Posts
from Model.Servers import Servers
from Model.URL import URL


"""
__App_state is a global variable that contains important information about the state of the server. 

__App_state['no_friend_Requests'] : Number of friend requests send to this server. Used for id'ing friend requests
(MAYBE) ** __App_state['no_Authors'] : Number of Authors created on the server so far. Used for id'ing the authors **
"""
__App_state = {}
db.create_all()

def DELETE_ALL():
	db.session.query(Author_Relationships).delete()
	db.session.query(Authors).delete()
	db.session.query(Comments).delete()
	db.session.query(Friend_Requests).delete()
	db.session.query(Images).delete()
	db.session.query(Posts).delete()
	db.session.query(Servers).delete()
	db.session.query(URL).delete()


def loadAppState():
	pass

def saveAppState():
	pass








