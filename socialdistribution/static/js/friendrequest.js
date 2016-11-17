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



//$("#unfriend").click(function(e) {
//                          
//                          e.preventDefault();
//                          //var friendsTemplate = document.getElementById('following-container');
//                          
//                          //                          var friendsTemplate = document.getElementById('friend-container');
//                          //
//                          //                          var phname = friendsTemplate.content.querySelector("#thisusername");
//                          //                          phname.textContent = "Change";
//                          //
//                          //                          var normalContent = document.getElementById('frequest');
//                          //
//                          //                          var clonedTemplate = friendsTemplate.content.cloneNode(true);
//                          //                          normalContent.appendChild(clonedTemplate)
//                          
//                          var acceptfrienddata = {};
//                          acceptfrienddata["author_id"] = document.getElementById("author2id").textContent;
//                          
//                          
//                          
//                          sendAJAX("POST", "http://127.0.0.1:5000/unfriend", acceptfrienddata, function(response) {
//                                   console.log(response);
//                                   window.location.href="friendspage.html";
//                                   
//                                   });
//                          });
