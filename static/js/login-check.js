/* INCLUDE THIS ON ALL PAGES THAT REQUIRE AUTHENTICATION
  index.html
  profilepage.html
  etc
  not author.html
*/

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
  if (authenticated == false) {
    window.location.href = "login.html";
  }
})();
