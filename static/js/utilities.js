// MAKE SURE TO LOAD THIS BEFORE ANY OTHER SCRIPTS ON EACH PAGE

// check for authentication before anything else
(function() {
  // check cookies for an author_id, if not found then redirect user
  var cookies = document.cookie.split(";");
  var authenticated = false;
  for(var i=0; i < cookies.length; i++) {
    var cname = cookies[i].split("=");
    // console.log(cname[0].trim());
    if(cname[0].trim() == "cookie_cmput404_session_id") {
      authenticated = true;
      // console.log("authenticated!");
    }
  }

  // unauthenticated? send to login page
  if ((authenticated == false) && (window.location.pathname != "/login.html") {
    window.location.href = "login.html";
  }
  // already authenticated? send to index page
  else if ((authenticated == true) && (window.location.pathname == "/login.html")) {
    window.location.href = "index.html"
  }

  // load navbar unless on login page
  if (window.location.pathname != "/login.html") {
    $('#navbar').load('/navbar.html');
  }
})();

// standard AJAX request
function sendAJAX(method, url, message, callback) {
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
        console.log('Error: ' + e.name + " message: " + e.message);
      }
    }
  }
  // don't do foreign host if we're requesting from github
  if (url.split(".com")[0] != "https://api.github") {
    xhr.setRequestHeader('Foreign-Host', "false");
    xhr.setRequestHeader('Authorization', "Basic c2VydmVydG9zZXJ2ZXI6NjU0MzIx");
  }
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify(message));
}
