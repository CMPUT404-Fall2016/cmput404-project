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

$(document).ready(function() {

                  
  var myauthorid = getCookieid();
  var mypTemplate = document.getElementById('profiledatas');
  
  //var friendauthorid = getFriendcookieid();
  
  var myprofilelink = "/author/" + myauthorid;
  //var thisauthorlink = "/author/" + getFriendcookieid();
  //sendAJAX("GET",)
  
 
  
  sendAJAX("GET", myprofilelink, "", function(result) {
           
           console.log(result);
           var td = mypTemplate.content.querySelector("#profilehname");
           profileusernametext = result.displayName;
           td.textContent = profileusernametext;

           mypTemplate.content.querySelector("#profileid").textContent = result.id;
           
           mypTemplate.content.querySelector("#profiledname").textContent = result.displayName;
           
           mypTemplate.content.querySelector("#profilehost").textContent = result.host;
           
           mypTemplate.content.querySelector("#profileurl").textContent = result.url;
           
           var normalContent = document.getElementById('profile');
           
           var clonedTemplate = mypTemplate.content.cloneNode(true);
           normalContent.appendChild(clonedTemplate)
           
           document.getElementById("editprofilebtn").style.display="";
          
           
           document.getElementById("pid").placeholder = document.getElementById("profileid").textContent;
           //document.getElementById("pdn").placeholder = document.getElementById("profiledname").textContent;
           document.getElementById("pdn").value = document.getElementById("profiledname").textContent;
           
           document.getElementById("phost").placeholder = document.getElementById("profilehost").textContent;
           document.getElementById("purl").placeholder = document.getElementById("profileurl").textContent;
           
           
  });
                  
                  
});


$("#editprofilebtn").click(function (e) {
                           e.preventDefault();
                           
                           document.getElementById("testid").placeholder = document.getElementById("profileid").textContent;
                           document.getElementById("pdn").value = document.getElementById("profiledname").textContent;
                           
                           
                           });


//$("#saveprofilechange").click(function (e) {

                              //e.preventDefault();

function saveprofilechange() {
                              //                              var editprofiledata = {}
                              //                              editprofiledata["name"] = profileeditmode.elements["displayName"].value;
                              //                              editprofiledata["github_id"] = profileeditmode.elements["githubid"].value;
                              //                              editprofiledata["bio"] = editprofiledata.elements["bio"].value;
                              //
                              //                              sendAJAX("POST", "/editProfile", editprofiledata, function(response) {
                              //
                              //
                              //
                              //                                       });
                              
                              //var editprofileform = document.getElementById("editprofileform");
                              
                              //document.getElementById("profiledname").textContent = document.getElementById("pdn").value;
                              var editprofiledata = {}
                              editprofiledata["name"] = document.getElementById("pdn").value;
                              
                              
                              sendAJAX("POST", "/editProfile", editprofiledata, function(response) {
                                       console.log(response);
                                       console.log("edited?");
                                       document.getElementById("profiledname").textContent = document.getElementById("pdn").value;
                                       //document.getElementById("pdn").placeholder = document.getElementById("profiledname").textContent;
                                       document.getElementById("pdn").value = document.getElementById("profiledname").textContent;
                                       
                              });
                              
                              
                              
                              
                              }



//$("#addfriendbtn").click(function(e) {
function afriendone(fn) {
  var myuserid = getCookieid();
  
  var myinfostuff = "/author/" + myuserid;
  sendAJAX("GET", myinfostuff, "", function(result) {
           //console.log(result);
           //var myid = result.id;
           var myhost = result.host;
           //console.log(result.host)
           //console.log(myhost);
           var mydisplayname = result.displayName;
           fn(result);
           //return myhost, mydisplayname;
    });
}

afriendone(function(result) {
           console.log("hello");
           console.log(result);
           var myhost = result.host;
           //console.log(result.host)
           //console.log(myhost);
           var mydisplayname = result.displayName;
  });



//function afriendtwo() {
//  var friendid = getFriendcookieid();
//  var getfriendinfo = "/author/" + friendid;
//  //  var friendid="";
//  //  var friendhost="";
//  //  var frienddisplayname ="";
//  //  var friendurl="";
//  
//  sendAJAX("GET", getfriendinfo, "", function(result2) {
//           //console.log(result);
//           var friendid = result2.id;
//           var friendhost = result2.host;
//           var frienddisplayname = result2.displayName;
//           var friendurl = result2.url;
//           //return friendid, friendhost, frienddisplayname, friendurl;
//           fn(result2);
//           });
//}
//
//afriendtwo(function(result2) {
//           console.log("hello2");
//           console.log(result2);
//           var friendid = result2.id;
//           var friendhost = result2.host;
//           var frienddisplayname = result2.displayName;
//           var friendurl = result2.url;
//           });




//var result = foo();
//foo(function(result) {
//    // Code that depends on 'result'
//    });

function addFrienddata(resultone, resulttwo) {
  
  //return myhost, mydisplayname, friendid, friendhost, frienddisplayname, friendurl;
              
                              
}

//function myCallback(result) {
//  // Code that depends on 'result'
//}
//
//foo(myCallback);

var resultuser = addFrienddata();

function addFriend() {
  console.log(myhost);
  
//  var friendrequestdata = {};
//  friendrequestdata["author"] = {}
//  friendrequestdata["author"]["id"]= myuserid;
//  friendrequestdata["author"]["host"] = myhost;
//  friendrequestdata["author"]["displayName"] = mydisplayname;
//  
//  //  friendrequestdata["friend"]={"id":friendid, "host":friendhost, "displayName":frienddisplayname, "url":friendurl};
//  //console.log(friendrequestdata);
//  friendrequestdata["friend"] = {};
//  friendrequestdata["friend"]["id"] = friendid;
//  friendrequestdata["friend"]["host"] = friendhost;
//  friendrequestdata["friend"]["displayName"] = frienddisplayname;
//  friendrequestdata["friend"]["url"] = friendurl;
//  
//  
//  sendAJAX("POST", "/friendrequest", friendrequestdata, function(response) {
//           //console.log(response);
//           //window.location.href="friendspage.html";
//           });

  
}

