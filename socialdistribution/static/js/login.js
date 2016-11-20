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
// encodes the form data as a json object and sends AJAX request
$("#create-btn").click(function (e) {

  e.preventDefault();
  var registerData = {}
  registerData["login_name"] = registerForm.elements["username"].value;
  registerData["name"] = registerForm.elements["displayName"].value;
  registerData["password"] = registerPassword.value;

  // // debug
  // console.log(message);
  // return false;
  sendAJAX("POST", "/register", registerData, function(response) {

    // server accepted the registration data, log the user in
    if(response["status"] == "SUCCESS") {
      login(response);

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
  localStorage.setItem("author_id", data["author_id"]);
  localStorage.setItem("display_name", data["name"]);
  // localStorage.setItem(github_username, data["github_username"]);
  window.location.href = "index.html";
}

// stores commonly used data in local storage and redirects to ADMIN
function login_admin() {
    // localStorage.setItem(author_id, data["author_id"]);
    // localStorage.setItem(display_name, data["display_name"]);
    // localStorage.setItem(github_username, data["github_username"]);
    window.location.href = "/admin/";
}

$("#admin-btn").click(function(e) {

  e.preventDefault();
  login_admin();
});



$("#login-btn").click(function(e) {

  e.preventDefault();
  var loginData = {};
  loginData["login_name"] = $("#login-form").find("input[name='username']").val();
  loginData["password"] = $("#login-form").find("input[name='password']").val();

  // // debug
  // console.log(message);
  // return false;
  sendAJAX("POST", "/login", loginData, function(response) {
    // console.log(response);
    // login is successful so log the user in
    if(response["status"] == "SUCCESS") {
      login(response);

    // login is Admin
    } else if (response["status"] == "ADMIN") {
      login_admin();

    // username or password is incorrect
    } else if (response["status"] == "NO_MATCH") {
      $("#incorrect-alert").prop("disabled", true);

    // again, what the fUCK
    } else {
      $(".server-alert").prop("disabled", false);
    }
  });
});
