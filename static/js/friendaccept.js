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

$("#friend-accept").click(function() {
                          alert( "Clicked" );
                          console.log("clicked");
                          
                          });

function acceptfriend() {

                    //e.preventDefault();
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
//                    acceptfrienddata["author"] = document.getElementById("author2id").textContent;
  acceptfrienddata["author"] = localStorage.getItem("fetch-addfriend-id");
                acceptfrienddata["server_address"] = document.getElementById("requesthost").textContent;

  console.log(acceptfrienddata);
  
  var headers = [["Foreign_host", "false"]];
  
  sendAJAX2(headers, "POST", "acceptFriendRequest", acceptfrienddata, function(response) {
                    //sendAJAX("POST", "acceptFriendRequest", acceptfrienddata, function(response) {
                             console.log(response);
                             window.location.href="friendspage.html";

                    });
}

