$(document).ready(function() {

  // searches cookies for a github_username
  // debug
  // document.cookie = "github_name=stat3kk; expires=Thu, 18 Dec 2018 12:00:00 UTC";
  function getGithubUsername() {
    // look for the github_name in cookies
    var cookies = document.cookie.split(";");
    for(var i=0; i < cookies.length; i++) {
      var gname = cookies[i].split("=");
      if(gname[0] == "github_name") {
        return gname[1];
      }
    }
    return "";
  }

  // this is the author's github_username, empty string if there isn't one
  var github_name = localStorage.getItem("github_username"),
      github_url = "https://api.github.com/users/" + github_name + "/events",
      sidebar = document.getElementById("github"),
      githubTemplate = document.getElementById("github-container");

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
      xhr.setHeader("Content-Type", "application/json");
    }
    xhr.send(JSON.stringify(message));
  }

  // get the events and process them to be displayed in github-containers
  if(github_name) {
    sendAJAX("GET", github_url, "", function(events) {
      for(var i=0; i < events.length; ++i) {
        var repo_url = "https://github.com/" + result[i].repo.name;

        // fill the container with details
        githubTemplate.content.querySelector(".github-type").innerHTML = result[i].type;
        githubTemplate.content.querySelector(".github-dp").href = result[i].actor.url;
        githubTemplate.content.querySelector(".github-repo-url").href = repo_url;
        githubTemplate.content.querySelector(".github-repo-url").innerHTML = repo_url;
        githubTemplate.content.querySelector(".github-date").innerHTML = result[i].created_at;

        // clone the template to render and append to the dom
        var clone = document.importNode(githubTemplate.content, true);
        sidebar.appendChild(clone);
      }
    });
  }
});
