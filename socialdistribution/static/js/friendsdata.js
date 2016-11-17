//function sendAJAX(method, url, message, session_id, callback) {
//  var xhr = new XMLHttpRequest();
//  xhr.open(method, url);
//  xhr.onreadystatechange = function(){
//    if (xhr.readyState==4) {
//      try {
//        if (xhr.status==200) {
//          if(callback) {
//            callback(JSON.parse(xhr.responseText));
//          }
//        }
//      }
//      catch(e) {
//        alert('Error: ' + e.name);
//      }
//    }
//  }
//  if(message) {
//    xhr.setHeader("Content-Type", "application/json");
//  }
//  xhr.send(JSON.stringify(message));
//}

$(document).ready(function() {
                  
                  function getCookieid() {
                    // look for the github_name in cookies
                    var cookies = document.cookie.split(";");
                    for(var i=0; i < cookies.length; i++) {
                      var gname = cookies[i].split("=");
                      if(gname[0] == "cookie_cmput404_author_id") {
                         return gname[1];
                      }
                    }
                    return "";
                  }
                  
                  var myauthorid = getCookieid();
                  
                  
//                  if (getCookieid() == myauthorid) {
//                    document.getElementById("editprofilebtn").style.display="";
//                  }
//                  else {
//                    document.getElementById("editprofilebtn").style.display="none";
//                  }
                  

  var friendsTemplate = document.getElementById('friends-container');
                  
                  var myauthorlink = "/author/" + myauthorid;
                  
                  
                  sendAJAX("GET", myauthorlink, "", function(events) {
                    for(var i=0; i < events.length; ++i) {
                           //var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
                           
                           friendsTemplate.content.querySelector("#friendid").href = result[i].friends[i].id;
                           friendsTemplate.content.querySelector("#friendhost").href = result[i].friends[i].host;
                           friendsTemplate.content.querySelector("#frienddisplayName").textContent = result[i].friends[i].displayName;
                           friendsTemplate.content.querySelector("#friendurl").href = result[i].friends[i].url;
                           
                           var normalContent = document.getElementById('friendstab');
                           

                  
//                  var friendsTemplate = document.getElementById('friends-container');
//                  
//                  var frienddatas = {};
//                  frienddatas["authorid"] = myauthorid;
//                  
//                  var myfriendlink = "/friends/" + myauthorid;
//                  
//                  sendAJAX("POST", myfriendlink, frienddatas, function(events) {
//                           for(var i=0; i < events.length; ++i) {
//                           
//                           var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
//                           
//                           sendAJAX("GET", "/authors", "", function(events) {
//                                    friendsTemplate.content.querySelector("#friendname").textContent = result[i].authorname;
//                                    friendsTemplate.content.querySelector("#friendnamelink").href = friendlink;
//                                    
//                                    var clonedTemplate = friendsTemplate.content.cloneNode(true);
//                                    normalContent.appendChild(clonedTemplate)
//                                    }
//                            }
//                                    
//                    });
                  /*var text1 = "Changed1";
                  var text2 = "Changed2";
                  var text3 = "Changed3";
                  var text4 = "Changed4";

                  document.getElementsByName('username')[0].placeholder=text1;
                  document.getElementsByName('displayName')[0].placeholder=text2;
                  document.getElementsByName('githubid')[0].placeholder=text3;
                  document.getElementsByName('bio')[0].placeholder=text4;*/
});

//$("#fingtab").click(function(e) {
//
//                    e.preventDefault();
//                    var friendsTemplate = document.getElementById('following-container');
//
//                    sendAJAX("GET", "/getFollowing", "", function(events) {
//                             for(var i=0; i < events.length; ++i) {
//                             var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
//                             friendsTemplate.content.querySelector("#friendname").textContent = result[i].authorname;
//                             friendsTemplate.content.querySelector("#friendnamelink").href = friendlink;
//
//                             var clonedTemplate = friendsTemplate.content.cloneNode(true);
//                             normalContent.appendChild(clonedTemplate)
//                             }
//
//                             });
//                    });

$("#fertab").click(function(e) {
                    e.preventDefault();
                    var friendsTemplate = document.getElementById('follower-container');

                    sendAJAX("GET", "/getFriendRequests", "", function(events) {
                             for(var i=0; i < events.length; ++i) {
                             var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
                             friendsTemplate.content.querySelector("#friendname").textContent = result[i].authorname;
                             friendsTemplate.content.querySelector("#friendnamelink").href = friendlink;

                             var clonedTemplate = friendsTemplate.content.cloneNode(true);
                             normalContent.appendChild(clonedTemplate)
                             }

                             });
//
//                   sendAJAX("GET", "/getFriendRequest", "", function(events) {
//                            for(var i=0; i < events.length; ++i) {
//
//                            friendsTemplate.content.querySelector("#thisusername").textContent = result[i].authorname;
//                            friendsTemplate.content.querySelector("#author2id").textContent = result[i].authorid;
//                            friendsTemplate.content.querySelector("#author2id").id = "author2id-" + i;
//                            friendsTemplate.content.querySelector("#profilepagelink").href = friendlink;
//
//                            var clonedTemplate = friendsTemplate.content.cloneNode(true);
//                            normalContent.appendChild(clonedTemplate)
//                            }
//
//                            });

                    });

$("#fdtab").click(function(e) {
                  e.preventDefault();
                   var friendsTemplate = document.getElementById('friends-container');

                   sendAJAX("GET", "/getFriends", "", function(events) {
                            for(var i=0; i < events.length; ++i) {
                            var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
                            friendsTemplate.content.querySelector("#friendname").textContent = result[i].authorname;
                            friendsTemplate.content.querySelector("#friendnamelink").href = friendlink;
                            
                            var normalContent = document.getElementById('friendstab');
                            
                            var clonedTemplate = friendsTemplate.content.cloneNode(true);
                            normalContent.appendChild(clonedTemplate)
                            }

                            });
                   });



$("#unfriendauthor").click(function(e) {
                   e.preventDefault();
                   
//                           var friendsTemplate = document.getElementById('friends-container');
//
//                           var normalContent = document.getElementById('friendstab');
//                           
//                           var clonedTemplate = friendsTemplate.content.cloneNode(true);
//                           normalContent.appendChild(clonedTemplate)
                   
                           sendAJAX("POST", "/unfriend", "", function(events) {
                   
                   });
                           });


