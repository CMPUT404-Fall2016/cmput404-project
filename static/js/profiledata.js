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

                  
  var myauthorid = getCookieid();
  //var myauthorid = localStorage.getItem("author_id");
  var mypTemplate = document.getElementById('profiledatas');
                  console.log(myauthorid);
  
  var myprofilelink = "/author/" + myauthorid;
                  console.log(myprofilelink);
 
  var headers = [["Foreign-Host", "false"], ["Authorization", "Basic c2VydmVydG9zZXJ2ZXI6NjU0MzIx"]];
  sendAJAX2(headers, "GET", myprofilelink, "", function(result) {
  //sendAJAX("GET", myprofilelink, "", function(result) {

            console.log("called");
           
           console.log(result);
           var td = mypTemplate.content.querySelector("#profilehname");
           profileusernametext = result.displayName;
           td.textContent = profileusernametext;

           mypTemplate.content.querySelector("#profileid").textContent = result.id;
           
           mypTemplate.content.querySelector("#profiledname").textContent = result.displayName;
           
           mypTemplate.content.querySelector("#profilehost").textContent = result.host;
           
           mypTemplate.content.querySelector("#profileurl").textContent = result.url;
           
           mypTemplate.content.querySelector("#profilegithub_id").textContent = result.githubUsername;
           
           var normalContent = document.getElementById('profile');
           
           var clonedTemplate = mypTemplate.content.cloneNode(true);
           normalContent.appendChild(clonedTemplate)
           
           document.getElementById("editprofilebtn").style.display="";
          
           
           document.getElementById("pid").placeholder = document.getElementById("profileid").textContent;
           document.getElementById("pdn").value = document.getElementById("profiledname").textContent;
           
           document.getElementById("phost").placeholder = document.getElementById("profilehost").textContent;
           document.getElementById("purl").placeholder = document.getElementById("profileurl").textContent;
           document.getElementById("pgitid").value = document.getElementById("profilegithub_id").textContent;
  });
                
                  
                  
});

// Change the values in edit profile tab
$("#editprofilebtn").click(function (e) {
                           e.preventDefault();
                           
                           document.getElementById("testid").placeholder = document.getElementById("profileid").textContent;
                           document.getElementById("pdn").value = document.getElementById("profiledname").value;
                           document.getElementById("pgitid").value = document.getElementById("profilegithub_id").value;
                           
                           
                           });


// Save the change made by user
function saveprofilechange() {

  var editprofiledata = {}
  editprofiledata["name"] = document.getElementById("pdn").value;
  editprofiledata["github_id"] = document.getElementById("pgitid").value;
  
  console.log(JSON.stringify(editprofiledata));
  localStorage.setItem("github_username", document.getElementById("pgitid").value);
  sendAJAX("POST", "/editProfile", editprofiledata, function(response) {
           console.log(response);
           localStorage.setItem("display_name", document.getElementById("pdn").value)
           window.location.reload();
           
  });
  
                              
                              
                              
                              }


