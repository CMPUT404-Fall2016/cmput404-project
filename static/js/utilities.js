// MAKE SURE TO LOAD THIS BEFORE ANY OTHER SCRIPTS ON EACH PAGE

// load navbar unless facing login page
$(document).ready(function(){
  if (window.location.href != "login.html") {
    $('#navbar').load('/navbar.html');
  }
});

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
