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

function sendAJAX2(headers, method, url, message, callback) {
  var xhr = new XMLHttpRequest();
  xhr.open(method, url);
  xhr.onreadystatechange = function(){
    if (xhr.readyState==4) {
      try {
        if (xhr.status==200) {
          if(callback) {
            // console.log(xhr.responseText);
            callback(JSON.parse(xhr.responseText));
          }
        }
      }
      catch(e) {
        alert('Error: ' + e.name);
      }
    }
  }
  console.log(headers.length);
  for (var i=0; i<headers.length; ++i) {
    xhr.setRequestHeader(headers[i][0], headers[i][1]);
    console.log(headers[i][0] + headers[i][1]);
  }
  xhr.send(JSON.stringify(message));
}


function editauthorpage() {
  document.getElementById("profiledname").textContent = document.getElementById("pdn").value;
  //document.getElementById("pdn").placeholder = document.getElementById("profiledname").textContent;
  document.getElementById("pdn").value = document.getElementById("profiledname").textContent;
}

// clear post tab when user on profile tab
$("#profile").click( function(e) {
    e.preventDefault();
    document.getElementById("posts").innerHTML = "";
});

// Onready
$(document).ready(function() {
    var myauthorid = localStorage.getItem("fetch-author-id");
    console.log(localStorage.getItem("fetch-author-id"));
                  
    // If author search there own id, it redirect them to the profile page
    if (myauthorid == getCookieid()) {
      window.location.href = "profilepage.html";
    }

    var mypTemplate = document.getElementById('profiledatas');

    var myprofilelink = "/author/" + myauthorid;
                  
    var headers = [["Foreign-Host", "false"], ["Authorization", "Basic c2VydmVydG9zZXJ2ZXI6NjU0MzIx"]];
    sendAJAX2(headers, "GET", myprofilelink, "", function(result) {
              
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
      if(getCookieid() == getFriendcookieid()) {
        document.getElementById("addfriendbtn").style.display="none";
      }
    });

    var author2sid = getCookieid();
                  
    var headers2 = [["Foreign-Host", "false"], ["Authorization", "Basic c2VydmVydG9zZXJ2ZXI6NjU0MzIx"]];
    var isfriend = "/friends/" + myauthorid + "/" + author2sid;
    console.log(isfriend);

    sendAJAX2(headers, "GET", isfriend, "", function(response) {
             console.log(response.friends);
             if(response.friends == true) {
             document.getElementById("addfriendbtn").style.display="none";
             }
     });
});

$("#posttabs").click(function(e) {
  e.preventDefault();
  var authorpid = getFriendcookieid();
  var authorpostlink = "/author/" + authorpid + "/posts";

  var postList = document.getElementById("posts");
  var postTemplate = document.getElementById("post-container");
  // page=<Page_No>&size=<Page_Zize>
                     var headers = [["Foreign-Host", "false"]];
  sendAJAX2(headers, "GET", authorpostlink, "", function(posts) {
    for(var i=0; i < posts.length; ++i) {
      // fill the container with details
      postTemplate.content.querySelector(".post-title").textContent = posts[i].title;
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

// Bind to the addfriendbtn. This gets the info of the two user to use in afriendtwo function
function afriendone() {
  var myuserid = getCookieid();

  var myinfostuff = "/author/" + myuserid;
  
  var headers = [["Foreign-Host", "false"]];
  sendAJAX2(headers, "GET", myinfostuff, "", function(result) {
  //sendAJAX("GET", myinfostuff, "", function(result) {
    var myinfodatacombine = {}
    myinfodatacombine.myhost = result.host;
    myinfodatacombine.mydisplayname = result.displayName;

    var friendid = getFriendcookieid();
    var getfriendinfo = "/author/" + friendid;

    var headers = [["Foreign-Host", "false"]];
    sendAJAX2(headers, "GET", getfriendinfo, "", function(result2) {
    //sendAJAX("GET", getfriendinfo, "", function(result2) {
      var myinfodatacombine = {}
      console.log(result.displayName);
      myinfodatacombine.myhost = result.host;
      myinfodatacombine.mydisplayname = result.displayName;
      myinfodatacombine.friendid = result2.id;
      myinfodatacombine.friendhost = result2.host;
      myinfodatacombine.frienddisplayname = result2.displayName
      myinfodatacombine.friendurl = result2.url;

      afriendtwo(myinfodatacombine);
    });
  });
}

// This sends the friend request to the user
function afriendtwo(result) {
  
  // This is the body for the POST request
  var friendrequestdata = {};
    friendrequestdata["author"] = {}
    friendrequestdata["author"]["id"]= getCookieid();;
    friendrequestdata["author"]["host"] = result.myhost;
    friendrequestdata["author"]["displayName"] = result.mydisplayname;
    friendrequestdata["friend"] = {};
    friendrequestdata["friend"]["id"] = result.friendid;
    friendrequestdata["friend"]["host"] = result.friendhost;
    friendrequestdata["friend"]["displayName"] = result.frienddisplayname;
    friendrequestdata["friend"]["url"] = result.friendurl;

  sendAJAX("POST", "/friendrequest", friendrequestdata, function(response) {
    if(response["status"] == "SUCCESS") {
      document.getElementById("addfriendbtn").style.display="none";
    }
    //window.location.href="friendspage.html";
  });
}


