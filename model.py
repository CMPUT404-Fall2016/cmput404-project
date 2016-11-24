from db import db
import uuid
import json

from Model.Author_Relationships import Author_Relationships
from Model.Authors import Authors
from Model.Comments import Comments
from Model.Friend_Requests import Friend_Requests
from Model.Images import Images
from Model.Posts import Posts
from Model.Servers import Servers
from Model.URL import URL
from Model.Global_var import Global_var
from sample_data.data1 import *


"""
APP_state is a global variable that contains important information about the state of the server. 

APP_state['no_friend_Requests'] : Number of friend requests send to this server. Used for id'ing friend requests
(MAYBE) ** APP_state['no_Authors'] : Number of Authors created on the server so far. Used for id'ing the authors **
"""
# APP_state = {}
# APP_state["session_ids"]={}
# APP_state["no_servers"] = 0
# APP_state["admin_credentials"] = None
# APP_state["shared_nodes"] = []
# APP_state["shared_nodes_images"] = []
# APP_state["shared_nodes_posts"] = []
# APP_state["nodes_with_authentication"] = True

def initAdmin():
    APP_state = loadGlobalVar()
    try :
        f = open("admin_credentials.txt")
        text = f.read()
        splitted = text.split(',')
        login = splitted[0].split(':')[1].strip()
        password = splitted[1].split(':')[1].strip()
        APP_state['admin_credentials'] = [login, password]
        f.close()
        print APP_state["admin_credentials"] 
        saveGlobalVar(APP_state)

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
    APP_state = loadGlobalVar()
    APP_state['session_ids'] = {}
    # APP_state['no_servers'] = 0
    APP_state['admin_credentials'] = None
    print APP_state
    saveGlobalVar(APP_state)

def initServerObj():
    global APP_state
    server={}
    server["server_id"] = uuid.uuid4().hex
    server["IP"] = "http://127.0.0.1:5000"  
    APP_state["no_servers"] += 1
    server["server_index"] = 0
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

def loadGlobalVar():
    global_var = db.session.query(Global_var).filter(Global_var.id == 0).all()[0]
    var_dict = json.loads(global_var.content)
    if 'local_server_Obj' in var_dict:
        myServer = var_dict['local_server_Obj']
        server_obj = emptyClass()  
        server_obj.server_id = myServer['server_id'] 
        server_obj.IP = myServer['IP'] 
        server_obj.server_index = myServer['server_index'] 
        server_obj.shareWith = myServer['shareWith'] 
        server_obj.shareWith_images = myServer['shareWith_images'] 
        server_obj.shareWith_posts = myServer['shareWith_posts'] 
        server_obj.user_name = myServer['user_name'] 
        server_obj.password = myServer['password'] 
        var_dict['local_server_Obj'] = server_obj

    return var_dict

def saveGlobalVar(var_dict):
    global_var = db.session.query(Global_var).filter(Global_var.id == 0).all()[0]
    if 'local_server_Obj' in var_dict:
        if type(var_dict['local_server_Obj']) == Servers or type(var_dict['local_server_Obj']) == emptyClass:
            server_obj = var_dict['local_server_Obj']
            myServer = {}
            myServer['server_id'] = server_obj.server_id
            myServer['IP'] = server_obj.IP
            myServer['server_index'] = server_obj.server_index
            myServer['shareWith'] = server_obj.shareWith
            myServer['shareWith_images'] = server_obj.shareWith_images
            myServer['shareWith_posts'] = server_obj.shareWith_posts
            myServer['user_name'] = server_obj.user_name
            myServer['password'] = server_obj.password
            var_dict['local_server_Obj'] = myServer
            print "Found type servers"

    print global_var
    toStore = json.dumps(var_dict)
    global_var.content = toStore
    db.session.commit()

def initDB():
    db.create_all()
    new_global = Global_var()
    new_global.content = "{}"
    new_global.id = 0
    db.session.add(new_global)
    db.session.commit()

class emptyClass():
    pass



# initServerObj()
initAppState()
initAdmin()
# initDB()
# createDefaultAuthor()










