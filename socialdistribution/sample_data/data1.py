from datetime import datetime
import time
import random

random.seed(time.time())
currentTime=datetime.now()

# Instances of Authors table

author1={}
author1["author_id"]  = 1
author1["name"] 	  = "Touqir Sajed"
author1["login_name"] = "touqir"
author1["password"]   = "123456"
author1["address"]    = "edmonton, alberta, Canada"
author1["birthdate"]  = currentTime
author1["bio"]        = "I love myself :D"
author1["numberOf_friends"] = 0  
author1["numberOf_followers"] = 0  
author1["numberOf_followees"] = 0  
author1["numberOf_friendRequests"] = 0  

author_empty={}


author2={}
author2["author_id"]  = 2
author2["name"] 	  = "King"
author2["login_name"] = "king_"
author2["password"]   = "123456"
author2["birthdate"]  = currentTime

author3={}
author3["author_id"]  = 3
author3["name"] 	  = "He Man"
author3["login_name"] = "he_man"
author3["password"]   = "123456"
author3["birthdate"]  = currentTime
# author3["numberOf_friends"] = 0  
# author3["numberOf_followers"] = 0  
# author3["numberOf_followees"] = 0  
# author3["numberOf_friendRequests"] = 0  

author4={}
author4["author_id"]  = 4
author4["name"] 	  = "No Man"
author4["login_name"] = "No_man"
author4["password"]   = "123456"
author4["birthdate"]  = currentTime

authors=[author1, author2, author3, author4]



#Instances of Server

server_empty={}

server1={}
server1["server_id"] = random.getrandbits(63)
server1["IP"] = "4023:decd:5f04:7aea:3c6b:c3bf:8335:e3cf" 
server1["server_index"] = 1

server2={}
server2["server_id"] = random.getrandbits(63)
server2["IP"] = "a164:ea21:735f:4af8:c49c:4dbf:ce66:a560"  
server2["server_index"] = 2

server3={}
server3["server_id"] = random.getrandbits(63)
server3["IP"] = "ad24:1b7d:39e0:c9c3:a9ba:60d9:b17:551d" 
server3["server_index"] = 3

servers=[server1, server2, server3]


#Instances of Author_Relationships

AR_empty={}

AR1={}
AR1["AuthorRelationship_id"] = 1
AR1["authorServer1_id"] = server1["server_index"]
AR1["authorServer2_id"] = server2["server_index"]
AR1["author1_id"] = author1["author_id"]
AR1["author2_id"] = author2["author_id"]
AR1["relationship_type"] = 1 # author 1 is only following author 2.

AR2={}
AR2["AuthorRelationship_id"] = 2
AR2["authorServer1_id"] = server1["server_index"]
AR2["authorServer2_id"] = server2["server_index"]
# Suppose there are 2 identical accounts on 2 servers, eg both have author1
AR2["author1_id"] = author1["author_id"]
AR2["author2_id"] = author1["author_id"]
AR2["relationship_type"] = 2 # author 1(server1) and author 1(server2) are mutually following each other(they are friends).

author_relationships=[AR1, AR2]


