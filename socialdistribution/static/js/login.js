var alert = document.getElementById("match-alert");
var password = document.getElementById("register-form").elements["password"];
var confirm = document.getElementById("register-form").elements["confirm"];
// function passwordCheck() {
//   if(password.value != confirm.value) {
//     alert("password do not match");
//     alert.className = "alert alert-danger";
//     return false;
//   } else {
//     return true;
//   }
// }
$(document).ready(function(){
  $("#password, #confirm").keyup(checkPassword);

});

function checkPassword() {
    if (password.value != confirm.value) {
      alert.className = "alert alert-danger";
      $("#create").prop("disabled", true);
    } else {
      alert.className = "alert alert-danger hidden";
      $("#create").prop("disabled", false);
    }
}
