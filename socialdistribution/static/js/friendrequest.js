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



//
//$(document).ready(function() {
//
//                  var myTemplate = document.getElementById('profiledatas');
//
////                  var displaynameh = document.getElementById('profilehname');
////                  var displaynameb = document.getElementById('profileusername');
////                  var pname = document.getElementById('profilename');
////                  var githubid = document.getElementById('profilegethubid');
////                  var pbio = document.getElementById('profilebio');
//
//                  var pu = myTemplate.content.querySelector(".profilehname");
//                  pu.textContent = "This is the changed pname";
//
//                  var pu = myTemplate.content.querySelector(".profileusername");
//                  pu.textContent = "This is the changed username";
//
//                  var pn = myTemplate.content.querySelector(".profilename");
//                  pn.textContent = "This is the changed name";
//
//                  var pg = myTemplate.content.querySelector(".profilegithubid");
//                  pg.textContent = "This is the changed github id";
//
//                  var pb = myTemplate.content.querySelector(".profilebio");
//                  pb.textContent = "This is the changed bio";
//
//                  var normalContent = document.getElementById('profile');
//
//                  var clonedTemplate = myTemplate.content.cloneNode(true);
//                  normalContent.appendChild(clonedTemplate)
//});
