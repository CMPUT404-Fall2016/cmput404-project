/*
    This is the table for posts entity.
*/

CREATE TABLE Posts
(
    post_id int,
    title varchar(64),
    text varchar(800),
    creation_time datetime,
    view_permission int,
    post_type int,
    numberOf_comments int,
    numberOf_URL int,
    numberOf_images int,
    PRIMARY KEY (post_id)
);

/*
    This is the table for comments entity.
*/

CREATE TABLE Comments
(
    comment_id int,
    post_id int,
    text varchar(800),
    creation_time datetime,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (post_id) REFERENCES Posts(post_id)
);

/*
    This is the table for images entity.
    If the image is not embedded in a post then post_id=0, if it is not embedded in a comment then comment_id=0.
*/

CREATE TABLE Images
(
    image_id int,
    post_id int,
    comment_id int,
    image BLOB,
    PRIMARY KEY (image_id),
    FOREIGN KEY (post_id) REFERENCES Posts(post_id),
    FOREIGN KEY (comment_id) REFERENCES Comments(comment_id)
);

/*
    This is the table for URL entity.
*/

CREATE TABLE URL
(
    URL_id int,
    post_id int,
    comment_id int,
    URL_link varchar(2048),
    type int,
    PRIMARY KEY (URL_id),
    FOREIGN KEY (post_id) REFERENCES Posts(post_id),
    FOREGIN KEY (comment_id) REFERENCES Comments(comment_id)
);

/*
    This is the table for Authors entity.
*/

CREATE TABLE Authors
(
    author_id int,
    name varchar(60),
    login_name varchar(60),
    password varchar(30),
    address varchar(100),
    birthdate date,
    bio varchar(200),
    numberOf_friends int,
    numberOf_followers int,
    numberOf_followees int,
    numberOf_friendRequests int,
    PRIMARY KEY (author_id)
);

/*
    This is the table for Author_Relationships. This is used for many-many relationships between authors.
*/

CREATE TABLE Author_Relationships
(
    AuthorRelationship_id int,
    author1_id int,
    authorServer1_id int,
    author2_id int,
    authorServer2_id int,
    type int,
    PRIMARY KEY (AuthorRelationship_id),
    FOREIGN KEY (author1_id) REFERENCES Authors(author_id),
    FOREIGN KEY (author2_id) REFERENCES Authors(author_id)
);

/*
    This is the table for Friend_Requests. Whenever a friend request is send, this table will add a friendrequest entry with information about the sender(including serverinfo) and the receiver, whether it has been checked by the receipent.
*/

CREATE TABLE Friend_Requests
(
    friendRequest_id int,
    fromAuthor_id int,
    fromAuthorServer_index int,
    toAuthor_id int,
    toAuthorServer_index int,
    isChecked boolean,
    PRIMARY KEY (friendRequest_id),
    FOREIGN KEY (fromAuthor_id) REFERENCES Authors(author_id),
    FOREIGN KEY (toAuthor_id) REFERENCES Authors(author_id)
);

/*
    This is the table for Servers. Each server will be assigned its own 64bit ID randomly when it is first created. 
    We will use a centralized server that keeps track of all the server's addresses and when a new server is 
    registered to the network, this central server will generate the ID and will send the ID along with IP, mac-address 
    to all the other connected servers. This table will be local to all the servers, so that everytime one server needs 
    to communicate with others, it doesnt have to rely on the central server. Also, I think using a local indexing system 
    is slightly safer as if for some reason the ID needs to be changed, the index will be consistent within the local 
    server's table. Probability of two servers being assigned same ID is 1/(2^128) which is approximately 2.94e-39. 
    Use "random.getrandbits" function for generating IDs.
*/

CREATE TABLE Servers
(
    server_id bigint,
    IP varchar(40), //Designed for 128bit IPv6 addressing
    server_index int,
    PRIMARY KEY(server_id)
);

