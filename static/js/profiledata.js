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

function getCookiehost() {
  // look for the github_name in cookies
  var cookies = document.cookie.split(";");
  for(var i=0; i < cookies.length; i++) {
    var gname = cookies[i].split("=");
    if(gname[0] == "cookie_cmput404_author_host") {
      return gname[1];
    }
  }
  return "";
}

function getFriendcookieid() {
  // look for the github_name in cookies
  var cookies = document.cookie.split(";");
  for(var i=0; i < cookies.length; i++) {
    var gname = cookies[i].split("=");
    if(gname[0] == "request_author_id") {
      return gname[1];
    }
  }
  return "";
}

$(document).ready(function() {


  var myauthorid = getCookieid();
  //var myauthorid = localStorage.getItem("author_id");
  var mypTemplate = document.getElementById('profiledatas');
                  console.log(myauthorid);

  var myprofilelink = "/author/" + myauthorid;
                  console.log(myprofilelink);

  sendAJAX("GET", myprofilelink, "", function(result) {

            console.log("called");

           console.log(result);
           var td = mypTemplate.content.querySelector("#profilehname");
           profileusernametext = result.displayName;
           td.textContent = profileusernametext;

           mypTemplate.content.querySelector("#profileid").textContent = result.id;

           mypTemplate.content.querySelector("#profiledname").textContent = result.displayName;

           mypTemplate.content.querySelector("#profilehost").textContent = result.host;

           mypTemplate.content.querySelector("#profileurl").textContent = result.url;

           mypTemplate.content.querySelector("#profilegithub_id").textContent = result.githubUsername;

           var normalContent = document.getElementById('profile');

           var clonedTemplate = mypTemplate.content.cloneNode(true);
           normalContent.appendChild(clonedTemplate)

           document.getElementById("editprofilebtn").style.display="";


           document.getElementById("pid").placeholder = document.getElementById("profileid").textContent;
           document.getElementById("pdn").value = document.getElementById("profiledname").textContent;

           document.getElementById("phost").placeholder = document.getElementById("profilehost").textContent;
           document.getElementById("purl").placeholder = document.getElementById("profileurl").textContent;
           document.getElementById("pgitid").value = document.getElementById("profilegithub_id").textContent;
  });



});

// Change the values in edit profile tab
$("#editprofilebtn").click(function (e) {
   e.preventDefault();

   document.getElementById("testid").placeholder = document.getElementById("profileid").textContent;
   document.getElementById("pdn").value = document.getElementById("profiledname").value;
   document.getElementById("pgitid").value = document.getElementById("profilegithub_id").value;


});

// Save the change made by user
function saveprofilechange() {

  var editprofiledata = {}
  editprofiledata["name"] = document.getElementById("pdn").value;
  editprofiledata["github_id"] = document.getElementById("pgitid").value;

  console.log(JSON.stringify(editprofiledata));
  localStorage.setItem("github_username", document.getElementById("pgitid").value);
  sendAJAX("POST", "/editProfile", editprofiledata, function(response) {
     console.log(response);
     localStorage.setItem("display_name", document.getElementById("pdn").value);
     localStorage.setItem("github_username", document.getElementById("pgitid").value);
     window.location.reload();
  });
}
