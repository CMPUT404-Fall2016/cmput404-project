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
    if(gname[0].trim() == "request_author_id") {
      return gname[1];
    }
  }
  return "";
}


function editauthorpage() {
  document.getElementById("profiledname").textContent = document.getElementById("pdn").value;
  //document.getElementById("pdn").placeholder = document.getElementById("profiledname").textContent;
  document.getElementById("pdn").value = document.getElementById("profiledname").textContent;
}

$(document).ready(function() {
                  //var myauthorid = getCookieid();
                  var mypTemplate = document.getElementById('profiledatas');
                  
                  var friendauthorid = getFriendcookieid();
                  //var myprofilelink = "/author/" + myauthorid;
                  var thisauthorlink = "/author/" + getFriendcookieid();
                  console.log(getFriendcookieid());
                  
    sendAJAX("GET", thisauthorlink, "", function(result) {
         //console.log(result);
         var td = mypTemplate.content.querySelector("#profilehname");
         profileusernametext = result.displayName;
         td.textContent = profileusernametext;
         
         mypTemplate.content.querySelector("#profileid").textContent = result.id;
         
         mypTemplate.content.querySelector("#dprofiledname").textContent = result.displayName;
         
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
         
         document.getElementById("editprofilebtn").style.display="none";
         //document.getElementById("addfriendbtn").style.display="";
    });
                  
                
});

$("#saveprofilechange").click(function (e) {

      e.preventDefault();
      var editprofiledata = {}
      editprofiledata["name"] = editprofiledata.elements["displayName"].value;
      editprofiledata["github_id"] = editprofiledata.elements["githubid"].value;
      editprofiledata["bio"] = editprofiledata.elements["bio"].value;
      
      sendAJAX("POST", "/editProfile", editprofiledata, function(response) {
               
               
               
      });
                              
});


function afriendone() {
  var myuserid = getCookieid();
  
  var myinfostuff = "/author/" + myuserid;
  sendAJAX("GET", myinfostuff, "", function(result) {
           //console.log(result);
           //var myid = result.id;
           var myinfodatacombine = {}
           myinfodatacombine.myhost = result.host;
           myinfodatacombine.mydisplayname = result.displayName;
//           var myhost = result.host;
//           var mydisplayname = result.displayName;
           //fn(myinfodatacombine);
           
           var friendid = getFriendcookieid();
           var getfriendinfo = "/author/" + friendid;
           
           sendAJAX("GET", getfriendinfo, "", function(result2) {
                    //console.log(result);
                    var myinfodatacombine = {}
                    console.log(result.displayName);
                    myinfodatacombine.myhost = result.host;
                    myinfodatacombine.mydisplayname = result.displayName;
                    console.log("<<");
                    console.log(result.displayName);
                    console.log(">>");
                    myinfodatacombine.friendid = result2.id;
                    myinfodatacombine.friendhost = result2.host;
                    myinfodatacombine.frienddisplayname = result2.displayName
                    myinfodatacombine.friendurl = result2.url;
                    
                    //               var friendid = result2.id;
                    //               var friendhost = result2.host;
                    //               var frienddisplayname = result2.displayName;
                    //               var friendurl = result2.url;
                    //return friendid, friendhost, frienddisplayname, friendurl;
                    afriendtwo(myinfodatacombine);
            });
    });
}

function afriendtwo(result) {
           console.log("hello");
           console.log(result);
           console.log("result1done");
           //var myhost = result.host;
           //console.log(result.host)
           //console.log(myhost);
           //var mydisplayname = result.displayName;
           var friendrequestdata = {};
             friendrequestdata["author"] = {}
           friendrequestdata["author"]["id"]= getCookieid();;
             friendrequestdata["author"]["host"] = result.myhost;
             friendrequestdata["author"]["displayName"] = result.mydisplayname;
           
             //  friendrequestdata["friend"]={"id":friendid, "host":friendhost, "displayName":frienddisplayname, "url":friendurl};
             //console.log(friendrequestdata);
             friendrequestdata["friend"] = {};
             friendrequestdata["friend"]["id"] = result.friendid;
             friendrequestdata["friend"]["host"] = result.friendhost;
             friendrequestdata["friend"]["displayName"] = result.frienddisplayname;
             friendrequestdata["friend"]["url"] = result.friendurl;
  console.log("<<");
  console.log(result.mydisplayName);
  
  console.log(friendrequestdata);
  console.log(">>");
  
             sendAJAX("POST", "/friendrequest", friendrequestdata, function(response) {
                      console.log(response);
                      if(response["status"] == "SUCCESS") {
                      

                      document.getElementById("addfriendbtn").style.display="none";
                      }
                      //window.location.href="friendspage.html";
            });
}












