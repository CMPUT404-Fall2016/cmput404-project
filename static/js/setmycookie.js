function getCookieid() {
  // look for the github_name in cookies
  var cookies = document.cookie.split(";");
  for(var i=0; i < cookies.length; i++) {
    var gname = cookies[i].split("=");
    if(gname[0].trim() == "cookie_cmput404_author_id") {
      return gname[1];
    }
  }
  return "";
}

$("#author-dp-cookie").click(function(e){
                      e.preventDefault();
                      document.cookie = "request_author_id=" + getCookieid();
                      window.location.href = "profilepage.html";
                      
                      
                      
                      
                      });