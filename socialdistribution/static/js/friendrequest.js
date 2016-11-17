//$(document).ready(function() {
//
////                  function getCookieid() {
////                    // look for the github_name in cookies
////                    var cookies = document.cookie.split(";");
////                    for(var i=0; i < cookies.length; i++) {
////                      var gname = cookies[i].split("=");
////                      if(gname[0] == "github_name") {
////                        return = gname[1];
////                      }
////                    }
////                    return "";
////                  }
////
//
//
//
//
//  var friendsTemplate = document.getElementById('friend-container');
//
////  var phname = friendsTemplate.content.querySelector("#thisusername");
////  phname.textContent = "Change";
////
////  var normalContent = document.getElementById('frequest');
////
////  var clonedTemplate = friendsTemplate.content.cloneNode(true);
////                  normalContent.appendChild(clonedTemplate)
//
//
//
//                  sendAJAX("GET", "/getFriendRequest", "", function(events) {
//                    for(var i=0; i < events.length; ++i) {
//
//                           friendsTemplate.content.querySelector("#thisusername").textContent = result[i].authorname;
//                           friendsTemplate.content.querySelector("#author2id").textContent = result[i].authorid;
//                           friendsTemplate.content.querySelector("#author2id").id = "author2id-" + i;
//                           friendsTemplate.content.querySelector("#profilepagelink").href = friendlink;
//
//                           var clonedTemplate = friendsTemplate.content.cloneNode(true);
//                           normalContent.appendChild(clonedTemplate)
//                    }
//
//                  });
//                  /*var text1 = "Changed1";
//                  var text2 = "Changed2";
//                  var text3 = "Changed3";
//                  var text4 = "Changed4";
//
//                  document.getElementsByName('username')[0].placeholder=text1;
//                  document.getElementsByName('displayName')[0].placeholder=text2;
//                  document.getElementsByName('githubid')[0].placeholder=text3;
//                  document.getElementsByName('bio')[0].placeholder=text4;*/
//});

$("#friend-accept").click(function(e) {

                    e.preventDefault();
                    //var friendsTemplate = document.getElementById('following-container');

//                          var friendsTemplate = document.getElementById('friend-container');
//
//                          var phname = friendsTemplate.content.querySelector("#thisusername");
//                          phname.textContent = "Change";
//
//                          var normalContent = document.getElementById('frequest');
//
//                          var clonedTemplate = friendsTemplate.content.cloneNode(true);
//                          normalContent.appendChild(clonedTemplate)

                          var acceptfrienddata = {};
                    acceptfrienddata["author_id"] = document.getElementById("author2id").textContent;



                    sendAJAX("POST", "http://127.0.0.1:5000/acceptFriendRequest", acceptfrienddata, function(response) {
                             console.log(response);
                             window.location.href="friendspage.html";

                    });
        });



$("#unfriend").click(function(e) {
                          
                          e.preventDefault();
                          //var friendsTemplate = document.getElementById('following-container');
                          
                          //                          var friendsTemplate = document.getElementById('friend-container');
                          //
                          //                          var phname = friendsTemplate.content.querySelector("#thisusername");
                          //                          phname.textContent = "Change";
                          //
                          //                          var normalContent = document.getElementById('frequest');
                          //
                          //                          var clonedTemplate = friendsTemplate.content.cloneNode(true);
                          //                          normalContent.appendChild(clonedTemplate)
                          
                          var acceptfrienddata = {};
                          acceptfrienddata["author_id"] = document.getElementById("author2id").textContent;
                          
                          
                          
                          sendAJAX("POST", "http://127.0.0.1:5000/unfriend", acceptfrienddata, function(response) {
                                   console.log(response);
                                   window.location.href="friendspage.html";
                                   
                                   });
                          });
