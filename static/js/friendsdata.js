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
    //    console.log(headers[i][0] + headers[i][1]);
  }
  xhr.send(JSON.stringify(message));
}

$(document).ready(function() {
                  
                  
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
                  
                  var myauthorid = getCookieid();
                  //console.log(getCookieid());
                  
                  
                  //var myauthorlink = "/author/52ec225c39b24d6896ffba3176e71a37";// + myauthorid;
                  var myauthorlink = "/author/" + myauthorid;
                   //console.log(myauthorlink);
                  var headers = [["Foreign-Host", "false"]];
                  //sendAJAX("GET", myauthorlink, "", function(events) {
                  sendAJAX2(headers, "GET", myauthorlink, "", function(events) {
                            
                            //sendAJAX("GET", myauthorlink, "", function(events) {
                            //                           console.log("this?");
                            console.log(events.friends);
                            //                           console.log(events.friends.length);
                            //                           console.log(events.friends[0]);
                            //                           console.log(">>>");
                            for(var i=0; i < events.friends.length; ++i) {
                            //var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
                            var friendsTemplate = document.getElementById('friends-container');
                            friendsTemplate.content.querySelector("#friendid").textContent = events.friends[i].id;
                            friendsTemplate.content.querySelector("#friendhost").textContent = events.friends[i].host;
                            friendsTemplate.content.querySelector("#frienddisplayName").textContent = events.friends[i].displayName;
                            console.log(events.friends[i].displayName);
                            //console.log(events.friends[i].displayName);
                            friendsTemplate.content.querySelector("#friendurl").href = events.friends[i].url;
                            
                            document.cookie = "request_author_id="+events.friends[i].id;
                            
                            friendsTemplate.content.querySelector("#friendp1link").href = "authorpage.html";
                            //friendsTemplate.content.querySelector("#friendp2link").href = "authorpage.html";
                            
                            var unfriendbtn = friendsTemplate.content.querySelector("#unfriendauthor");
                            unfriendbtn.name = events.friends[i].id;
                            unfriendbtn.setAttribute("friendhostname", events.friends[i].host);
                            
                            //console.log(">>>>");
                            //console.log(events.friends[i].host);
                            console.log(unfriendbtn);
                            
                            
                            var normalContent = document.getElementById('friendstab');
                            
                            var clonedTemplate = friendsTemplate.content.cloneNode(true);
                            normalContent.appendChild(clonedTemplate);
                            
                            
                            
                            }
                            
                            $(".unfriendauthor").click(function (e) {
                                                       
                                                       e.preventDefault();
                                                       
                                                       localStorage.setItem("fetch-unfriend-id", $(this).attr("name"));
                                                       localStorage.setItem("fetch-unfriend-host", $(this).attr("friendhostname"));
                                                       unfriendauthor();
                                                       
                                                       });
                            });            
                  

});


$("#reqtab").click(function(e) {
                   e.preventDefault();
                   
                   var headers = [["Foreign-Host", "false"]];
                   //sendAJAX("GET", myauthorlink, "", function(events) {
                   
                 //  sendAJAX("GET", "/getFriendRequests", "", function(events) {
                  sendAJAX2(headers, "GET", "/getFriendRequests", "", function(events) {
                            console.log(events);
                            //console.log(events.friendRequestList[0].fromAuthor_id);
                            console.log(events.friendRequestList.length);
                            for(var i=0; i < events.friendRequestList.length; ++i) {
                            var requestTemplate = document.getElementById('request-container');
                            requestTemplate.content.querySelector("#thisusername").textContent = events.friendRequestList[i].fromAuthorDisplayName;
                            requestTemplate.content.querySelector("#profilepagelink").href = events.friendRequestList[i].url;
                            requestTemplate.content.querySelector("#requesthost").textContent = events.friendRequestList[i].fromServerIP;
                            //console.log(events.friendRequestList[i].fromServerIP);
                            requestTemplate.content.querySelector("#author2id").textContent = events.friendRequestList[i].fromAuthor_id;
                            
                            
                            var addingfriendbtn = requestTemplate.content.querySelector("#friend-accept");
                            addingfriendbtn.name = events.friendRequestList[i].fromAuthor_id;
                            
                            console.log("<<<");
                            console.log(addingfriendbtn);
                            console.log(">>>");
                            
                            var normalContent = document.getElementById('frequest');
                            
                            var clonedTemplate = requestTemplate.content.cloneNode(true);
                            normalContent.appendChild(clonedTemplate);
                            }
                            
                            
                            $(".friend-accept").click(function (e) {
                                                      
                                                      e.preventDefault();
                                                      
                                                      localStorage.setItem("fetch-addfriend-id", $(this).attr("name"));
                                                      acceptfriend();
                                                      
                                                      });
                            
                            
                            });
                   document.getElementById("friendstab").innerHTML = "";
                    });

function acceptfriend() {
  
  var acceptfrienddata = {};
  //                    acceptfrienddata["author"] = document.getElementById("author2id").textContent;
  acceptfrienddata["author"] = localStorage.getItem("fetch-addfriend-id");
  acceptfrienddata["server_address"] = document.getElementById("requesthost").textContent;
  
  console.log(acceptfrienddata);
  
  var headers = [["Foreign-Host", "false"]];
  
  sendAJAX2(headers, "POST", "acceptFriendRequest", acceptfrienddata, function(response) {
            //sendAJAX("POST", "acceptFriendRequest", acceptfrienddata, function(response) {
            console.log(response);
            window.location.href="friendspage.html";
            
            });
}



$("#fdtab").click(function(e) {
                  e.preventDefault();
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
                  
                  var myauthorid = getCookieid();
                  var myauthorlink = "/author/" + myauthorid;
                  console.log(myauthorlink);
                  
                  var headers = [["Foreign-Host", "false"]];
                  //sendAJAX("GET", myauthorlink, "", function(events) {
                  sendAJAX2(headers, "GET", myauthorlink, "", function(events) {
                  
                  //sendAJAX("GET", myauthorlink, "", function(events) {
                           //                           console.log("this?");
                           console.log(events.friends);
                           //                           console.log(events.friends.length);
                           //                           console.log(events.friends[0]);
                           //                           console.log(">>>");
                           for(var i=0; i < events.friends.length; ++i) {
                           //var friendlink = "http://127.0.0.1:5000/author/" + result[i].authorid;
                           var friendsTemplate = document.getElementById('friends-container');
                           friendsTemplate.content.querySelector("#friendid").textContent = events.friends[i].id;
                           friendsTemplate.content.querySelector("#friendhost").textContent = events.friends[i].host;
                           friendsTemplate.content.querySelector("#frienddisplayName").textContent = events.friends[i].displayName;
                           console.log(events.friends[i].displayName);
                           //console.log(events.friends[i].displayName);
                           friendsTemplate.content.querySelector("#friendurl").href = events.friends[i].url;
                           
                           document.cookie = "request_author_id="+events.friends[i].id;
                           
                           friendsTemplate.content.querySelector("#friendp1link").href = "authorpage.html";
                           //friendsTemplate.content.querySelector("#friendp2link").href = "authorpage.html";
                           
                           var unfriendbtn = friendsTemplate.content.querySelector("#unfriendauthor");
                           unfriendbtn.name = events.friends[i].id;
                            unfriendbtn.setAttribute("friendhostname", events.friends[i].host);
                           
                            //console.log(">>>>");
                           //console.log(events.friends[i].host);
                            console.log(unfriendbtn);
                           
                           
                           var normalContent = document.getElementById('friendstab');
                           
                           var clonedTemplate = friendsTemplate.content.cloneNode(true);
                           normalContent.appendChild(clonedTemplate);
                           
                           
                           
                           }
                           
                           $(".unfriendauthor").click(function (e) {
                                                      
                                                      e.preventDefault();
                                                      
                                                      localStorage.setItem("fetch-unfriend-id", $(this).attr("name"));
                                                      localStorage.setItem("fetch-unfriend-host", $(this).attr("friendhostname"));
                                                      unfriendauthor();
                                                      
                                                      });
                           });

                  document.getElementById("frequest").innerHTML = "";
  });


//$("#friend-accept").click(function (e) {
//                        
//                        e.preventDefault();
//                        
//                        locatStorage.setItem("fetch-addfriend-id", $(this).attr("name"));
//                        
//                        });





//$("#unfriendauthor").click(function(e) {
//                           
//                   e.preventDefault();
function unfriendauthor() {
                           //alert("hello");
                           console.log("btnwork");

//                           var friendsTemplate = document.getElementById('friends-container');
//
//                           var normalContent = document.getElementById('friendstab');
//                           
//                           var clonedTemplate = friendsTemplate.content.cloneNode(true);
//                           normalContent.appendChild(clonedTemplate)
                           //console.log(document.getElementById("friendhost").href);
                   
                           var unfrienddata = {};
                           //unfrienddata["author"] = document.getElementById("friendid").textContent;
  unfrienddata["author"] = localStorage.getItem("fetch-unfriend-id");
  unfrienddata["server_address"] = localStorage.getItem("fetch-unfriend-host");
  
                           console.log(unfrienddata);
   var headers = [["Foreign-Host", "false"]];
  sendAJAX2(headers, "POST", "/unFriend", unfrienddata, function(response) {
                           
                           //sendAJAX("POST", "/unFriend", unfrienddata, function(response) {
                                    console.log("hello");
                                    console.log(response);
                                    window.location.href="friendspage.html";
                                    
                                    });
                           
                           }


