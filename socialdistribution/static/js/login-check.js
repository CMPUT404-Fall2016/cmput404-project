(function() {
  // check cookies for an author_id, if not found then redirect user
  var cookies = document.cookie.split(";");
  for(var i=0; i < cookies.length; i++) {
    var cname = cookies[i].split("=");
    if(cname[0] == "cookie_cmput404") {
      return;
    }
  }
  window.location.replace("login.html");
})();
