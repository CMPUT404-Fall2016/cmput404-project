URL = "http://127.0.0.1:5000"  


author1_reg={}
author1_reg["name"] 	  = "Touqir Sajed"
author1_reg["login_name"] = "touqir"
author1_reg["password"]   = "123456"

author2_reg={}
author2_reg["name"] 	  = "Shrek the third"
author2_reg["login_name"] = "shrek3rd"
author2_reg["password"]   = "123456"


author1_log={}
author1_log["name"] 	  = "Touqir Sajed"
author1_log["login_name"] = "touqir"
author1_log["password"]   = "123456"

author2_log={}
author2_log["name"] 	  = "Shrek the third"
author2_log["login_name"] = "shrek3rd"
author2_log["password"]   = "123456"

author1_edit = {}
author1_edit['bio'] = 'I am cool :D'
author1_edit['github_id'] = 'shrekkii'

def createFriendRequest():
	friendRequest1 = {}
	friendRequest1["author"]={'id': author1_log['author_id'], 'host':URL, 'displayName':author1_log['name']}
	friendRequest1["friend"]={'id': author2_log['author_id'], 'host':URL, 'displayName':author2_log['name'], 'url' : URL+'/author/'+author2_log['author_id']}

	return friendRequest1
