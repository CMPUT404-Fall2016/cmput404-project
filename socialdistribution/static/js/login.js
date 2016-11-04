const registerForm = document.getElementById("register-form");
const registerPassword = registerForm.elements["password"];
const registerConfirm = registerForm.elements["confirm"];
const loginForm = document.getElementById("login-form");

// checks the passwords for a match whenever the user types
$(document).ready(function(){
  $("#registerPassword, #registerConfirm").keyup(checkPassword);
});

// disable the submit button if the passwords do not match
function checkPassword() {
    if (registerPassword.value != registerConfirm.value) {
      $("#match-alert").removeClass("hidden");
      $("#create").prop("disabled", true);
    } else {
      $("#match-alert").addClass("hidden");
      $("#create").prop("disabled", false);
    }
}

// standard AJAX request
function sendAJAX(method, url, message, session_id, callback) {
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
  if(message) {
    xhr.setRequestHeader("Content-Type", "application/json");
  }
  xhr.send(JSON.stringify(message));
}


// encodes the form data as a json object and sends AJAX request
$("#create").click(function () {

  var registerData = {}
  registerData["login_name"] = registerForm.elements["username"].value;
  registerData["name"] = registerForm.elements["displayName"].value;
  registerData["password"] = registerPassword.value;

  var message = JSON.stringify(registerData);
  // // debug
  // console.log(message);
  // return false;
  sendAJAX("POST", "/register", message, function(response) {

    // server accepted the registration data, log the user in
    if(response["status"] == "SUCCESS") {
      localStorage.setItem(author_id, response["author_id"]);
      localStorage.setItem(display_name, response["display_name"]);
      localStorage.setItem(github_username, response["github_username"]);
      window.location.replace("/");

    // author exists in the database
    } else if (response == "DUPLICATE") {
      $("#duplicate-alert").className = "alert alert-danger alert-dismissible";

    // what the fuck man
    } else {
      $("#server-alert").className = "alert alert-danger";
    }
  });
});
