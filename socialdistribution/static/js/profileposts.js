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

//$(document).ready(function() {

$("#posttab").click(function(e) {

  e.preventDefault();
  var myauthorid = getCookieid();
  var mypTemplate = document.getElementById('post-container');
  
  //var friendauthorid = getFriendcookieid();
  
  var myprofileposts = "/author/" + myauthorid + "/posts";
  //var thisauthorlink = "/author/" + getFriendcookieid();
  //sendAJAX("GET",)
  
                    
 
  
  sendAJAX("GET", myprofileposts, "", function(result) {
           
           console.log(result);
           
  });
                
                  
                  
});


