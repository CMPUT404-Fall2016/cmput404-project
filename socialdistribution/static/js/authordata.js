function getCookieid() {
  // look for the github_name in cookies
  var cookies = document.cookie.split(";");
  for(var i=0; i < cookies.length; i++) {
    var gname = cookies[i].split("=");
    if(gname[0].trim() == "cookie_cmput404_author_id") {
      return gname[1];
    }
  }
  return "";
}

function getCookiehost() {
  // look for the github_name in cookies
  var cookies = document.cookie.split(";");
  for(var i=0; i < cookies.length; i++) {
    var gname = cookies[i].split("=");
    if(gname[0] == "cookie_cmput404_author_host") {
      return gname[1];
    }
  }
  return "";
}

function getFriendcookieid() {
  // look for the github_name in cookies
  var cookies = document.cookie.split(";");
  for(var i=0; i < cookies.length; i++) {
    var gname = cookies[i].split("=");
    if(gname[0].trim() == "request_author_id") {
      return gname[1];
    }
  }
  return "";
}


function editauthorpage() {
  document.getElementById("profiledname").textContent = document.getElementById("pdn").value;
  //document.getElementById("pdn").placeholder = document.getElementById("profiledname").textContent;
  document.getElementById("pdn").value = document.getElementById("profiledname").textContent;
}

$(document).ready(function() {
    //var myauthorid = getCookieid();
    var myauthorid = localStorage.getItem("fetch-author-id");

    var mypTemplate = document.getElementById('profiledatas');

    //var friendauthorid = getFriendcookieid();

    var myprofilelink = "/author/" + myauthorid;

    sendAJAX("GET", myprofilelink, "", function(result) {

      console.log(result);
      var td = mypTemplate.content.querySelector("#profilehname");
      profileusernametext = result.displayName;
      td.textContent = profileusernametext;

      mypTemplate.content.querySelector("#profileid").textContent = result.id;

      mypTemplate.content.querySelector("#profiledname").textContent = result.displayName;

      mypTemplate.content.querySelector("#profilehost").textContent = result.host;

      mypTemplate.content.querySelector("#profileurl").textContent = result.url;
      mypTemplate.content.querySelector("#profilegithub_id").textContent = result.github_username;

      var normalContent = document.getElementById('profile');

      var clonedTemplate = mypTemplate.content.cloneNode(true);
      normalContent.appendChild(clonedTemplate);


      if(getCookieid() == getFriendcookieid()) {
        document.getElementById("addfriendbtn").style.display="none";
      }
    });

    var author2sid = getCookieid();

    var isfriend = "/friends/" + myauthorid + "/" + author2sid;
    console.log(isfriend);

    sendAJAX("GET", isfriend, "", function(response) {
             console.log(response.friends);
             if(response.friends == true) {
             document.getElementById("addfriendbtn").style.display="none";
             }
             });
});

$("#posttabs").click(function(e) {
  e.preventDefault();
  var authorpid = getFriendcookieid();
  var authorpostlink = "service/author/" + authorpid + "/posts";

  var postList = document.getElementById("posts");
  var postTemplate = document.getElementById("post-container");
  // page=<Page_No>&size=<Page_Zize>
  sendAJAX("GET", authorpostlink, "", function(posts) {
    for(var i=0; i < posts.length; ++i) {
      // fill the container with details
      postTemplate.content.querySelector(".post-title").textContent = posts[i].title;
      // postTemplate.content.querySelector(".post-description").textContent = posts[i].description;
      // postTemplate.content.querySelector(".post-author").textContent = posts[i].author.displayname;
      postTemplate.content.querySelector(".post-author").textContent = posts[i].author_id;
      postTemplate.content.querySelector(".post-content").textContent = posts[i].content;

      // attach data to the links so it can be referenced when clicked
      var authorBtn = postTemplate.content.querySelector(".post-author");
      $(authorBtn).data("post-author", posts[i].author_id);

      var commentsBtn = postTemplate.content.querySelector(".comments");
      // $(commentsBtn).data("post-host", posts[i].author.host);
      $(commentsBtn).data("post-id", posts[i].id);

      var clone = document.importNode(postTemplate.content, true);
      postList.appendChild(clone);
    }

    // bind the onclick to set post host and id in localStorage
    // and link the user to the post's page
    $(".comments").click(function(e) {
      e.preventDefault();
      // set this for later
      // localStorage.setItem("fetch-post-host", $(this).data("post-host"));
      localStorage.setItem("fetch-post-id", $(this).data("post-id"));
      window.location.href ="post.html";
      });

    // bind the onclick to set author id in localStorage
    // and link the user to the author's profile
    $(".post-author-url").click(function(e) {
      e.preventDefault();
      // set this for authorpage to use
      localStorage.setItem("fetch-author-id", $(this).data("post-author-id"));
      window.location.href = "authorpage.html";
      });
    });
  });

function afriendone() {
  console.log("in?");
  var myuserid = getCookieid();

  var myinfostuff = "/author/" + myuserid;
  sendAJAX("GET", myinfostuff, "", function(result) {
    //console.log(result);
    //var myid = result.id;
    var myinfodatacombine = {}
    myinfodatacombine.myhost = result.host;
    myinfodatacombine.mydisplayname = result.displayName;
    //           var myhost = result.host;
    //           var mydisplayname = result.displayName;
    //fn(myinfodatacombine);

    var friendid = getFriendcookieid();
    var getfriendinfo = "/author/" + friendid;

    sendAJAX("GET", getfriendinfo, "", function(result2) {
      //console.log(result);
      var myinfodatacombine = {}
      console.log(result.displayName);
      myinfodatacombine.myhost = result.host;
      myinfodatacombine.mydisplayname = result.displayName;
      console.log("<<");
      console.log(result.displayName);
      console.log(">>");
      myinfodatacombine.friendid = result2.id;
      myinfodatacombine.friendhost = result2.host;
      myinfodatacombine.frienddisplayname = result2.displayName
      myinfodatacombine.friendurl = result2.url;

      afriendtwo(myinfodatacombine);
    });
  });
}

function afriendtwo(result) {
  console.log("hello");
  console.log(result);
  console.log("result1done");
  //var myhost = result.host;
  //console.log(result.host)
  //console.log(myhost);
  //var mydisplayname = result.displayName;
  var friendrequestdata = {};
    friendrequestdata["author"] = {}
  friendrequestdata["author"]["id"]= getCookieid();;
    friendrequestdata["author"]["host"] = result.myhost;
    friendrequestdata["author"]["displayName"] = result.mydisplayname;

     //  friendrequestdata["friend"]={"id":friendid, "host":friendhost, "displayName":frienddisplayname, "url":friendurl};
     //console.log(friendrequestdata);
    friendrequestdata["friend"] = {};
    friendrequestdata["friend"]["id"] = result.friendid;
    friendrequestdata["friend"]["host"] = result.friendhost;
    friendrequestdata["friend"]["displayName"] = result.frienddisplayname;
    friendrequestdata["friend"]["url"] = result.friendurl;
  console.log("<<");
  console.log(result.mydisplayName);

  console.log(friendrequestdata);
  console.log(">>");

  sendAJAX("POST", "/friendrequest", friendrequestdata, function(response) {
  console.log(response);
  if(response["status"] == "SUCCESS") {


    document.getElementById("addfriendbtn").style.display="none";
  }
  //window.location.href="friendspage.html";
  });
}
