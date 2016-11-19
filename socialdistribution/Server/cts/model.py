from db import db
import uuid

from Model.Author_Relationships import Author_Relationships
from Model.Authors import Authors
from Model.Comments import Comments
from Model.Friend_Requests import Friend_Requests
from Model.Images import Images
from Model.Posts import Posts
from Model.Servers import Servers
from Model.URL import URL
from sample_data.data1 import *


"""
APP_state is a global variable that contains important information about the state of the server. 

APP_state['no_friend_Requests'] : Number of friend requests send to this server. Used for id'ing friend requests
(MAYBE) ** APP_state['no_Authors'] : Number of Authors created on the server so far. Used for id'ing the authors **
"""
APP_state = {}
APP_state["session_ids"]={}
APP_state["session_ids"]["123"] = "Randy"
APP_state["no_servers"] = 0
APP_state["admin_credentials"] = None
APP_state["shared_nodes"] = []
APP_state["shared_nodes_images"] = []
APP_state["shared_nodes_posts"] = []
APP_state["pending_authors"] = []
APP_state["nodes_with_authentication"] = True

def initAdmin():
	try :
		f = open("admin_credentials.txt")
		text = f.read()
		splitted = text.split(',')
		login = splitted[0].split(':')[1].strip()
		password = splitted[1].split(':')[1].strip()
		APP_state['admin_credentials'] = [login, password]
		f.close()
		print APP_state["admin_credentials"] 

	except Exception as e:
		print "error while loading admin : ", e


def DELETE_ALL():
	db.session.query(Author_Relationships).delete()
	db.session.query(Authors).delete()
	db.session.query(Comments).delete()
	db.session.query(Friend_Requests).delete()
	db.session.query(Images).delete()
	db.session.query(Posts).delete()
	db.session.query(Servers).delete()
	db.session.query(URL).delete()


def initAppState():
	global APP_state
	if "session_ids" not in APP_state.keys():
		APP_state["session_ids"]={}


def saveAppState():
	pass

def initServerObj():
	server={}
	server["server_id"] = uuid.uuid4().hex
	server["IP"] = "http://127.0.0.1:5000"  
	APP_state["no_servers"] += 1
	server["server_index"] = 1
	myServer=Servers(server)
	APP_state['local_server_Obj'] = myServer
	db.session.add(myServer)
	db.session.commit()

def createDefaultAuthor():
	defaultAuthor1=Authors(author1)
	defaultAuthor2=Authors(author2)
	db.session.add(defaultAuthor1)
	db.session.add(defaultAuthor2)
	db.session.commit()

db.create_all()
initServerObj()
initAdmin()
createDefaultAuthor()










