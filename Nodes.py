"""
key-names:
	
	for retrieving friendlist of author A:
		'GET/friends/A' 

	for checking whether author A1 and A2 are friends:
		'GET/friends/A1/A2'

	for checking whether the provided list of authors are friends  of A:  
		'POST/friends/A' 

	for making friend request:
		'POST/friendrequest'

	for fetching author A:  
		'GET/author/A' 

	For getting posts
		'GET/posts' 

	For getting posts visible to authenticated user:
		'GET/author/posts' 

	To get posts made by author A which is visible to authenticated user: 
		'GET/author/A/posts'

	To get post with post ID P 
		'GET/posts/P' 

	To get comments of post ID P
		'GET/posts/P/comments'

	Make a comment in the post with ID P:  
		'POST/posts/P/comments' 

	How to use them?
	_NODES_ is a dictionary with keys that correspond to the host name of the nodes.
	_NODES_[SOME_HOST_NAME] is a dictionary with keys like 'GET/friends/A', anything from the above key-names
	The values corresponding to these key-names will contain prefix and suffix. 
	For example for getting author API we GET http://secret-penguin.herokuapp.com/author/948324923239sfsf9sf09sf, 
	the prefix is 'http://secret-penguin.herokuapp.com/author/' and suffix can be anything that comes after the AUTHOR ID like say for example '/getJson' can be a suffix

	Just use getAPI function for getting the suffixes and prefixes

"""

def getAPI(hostname, API_NAME):
	host_dict = _NODES_[hostname]
	try:
		[prefix, suffix] = host_dict[API_NAME]
		return [prefix, suffix]

	except Exception as e:
		print "API_NAME provided is not a valid key, please provide a valid key"
		return None

def testgetAPI(hosts):
	authorID1 = str(12)
	authorID2 = str(34)
	postID = str(56)

	for host in hosts:
		print("")
		print "for host : %s"%(host)
		[prefix, suffix] = getAPI(host, 'GET/friends/A')
		print 'URL for "GET/friends/A" : %s' % (prefix + authorID1 + suffix) 
		[prefix, suffix] = getAPI(host, 'GET/friends/A1/A2')
		print 'URL for "GET/friends/A1/A2" : %s' % (prefix + authorID1 + '/' + authorID2 + suffix) 
		[prefix, suffix] = getAPI(host, 'POST/friends/A') 
		print 'URL for "POST/friends/A" : %s' % (prefix+authorID1+suffix) 
		[prefix, suffix] = getAPI(host, 'POST/friendrequest')
		print 'URL for "POST/friendrequest" : %s' % (prefix+suffix) 
		[prefix, suffix] = getAPI(host, 'GET/author/A') 
		print 'URL for "GET/author/A" : %s' % (prefix+ authorID1 + suffix) 
		[prefix, suffix] = getAPI(host, 'GET/posts') 
		print 'URL for "GET/posts" : %s' % (prefix + suffix) 
		[prefix, suffix] = getAPI(host, 'GET/author/posts') 
		print 'URL for "GET/author/posts" : %s' % (prefix + suffix) 
		[prefix, suffix] = getAPI(host,'GET/author/A/posts')
		print 'URL for "GET/author/A/posts" : %s' % (prefix + authorID1 + suffix) 
		[prefix, suffix] = getAPI(host, 'GET/posts/P') 
		print 'URL for "GET/posts/P" : %s' % (prefix + postID + suffix)
		[prefix, suffix] = getAPI(host, 'GET/posts/P/comments')
		print 'URL for "GET/posts/P/comments" : %s' % (prefix + postID + suffix)
		[prefix, suffix] = getAPI(host, 'POST/posts/P/comments') 
		print 'URL for "POST/posts/P/comments" : %s' % (prefix + postID + suffix)



_NODES_ = {}
secret_penguin = {
			'GET/friends/A' : ["http://secret-penguin.herokuapp.com/friends/", ""],
			'GET/friends/A1/A2' : ["http://secret-penguin.herokuapp.com/friends/", ""],
			'POST/friends/A' : ["http://secret-penguin.herokuapp.com/friends/" , ""],
			'POST/friendrequest' : ["http://secret-penguin.herokuapp.com/friendrequest", ""],
			'GET/author/A' : ["http://secret-penguin.herokuapp.com/author/", ""],
			'GET/posts' : ["http://secret-penguin.herokuapp.com/posts", ""],
			'GET/author/posts' : ["http://secret-penguin.herokuapp.com/author/posts", ""],
			'GET/author/A/posts' : ["http://secret-penguin.herokuapp.com/author/", "/posts"],
			'GET/posts/P' : ["http://secret-penguin.herokuapp.com/posts/", ""],
			'GET/posts/P/comments' : ["http://secret-penguin.herokuapp.com/posts/", "/comments"],
			'POST/posts/P/comments' : ["http://secret-penguin.herokuapp.com/posts/", "/comments"]
		   }

secure_springs = {
			'GET/friends/A' : ["http://secure-springs-85403.herokuapp.com/friends/", ""],
			'GET/friends/A1/A2' : ["http://secure-springs-85403.herokuapp.com/friends/", ""],
			'POST/friends/A' : ["http://secure-springs-85403.herokuapp.com/friends/" , ""],
			'POST/friendrequest' : ["http://secure-springs-85403.herokuapp.com/friendrequest", ""],
			'GET/author/A' : ["http://secure-springs-85403.herokuapp.com/author/", ""],
			'GET/posts' : ["http://secure-springs-85403.herokuapp.com/posts", ""],
			'GET/author/posts' : ["http://secure-springs-85403.herokuapp.com/author/posts", ""],
			'GET/author/A/posts' : ["http://secure-springs-85403.herokuapp.com/author/", "/posts"],
			'GET/posts/P' : ["http://secure-springs-85403.herokuapp.com/posts/", ""],
			'GET/posts/P/comments' : ["http://secure-springs-85403.herokuapp.com/posts/", "/comments"],
			'POST/posts/P/comments' : ["http://secure-springs-85403.herokuapp.com/posts/", "/comments"]
			}

bloggyblog404 = {
			'GET/friends/A' : ["http://api-bloggyblog404.herokuapp.com/friends/", "/?format=json"],
			'GET/friends/A1/A2' : ["http://api-bloggyblog404.herokuapp.com/friends/", "/?format=json"],
			'POST/friends/A' : ["http://api-bloggyblog404.herokuapp.com/friends/" , "/?format=json"],
			'POST/friendrequest' : ["http://api-bloggyblog404.herokuapp.com/friendrequest", "/?format=json"],
			'GET/author/A' : ["http://api-bloggyblog404.herokuapp.com/author/", "/?format=json"],
			'GET/posts' : ["http://api-bloggyblog404.herokuapp.com/posts", "/?format=json"],
			'GET/author/posts' : ["http://api-bloggyblog404.herokuapp.com/author/posts", "/?format=json"],
			'GET/author/A/posts' : ["http://api-bloggyblog404.herokuapp.com/author/", "/posts/?format=json"],
			'GET/posts/P' : ["http://api-bloggyblog404.herokuapp.com/posts/", "/?format=json"],
			'GET/posts/P/comments' : ["http://api-bloggyblog404.herokuapp.com/posts/", "/comments/?format=json"],
			'POST/posts/P/comments' : ["http://api-bloggyblog404.herokuapp.com/posts/", "/comments/?format=json"]
			}


_NODES_['http://secret-penguin.herokuapp.com'] = secret_penguin
_NODES_['http://secure-springs-85403.herokuapp.com'] = secure_springs
_NODES_['http://api-bloggyblog404.herokuapp.com'] = bloggyblog404

if __name__ == "__main__":
	hostnames = ['http://secret-penguin.herokuapp.com', 'http://secure-springs-85403.herokuapp.com', 'http://api-bloggyblog404.herokuapp.com']
	testgetAPI(hostnames)
