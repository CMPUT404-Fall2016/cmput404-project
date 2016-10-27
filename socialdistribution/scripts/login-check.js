$(document).ready(function() {

  // check all the cookies for an author_id, if not found then return false
  function loginCheck() {
    var cookies = document.cookie.split(";");
    for(var i=0; i < cookies.length; i++) {
      var cname = cookies[i].split("=");
      if(cname[0] == author_id) {
        return true;
      }
    }
    return false;
  }

  // if username isn't found in cookies, prompt login
  if(!loginCheck()) {
    window.location.href("/login");
  }
}