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

// clear post tab when user on profile tab
$(".profiletab").click( function(e) {
    e.preventDefault();
    document.getElementById("posts").innerHTML = "";
});

// Onready
$(document).ready(function() {
  var myauthorid = localStorage.getItem("fetch-author-id");
//    console.log(localStorage.getItem("fetch-author-id"));

  // If author search there own id, it redirect them to the profile page
  if (myauthorid == getCookieid()) {
    window.location.href = "profilepage.html";
  }

  var mypTemplate = document.getElementById('profiledatas');

  var myprofilelink = "/author/" + myauthorid;

  sendAJAX("GET", myprofilelink, "", function(result) {

    // fill the container with details
    var td = mypTemplate.content.querySelector("#profilehname");
    profileusernametext = result.displayName;
    td.textContent = profileusernametext;

    mypTemplate.content.querySelector("#profileid").textContent = result.id;

    mypTemplate.content.querySelector("#profiledname").textContent = result.displayName;

    mypTemplate.content.querySelector("#profilehost").textContent = result.host;

    mypTemplate.content.querySelector("#profileurl").textContent = result.url;
    mypTemplate.content.querySelector("#profilegithub_id").textContent = result.githubUsername;

    var normalContent = document.getElementById('profile');

    var clonedTemplate = mypTemplate.content.cloneNode(true);
    normalContent.appendChild(clonedTemplate);

    // This checks if the user is the same as the search user
    if(getCookieid() == localStorage.getItem("fetch-author-id")) {
      document.getElementById("addfriendbtn").style.display="none";
    }

           var author2sid = getCookieid();

     var isfriend = "/friends/" + myauthorid + "/" + author2sid;
//       console.log(isfriend);

     sendAJAX("GET", isfriend, "", function(response) {
//        console.log(response.friends);
      if(response.friends == true) {
        //console.log(">>");
        //console.log(document.getElementById("addfriendbtn").style.display);
        //document.getElementById("addfriendbtn").style.display="none";
          changebtn();
      }
    });
  });
});

function changebtn() {
  document.getElementById("addfriendbtn").style.display="none";
}

$("#posttabs").click(function(e) {
  e.preventDefault();
  document.getElementById("posts").innerHTML = "";
  var authorpid = localStorage.getItem("fetch-author-id");
  var authorpostlink = "/author/" + authorpid + "/posts?size=50";
//  console.log(authorpostlink);

  var postList = document.getElementById("posts");
  var postTemplate = document.getElementById("post-container");
  // page=<Page_No>&size=<Page_Zize>
  sendAJAX("GET", authorpostlink, "", function(results) {
    for(var i=0; i < results.posts.length; ++i) {
      // fill the container with details
      postTemplate.content.querySelector(".post-title").textContent = results.posts[i].title;
      postTemplate.content.querySelector(".post-description").textContent = results.posts[i].description;
      postTemplate.content.querySelector(".post-author").textContent = results.posts[i].author.displayName;

       if(results.posts[i].contentType == "text/markdown" || results.posts[i].contentType == "text/x-markdown") {
           var cmreader = new commonmark.Parser();
           var writer = new commonmark.HtmlRenderer();
           var parsed = cmreader.parse(results.posts[i].content); // parsed is a 'Node' tree
           // transform parsed if you like...
           var commonmarkresult = writer.render(parsed);
           postTemplate.content.querySelector(".post-content").innerHTML = commonmarkresult;
       } else {
           postTemplate.content.querySelector(".post-content").innerHTML = results.posts[i].content;
       }

      //postTemplate.content.querySelector(".post-content").innerHTML = results.posts[i].content;
      if (results.posts[i].count > 0) {
        postTemplate.content.querySelector(".comments-num").textContent = "("+results.posts[i].count+")";
      } else {
        postTemplate.content.querySelector(".comments-num").textContent = "";
      }
      // attach data to the links so it can be referenced when clicked
      var authorBtn = postTemplate.content.querySelector(".post-author");
      authorBtn.setAttribute("post-author-id", results.posts[i].author.id);

      var commentsBtn = postTemplate.content.querySelector(".comments");
      commentsBtn.setAttribute("post-id", results.posts[i].id);

      var clone = document.importNode(postTemplate.content, true);
      postList.appendChild(clone);
    }

    // bind the onclick to set post host and id in localStorage
    // and link the user to the post's page
    $(".comments").click(function(e) {
      e.preventDefault();
      // set this for later
      // localStorage.setItem("fetch-post-host", $(this).data("post-host"));
      localStorage.setItem("fetch-post-id", $(this).attr("post-id"));
      window.location.href ="post.html";
      });

    // bind the onclick to set author id in localStorage
    // and link the user to the author's profile
    $(".post-author-url").click(function(e) {
      e.preventDefault();
      // set this for authorpage to use
      localStorage.setItem("fetch-author-id", $(this).attr("post-author-id"));
      window.location.href = "authorpage.html";
      });
    });
  });

// Bind to the addfriendbtn. This gets the info of the two user to use in afriendtwo function
function afriendone() {
  var myuserid = getCookieid();

  var myinfostuff = "/author/" + myuserid;
  var headers = [["Foreign-Host", "false"], ["Authorization", "Basic c2VydmVydG9zZXJ2ZXI6NjU0MzIx"]];

  sendAJAX("GET", myinfostuff, "", function(result) {
    var myinfodatacombine = {}
    myinfodatacombine.myhost = result.host;
    myinfodatacombine.mydisplayname = result.displayName;
    myinfodatacombine.mydisplayname = result.url;
//    console.log(myinfodatacombine);

    //var friendid = getFriendcookieid();
    var friendid = localStorage.getItem("fetch-author-id");
    var getfriendinfo = "/author/" + friendid;

    sendAJAX("GET", getfriendinfo, "", function(result2) {
      var myinfodatacombines = {}
//      console.log(result.displayName);
      myinfodatacombines.myhost = result.host;
      myinfodatacombines.mydisplayname = result.displayName;
      myinfodatacombines.myurl = result.url;
      myinfodatacombines.friendid = result2.id;
      myinfodatacombines.friendhost = result2.host;
      myinfodatacombines.frienddisplayname = result2.displayName
      myinfodatacombines.friendurl = result2.url;

//             console.log(myinfodatacombines);

      afriendtwo(myinfodatacombines);
    });
  });
}

// This sends the friend request to the user
function afriendtwo(result) {

  // This is the body for the POST request
  var friendrequestdata = {};

    friendrequestdata["author"] = {};
    friendrequestdata["author"]["id"] = result.friendid;
    friendrequestdata["author"]["host"] = result.friendhost;
    friendrequestdata["author"]["displayName"] = result.frienddisplayname;
//    friendrequestdata["author"]["url"] = result.friendurl;
    friendrequestdata["friend"] = {}
    friendrequestdata["friend"]["id"]= getCookieid();;
    friendrequestdata["friend"]["host"] = result.myhost;
    friendrequestdata["friend"]["displayName"] = result.mydisplayname;
    friendrequestdata["friend"]["url"] = result.myurl;

//  console.log(JSON.stringify(friendrequestdata));

  var headers = [["Foreign-Host", "false"], ["Authorization", "Basic c2VydmVydG9zZXJ2ZXI6NjU0MzIx"]];
  sendAJAX("POST", "/friendrequest/", friendrequestdata, null);
  document.getElementById("addfriendbtn").style.display="none";
}
