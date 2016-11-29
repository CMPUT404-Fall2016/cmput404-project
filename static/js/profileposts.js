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

// clear posts tab when user is on profile tab
$("#profiletab").click(function(e) {
                    e.preventDefault();
                    document.getElementById("posts").innerHTML = "";

                    });

// When user click post tab
$("#posttab").click(function(e) {
  e.preventDefault();
  var myauthorid = getCookieid();

  var myprofileposts = "/author/" + myauthorid + "/posts";

  var postList = document.getElementById("posts");
  var postTemplate = document.getElementById("post-container");
  // page=<Page_No>&size=<Page_Zize>
  sendAJAX("GET", myprofileposts, "", function(results) {
           console.log(results);
         // if not post are found
//         if (posts == "status : NO_MATCH") {
//              document.getElementById("posts").innerHTML = "";
//         }
//         // if post are found
//         else {
           for(var i=0; i < results.posts.length; ++i) {
           // fill the container with details
           postTemplate.content.querySelector(".post-title").textContent = results.posts[i].title;
           //console.log(results.posts[i].title);
           postTemplate.content.querySelector(".post-description").textContent = results.posts[i].description;
//           console.log(results.posts[i].description);
           postTemplate.content.querySelector(".post-author").textContent = results.posts[i].author.displayName;
//           console.log(results.posts[i].author.displayName);
           
           //postTemplate.content.querySelector(".post-content").textContent = posts[i].content;
           postTemplate.content.querySelector(".post-content").innerHTML = results.posts[i].content;

           // attach data to the links so it can be referenced when clicked
           var authorBtn = postTemplate.content.querySelector(".post-author");
           //$(authorBtn).data("post-author-id", posts[i].author_id);
           authorBtn.setAttribute("post-author-id", results.posts[i].author.id);
           //console.log(authorBtn);

           var commentsBtn = postTemplate.content.querySelector(".comments");
           commentsBtn.setAttribute("post-id", results.posts[i].id);

           var deletepostBtn = postTemplate.content.querySelector(".deletepost");
           deletepostBtn.setAttribute("delete-post-id", results.posts[i].id);

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
                window.location.href = "post.html";
          });

           // bind the onclick to set author id in localStorage
           // and link the user to the author's profile
           $(".post-author-url").click(function(e) {
               e.preventDefault();
               // set this for authorpage to use
               localStorage.setItem("fetch-author-id", $(this).attr("post-author-id"));
               window.location.href= "authorpage.html";
               });

           //$("#deletepost").click(function(e) {
           $(".deletepost").on('click', (function(e) {
                e.preventDefault();

                console.log("clicked");

                localStorage.setItem("delete-post-id", $(this).attr("delete-post-id"))
                deletepost();
                location.reload();

           }));
//         g}
   });
});


// delete the post
function deletepost() {
  var thispostid = localStorage.getItem("delete-post-id");
  var deletepostlink = "/posts/" + thispostid;

  sendAJAX("DELETE", deletepostlink, "", function(result) {
           console.log(result);
           //location.reload();
           });
}


// These are for changing post visibility
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
