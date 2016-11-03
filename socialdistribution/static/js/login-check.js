$(document).ready(function() {

  var authorId = function() {
    // checks cookies for an author_id, if not found then redirect user
    var cookies = document.cookie.split(";");
    for(var i=0; i < cookies.length; i++) {
      var cname = cookies[i].split("=");
      if(cname[0] == "cookie_cmput404") {
        return cname[1];
      }
    }
    // if username isn't found in cookies, prompt login
    window.location.href("login.html");
  }
});
