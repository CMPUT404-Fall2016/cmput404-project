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

function getCookieid() {
  var cookies = document.cookie.split(";");
  for(var i=0; i < cookies.length; i++) {
    var gname = cookies[i].split("=");
    if(gname[0].trim() == "cookie_cmput404_author_id") {
      return gname[1];
      
    }
  }
  return "";
}

$(document).ready(function() {
                  
                  
                  
                  var myauthorid = getCookieid();
                  console.log(getCookieid());
                  
                  
//                  if (getCookieid() == myauthorid) {
//                    document.getElementById("editprofilebtn").style.display="";
//                  }
//                  else {
//                    document.getElementById("editprofilebtn").style.display="none";
//                  }
                  

  //var friendsTemplate = document.getElementById('friends-container');
                  
                  //var myauthorlink = "/author/52ec225c39b24d6896ffba3176e71a37";// + myauthorid;
                  var myauthorlink = "/author/" + myauthorid;
                   //console.log(myauthorlink);
                  
                  sendAJAX("GET", myauthorlink, "", function(events) {
                           console.log("this?");
                           console.log(events);
                    for(var i=0; i < events.length; ++i) {
                           //var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
                           var friendsTemplate = document.getElementById('friends-container');
                           friendsTemplate.content.querySelector("#friendid").href = events.friends[i].id;
                           friendsTemplate.content.querySelector("#friendhost").href = events.friends[i].host;
                           friendsTemplate.content.querySelector("#frienddisplayName").textContent = events.friends[i].displayName;
                           friendsTemplate.content.querySelector("#friendurl").href = events.friends[i].url;
                           
                           var normalContent = document.getElementById('friendstab');
                           
                           var clonedTemplate = friendsTemplate.content.cloneNode(true);
                           normalContent.appendChild(clonedTemplate);
                           
                           }
                  });
                  
                  sendAJAX("GET", "/getFriendRequests", "", function(events) {
                           console.log(events);
                           console.log(events.friendRequestList[0].fromAuthor_id);
                           console.log(events.friendRequestList.length);
                           for(var i=0; i < events.friendRequestList.length; ++i) {
                           var requestTemplate = document.getElementById('request-container');
                           //friendRequestList.content.querySelector("#friend-accept").value = "btn"+i;
                           //var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
                           requestTemplate.content.querySelector("#thisusername").textContent = events.friendRequestList[i].fromAuthor_id;
                           requestTemplate.content.querySelector("#profilepagelink").href = events.friendRequestList[i].url;
                           requestTemplate.content.querySelector("#author2id").textContent = events.friendRequestList[i].fromAuthor_id;
                           
                           var normalContent = document.getElementById('frequest');
                           
                           var clonedTemplate = requestTemplate.content.cloneNode(true);
                           normalContent.appendChild(clonedTemplate);
                           }
                           
                           });
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
//                   var requestTemplate = document.getElementById('request-container');
//                   //var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
//                   requestTemplate.content.querySelector("#thisusername").textContent = "123";
//                   requestTemplate.content.querySelector("#profilepagelink").href = "#";
//                   requestTemplate.content.querySelector("#author2id").textContent = "";
//                   
//                   var normalContent = document.getElementById('frequest');
//                   
//                   var clonedTemplate = requestTemplate.content.cloneNode(true);
//                   normalContent.appendChild(clonedTemplate);
                   
//                   sendAJAX("GET", "/getFriendRequests", "", function(events) {
//                            console.log(events);
//                            console.log(events.friendRequestList[0].fromAuthor_id);
//                            console.log(events.friendRequestList.length);
//                        for(var i=0; i < events.friendRequestList.length; ++i) {
//                            var requestTemplate = document.getElementById('request-container');
//                            //var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
//                            requestTemplate.content.querySelector("#thisusername").textContent = events.friendRequestList[i].fromAuthor_id;
//                            requestTemplate.content.querySelector("#profilepagelink").href = events.friendRequestList[i].url;
//                            requestTemplate.content.querySelector("#author2id").textContent = events.friendRequestList[i].fromAuthor_id;
//                            
//                            var normalContent = document.getElementById('frequest');
//                            
//                            var clonedTemplate = requestTemplate.content.cloneNode(true);
//                            normalContent.appendChild(clonedTemplate);
//                        }
//                            
//                  });
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
                  var myauthorlink = "/author/" + getCookieid();
                  
                  sendAJAX("GET", myauthorlink, "", function(events) {
                           for(var i=0; i < events.length; ++i) {
                         
                                                      //var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
                           
                            friendsTemplate.content.querySelector("#friendid").href = result[i].friends[i].id;
                            friendsTemplate.content.querySelector("#friendhost").href = result[i].friends[i].host;
                            friendsTemplate.content.querySelector("#frienddisplayName").textContent = result[i].friends[i].displayName;
                           friendsTemplate.content.querySelector("#friendurl").href = result[i].friends[i].url;
                           
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


