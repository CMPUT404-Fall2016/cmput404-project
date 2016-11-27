from flask import jsonify
from sqlalchemy import exc
from model import *
from datetime import datetime
import time
import uuid

random.seed(time.time())



class RestHandlers():
    """
    This class implements functionality based on the specifications in:
    https://github.com/abramhindle/CMPUT404-project-socialdistribution/blob/master/example-article.json
    """
    def __init__(self):
        pass
    
    def getAuthor(self, aid):
        return db.session.query(Authors).filter(Authors.author_id == aid).first()

    def getAllPosts(self, param=None):
        """
        This will be called in response to :
        GET http://service/posts  (all posts marked as public on the server)

        Refer to top - 113
        """ 
        # I assume for now view_permission = 1 -> public
        rtl = []
        posts = self.sort_posts( db.session.query(Posts).filter(Posts.view_permission == 1).all() ) 
        for post in posts:
            rtl.append([post, self.getAuthor(post.author_id), self.getComments(post.post_id)])
        return rtl


    def getVisiblePosts(self, authenticatedUser):
        """
        This will be called in response to :
        GET http://service/author/posts  (posts that are visible to the currently authenticated user)
        
        Refer to top - 113
        """
        #Firstly fetch all friends of the currently authenticated user
        friends = db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == authenticatedUser, Author_Relationships.relationship_type == 3).all()
        friends2 = db.session.query(Author_Relationships).filter(Author_Relationships.author2_id == authenticatedUser, Author_Relationships.relationship_type == 3).all()

        #firends 
        rtl = []
        fofr = []
        fof = set()
        for friend in friends:
            rtl = db.session.query(Posts).filter(Posts.author_id == friend.author2_id, Posts.view_permission == 3).all()    
            fofr = db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == friend.author2_id, Author_Relationships.relationship_type== 3).all()

            for ele in fofr:
                fof.add(ele.author2_id)         

            fofr = db.session.query(Author_Relationships).filter(Author_Relationships.author2_id == friend.author2_id, Author_Relationships.relationship_type== 3).all()
        
            for ele in fofr:
                fof.add(ele.author1_id)

        for friend in friends2:
            rtl += db.session.query(Posts).filter(Posts.author_id == friend.author1_id, Posts.view_permission == 3).all()   
            fofr = db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == friend.author1_id, Author_Relationships.relationship_type== 3).all()
            for ele in fofr:
                fof.add(ele.author2_id)         

            fofr = db.session.query(Author_Relationships).filter(Author_Relationships.author2_id == friend.author1_id, Author_Relationships.relationship_type== 3).all()
            for ele in fofr:
                fof.add(ele.author1_id)

    
        #self posts exclude public ones
        rtl += db.session.query(Posts).filter(Posts.author_id == authenticatedUser, Posts.view_permission != 1).all()   

        #friend of friend
        for ele in fof:
            if ele != authenticatedUser:
                rtl += db.session.query(Posts).filter(Posts.author_id == ele, Posts.view_permission == 4).all()
        
        #all public ones
        rtl += db.session.query(Posts).filter(Posts.view_permission == 1).all() 


        posts = self.sort_posts(rtl)    
        rtl = []
        for post in posts:
            rtl.append([post, self.getAuthor(post.author_id), self.getComments(post.post_id)])
        return rtl



    def getVisiblePostsByAuthor(self, authenticatedUser, user_id):
        """
        This will be called in response to :
        GET http://service/author/{AUTHOR_ID}/posts  (all posts made by {AUTHOR_ID} visible to the currently authenticated user)        

        Refer to top - 113
        """
        rtl = []

        #First step is determine the relationship of the two authors
        if(authenticatedUser == user_id):
            posts = db.session.query(Posts).filter(Posts.author_id == user_id).all()
        else:
            friendship = db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == authenticatedUser, Author_Relationships.author2_id == user_id, Author_Relationships.relationship_type == 3).all()

            if not friendship:
                friendship = db.session.query(Author_Relationships).filter(Author_Relationships.author2_id == authenticatedUser, Author_Relationships.author1_id == user_id, Author_Relationships.relationship_type == 3).all()

            #Get the user's public post
            rtl = db.session.query(Posts).filter(Posts.author_id == user_id, Posts.view_permission == 1).all()  
            fof = set()
            if friendship:
                #they are friends
                rtl += db.session.query(Posts).filter(Posts.author_id == user_id, Posts.view_permission == 3).all() 
                fofr = db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == user_id, Author_Relationships.relationship_type == 3).all()
                for ele in fofr:
                    fof.add(ele.author2_id)                                         

                fofr += db.session.query(Author_Relationships).filter(Author_Relationships.author2_id == user_id, Author_Relationships.relationship_type == 3).all()
                for ele in fofr:
                    fof.add(ele.author1_id)                                         

            #Friend of Friend
            for ele in fof:
                if ele != authenticatedUser:
                    rtl += db.session.query(Posts).filter(Posts.author_id == ele, Posts.view_permission == 4).all()

            posts = rtl

        rtl = []
        for post in posts:
            rtl.append([post, self.getAuthor(post.author_id), self.getComments(post.post_id)])
        return rtl



    def getPost(self, post_id):
        """
        This will be called in response to :
        GET http://service/posts/{POST_ID}  access to a single post with id = {POST_ID}     
        
        Refer to top - 113
        """
        #Return a post with its images list and its comments list
        return [db.session.query(Posts).filter(Posts.post_id == post_id).first(), self.getAuthor(author_id), self.getComments(post_id)]
        #return [db.session.query(Posts).filter(Posts.post_id == post_id).first(), self.getAuthor(author_id), self.getComments(post_id)]


    def getComments(self, post_id):
        """
        This will be called in response to :
        GET http://service/posts/{post_id}/comments  access to the comments in a post

        Refer to line 116-141
        """
        #Get the comments of the post with post_id
        return db.session.query(Comments).filter(Comments.post_id == post_id).all() 



    def getImages(self, post_id):
        #Get the images of the post with post_id
        return db.session.query(Images).filter(Images.post_id == post_id).all() 



    def delete_post(self, post_id):
        #Fetch post that needs to be deleted
        d = db.session.query(Posts).filter(Posts.post_id == post_id).first()    
        cmts = db.session.query(Comments).filter(Comments.post_id == post_id).all()
        imgs = db.session.query(Images).filter(Images.post_id == post_id).all()
        #Delete the post from DB including its images and comments
        for cmt in cmts:
            self.delete_comment(cmt.comment_id)
        for img in imgs:
            self.delete_image(img.image_id)
        try:
            db.session.delete(d)
            db.session.commit()     
            #Successfully deleted the post
            return True
        except  exc.SQLAlchemyError:
            return False



    def delete_comment(self, comment_id):
        #Fetch comment that needs to be deleted
        d = db.session.query(Comments).filter(Comments.comment_id == comment_id).first()    
        #Delete the post from DB
        try:
            db.session.delete(d)
            db.session.commit()     
            #Successfully deleted the comment
            return True
        except  exc.SQLAlchemyError:
            return False



    def delete_image(self, image_id):
        #Fetch Image that needs to be deleted
        d = db.session.query(Images).filter(Images.image_id == image_id).first()    
        #Delete the post from DB
        try:
            db.session.delete(d)
            db.session.commit()     
            #Successfully deleted the image
            return True
        except  exc.SQLAlchemyError:
            return False



    def make_post(self, data):
        #Make the post 
        currentTime = datetime.now()
        post =  {
                            "post_id" : uuid.uuid4().hex, #Need to change to self generated uuid
                            "title" :   data["title"],
                            "content_type"  : data["content_type"],
                            "desciption"    : data["description"],
                            "categories"    : "abram bear",
                            "content"   :   data["content"],
                            "creation_time" :   currentTime,
                            "view_permission" : data["view_permission"],
                            "author_id" :   data["author_id"]
                        }       


        #If the post comes with images, make them
        data["post_id"] = post["post_id"]
        if "images" in data:
            self.make_images(data)


        try:
            db.session.add(Posts(post))
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            return False



    def make_comment(self, data):
        currentTime = datetime.now()    
        comment = {
                                "comment_id"    :   data["comment_id"],
                                "author_id" :   data["author_id"],
                                "author_host" :   data["author_host"],
                                "author_name" :   data["author_name"],
                                "author_url" :   data["author_url"],
                                "author_github" :   data["author_github"],
                                "post_id"   :   data["post_id"],
                                "comment_text"  :   data["comment_text"],
                                "content_type"  :   "text/markdown",    
                                "creation_time" :   data["published"]
                            }
        try:
            db.session.add(Comments(comment))
            db.session.commit()
            return True
        except  exc.SQLAlchemyError:
            return False
        



    #Add the images to the database
    def make_images(self, data):
        try:
            for image in data["images"]: 
                img =   {   
                                "image_id"  :   uuid.uuid4().hex, #Need to change to self generated uuid
                                "post_id"   :   data["post_id"],
                                "image" :   image   #Decode to BLOB from Base64 encoded string
                            }
                db.session.add(Images(img))
                db.session.commit()
            return True
        except exc.SQLAlchemyError:
            return False

    

    #This merge sort function sorts the posts based on creation time
    #Complexity:    O(n*log(n))
    def sort_posts(self, posts):
        result = []
        if len(posts) < 2:
            return posts
        mid = int(len(posts)/2)
        y = self.sort_posts(posts[:mid])
        z = self.sort_posts(posts[mid:])
        i = 0
        j = 0
        while i < len(y) and j < len(z):
            if y[i].creation_time < z[j].creation_time:
                result.append(z[j])
                j += 1
            else:
                result.append(y[i])
                i += 1
        result += y[i:]
        result += z[j:]
        return result

    def updatePost(self, param):

        if len(param.keys()) <= 1:
            return True

        results = db.session.query(Posts).filter(Posts.post_id == param["post_id"]).all()
        results_image = db.session.query(Images).filter(Images.post_id == param["image_id"]).all()
        
        if len(results) == 0:
            return "NO_MATCH"
        
        post = results[0]
        image = results_image[0]

        if "title" in param.keys():
            post.title = param["title"]

        if "text" in param.keys():
            post.text = param["text"]

        if "image" in param.keys():
            image.image = param["image"]

        try:
            db.session.commit()

        except Exception as e:
            print "ERROR! Failed to update post information! : ", e
            return "DB_FAILURE"

        return True


    #This function determines if usr1 and usr2 are friends or not
    def isFriend(self, usr1, usr2):
        friendship = db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == usr1, Author_Relationships.author2_id == usr2, Author_Relationships.relationship_type == 3).all()
        if not friendship:
            friendship = db.session.query(Author_Relationships).filter(Author_Relationships.author1_id == usr2, Author_Relationships.author2_id == usr1, Author_Relationships.relationship_type == 3).all()
        if not friendship:
            return False
        else:
            return True
        

    #This function gets all remote server addrs where we have permission to share data
    def getConnectedNodes(self):
        nodes = []
        servers = db.session.query(Servers).filter(Servers.shareWith == True).all()
        for ele in servers:
            nodes.append(ele.IP)
        return nodes        


    #This function returns true if usr is friend of at least one usr in usrs        
    def atlOneFriend(self, usr, usrs):
        for usrr in usrs:
            if isFriend(usr, usrr):
                return True
        return False

    
    #This function returns all FOAF posts stored in the server
    def getAllFoafPosts(self):
        return db.session.query(Posts).filter(Posts.view_permission == 4).all()


    def getAllFoafPostsByUsr(self, author_id):
        return db.session.query(Posts).filter(Posts.view_permission == 4, Posts.author_id == author_id).all()


    def getAllUsers(self):
        return db.session.query(Authors).filter().all()	
