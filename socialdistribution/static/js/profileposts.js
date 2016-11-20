function sendAJAX(method, url, message, callback) {
  var xhr = new XMLHttpRequest();
  xhr.open(method, url);
  xhr.onreadystatechange = function(){
    if (xhr.readyState==4) {
      try {
        if (xhr.status==200) {
          if(callback) {
            callback(JSON.parse(xhr.responseText));
          }
        }
      }
      catch(e) {
        alert('Error: ' + e.name);
      }
    }
  }
  //  if(message) {
  //    xhr.setHeader("Content-Type", "application/json");
  //  }
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify(message));
}

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
    if(gname[0] == "request_author_id") {
      return gname[1];
    }
  }
  return "";
}


//function editauthorpage() {
//  document.getElementById("profiledname").textContent = document.getElementById("pdn").value;
//  //document.getElementById("pdn").placeholder = document.getElementById("profiledname").textContent;
//  document.getElementById("pdn").value = document.getElementById("profiledname").textContent;
//}

//$(document).ready(function() {

$("#posttab").click(function(e) {

  e.preventDefault();
  var myauthorid = getCookieid();
  var mypTemplate = document.getElementById('post-container');
  
  //var friendauthorid = getFriendcookieid();
  
  var myprofileposts = "/author/" + myauthorid + "/posts";
  //var thisauthorlink = "/author/" + getFriendcookieid();
  //sendAJAX("GET",)
  
      
  //var postList = document.getElementById("posts");
  var postTemplate = document.getElementById("post-container");
  // page=<Page_No>&size=<Page_Zize>
  sendAJAX("GET", myprofileposts, "", function(posts) {
           console.log(posts);
      for(var i=0; i < posts.length; ++i) {
           // fill the container with details
           postTemplate.content.querySelector(".post-title").textContent = posts[i].title;
           postTemplate.content.querySelector(".post-description").textContent = posts[i].description;
           postTemplate.content.querySelector(".post-author").textContent = posts[i].author.displayname;
           postTemplate.content.querySelector(".post-content").textContent = posts[i].content;
           postTemplate.content.querySelector("#postid").textContent = posts[i].id;
           
           // attach data to the links so it can be referenced when clicked
           var deletepostBtn = postTemplate.content.querySelector("#deletepost");
           $(deletepostBtn).data("this-post-id", posts[i].id);
           console.log(deletepostBtn);
           
//           var commentsBtn = postTemplate.content.querySelector(".comments");
//           $(commentsBtn).data("post-host", posts[i].author.host);
//           $(commentsBtn).data("post-id", posts[i].id);
           
           var clone = document.importNode(postTemplate.content, true);
           postList.appendChild(clone);
           }
           
           $("#deletepost").click(function(e) {
                                  
                                  e.preventDefault();
                                  
                                  localStorage.setItem("delete-post-id", $(this).data("this-post-id"))
                                  
                                  var thispostid = localStorage.getItem("delete-post-id");
                                  var deletepostlink = "/deleteposts/" + thispostid;
                                  
                                  sendAJAX("POST", deletepostlink, "", function(result) {
                                           console.log(result);
                                           });
                                  });
           });
 
  
//  sendAJAX("GET", myprofileposts, "", function(result) {
//           
//           console.log(result);
//           
//  });
//                
                  
                  
});


$("#deletepost").click(function(e) {
                    
                  e.preventDefault();
                       
                       var thispostid = document.getElementById("postid").textContent
                       var deletepostlink = "/deleteposts/" + thispostid;
                       
                  sendAJAX("POST", deletepostlink, "", function(result) {
                       console.log(result);
                  });
});

//$("#postpublic").click(function(e) {
//                       
//                       e.preventDefault();
//                       
//                       
//                       var thispostid = document.getElementById("postid").textContent
//                       var postlink = "/posts/" + thispostid;
//                       
//                       var postvisibility = {}
//                       postvisibility["posts"]["visiibility"] = "PUBLIC";
//                       
//                       
//                       sendAJAX("POST", postlink, postvisibility, function(result) {
//                                console.log(result);
//                                });
//                       
//                       });
//
//
//$("#postonlyme").click(function(e) {
//                    
//                    e.preventDefault();
//                       
//                       var thispostid = document.getElementById("postid").textContent
//                       var postlink = "/posts/" + thispostid;
//                       
//                       var postvisibility = {}
//                       postvisibility["posts"]["visiibility"] = "PRIVATE";
//                       
//                       sendAJAX("POST", postlink, postvisibility, function(result) {
//                                console.log(result);
//                                });
//                    
//                    });
//
//$("#postmyfriend").click(function(e) {
//                    
//                    e.preventDefault();
//                         
//                         var thispostid = document.getElementById("postid").textContent
//                         var postlink = "/posts/" + thispostid;
//                         
//                         var postvisibility = {}
//                         postvisibility["posts"]["visiibility"] = "FRIENDS";
//                         sendAJAX("POST", postlink, postvisibility, function(result) {
//                                  console.log(result);
//                                  });
//                    
//                         });
//
//$("#postfoaf").click(function(e) {
//                    
//                    e.preventDefault();
//                     
//                     var thispostid = document.getElementById("postid").textContent
//                     var postlink = "/posts/" + thispostid;
//                     var postvisibility = {}
//                     postvisibility["posts"]["visiibility"] = "FOAF";
//                     
//                     sendAJAX("POST", postlink, postvisibility, function(result) {
//                              console.log(result);
//                              });
//                    
//                     });
//
//$("#postfsamehost").click(function(e) {
//                    
//                    e.preventDefault();
//                          
//                          var thispostid = document.getElementById("postid").textContent
//                          var postlink = "/posts/" + thispostid;
//                          var postvisibility = {}
//                          postvisibility["posts"]["visiibility"] = "SERVERONLY";
//                          sendAJAX("POST", postlink, postvisibility, function(result) {
//                                   console.log(result);
//                                   });
//                    
//                          });




























