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
      $("#create-btn").prop("disabled", true);
    } else {
      $("#match-alert").addClass("hidden");
      $("#create-btn").prop("disabled", false);
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
  xhr.setRequestHeader('Content-Type', 'application/json');
  console.log(message);
  xhr.send(message);
}


// encodes the form data as a json object and sends AJAX request
$("#create-btn").click(function () {

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
      login(message);

    // author already exists
    } else if (response["status"] == "DUPLICATE") {
      $("#duplicate-alert").prop("disabled", false);
    // what the fuck man
    } else {
      $("#server-alert").prop("disabled", false);
    }
  });
});

// stores commonly used data in local storage and redirects to index.html
function login(data) {
  localStorage.setItem(author_id, data["author_id"]);
  localStorage.setItem(display_name, data["display_name"]);
  localStorage.setItem(github_username, data["github_username"]);
  window.location.replace("/");
}

$("#login-btn").click(function() {

  var loginData = {};
  loginData["login_name"] = $("#login-form").find("input[name='username']").val();
  loginData["password"] = $("#login-form").find("input[name='password']").val();

  var message = JSON.stringify(loginData);

  // // debug
  // console.log(message);
  // return false;
  sendAJAX("POST", "/login", message, function(response) {

    // login is successful so log the user in
    if(response["status"] == "SUCCESS") {
      login(message);

    // username or password is incorrect
    } else if (response["status"] == "NO_MATCH") {
      $("#incorrect-alert").prop("disabled", true);

    // again, what the fUCK
    } else {
      $(".server-alert").prop("disabled");
    }
  });
});
