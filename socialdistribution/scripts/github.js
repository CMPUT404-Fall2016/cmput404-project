$(document).ready(function() {

  // this is the author's github_username, empty string if there isn't one
  var github_name = "";

  //debug
  // document.cookie = "github_name=stat3kk; expires=Thu, 18 Dec 2018 12:00:00 UTC";

  (function getGithubUsername() {
    // look for the github_name in cookies
    var cookies = document.cookie.split(";");
    for(var i=0; i < cookies.length; i++) {
      var gname = cookies[i].split("=");
      if(gname[0] == "github_name") {
        github_name = gname[1];
        return;
      }
    }
    // // if not found, query the DB for it
    // sendAJAX("GET", "http://service/author/github_username", "", function(text) {
    //   username = JSON.parse(text);
    //   console.log(username);
    //   if(username) {
    //     return username;
    //   } else {
    //     return "";
    //   }
    // });
  })();

  var github_url = "https://api.github.com/users/" + github_name + "/events";

  var postContainer = document.getElementById("posts");
  var githubContainer = document.getElementById("github-container");

  // standard AJAX request
  function sendAJAX(method, url, message, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url);
    xhr.onreadystatechange = function(){
      if (xhr.readyState==4) {
        try {
          if (xhr.status==200) {
            if(callback) {
              callback(xhr.responseText);
            }
          }
        } 
        catch(e) {
          alert('Error: ' + e.name);
        }
      }
    }
    xhr.send(JSON.stringify(message));
  }

  // get the events and process them to be displayed in github-containers
  if(github_name) {
    sendAJAX("GET", github_url, "", function(events) {
      var result = JSON.parse(events);
      for(var i=0; i < result.length; ++i) {
        var repo_url = "https://github.com/" + result[i].repo.name;

        // fill the container with details
        githubContainer.content.querySelector(".github-type").innerHTML = result[i].type;
        githubContainer.content.querySelector(".github-dp").href = result[i].actor.url;
        githubContainer.content.querySelector(".github-repo-url").href = repo_url;
        githubContainer.content.querySelector(".github-repo-url").innerHTML = repo_url;
        githubContainer.content.querySelector(".github-date").innerHTML = result[i].created_at;
        
        // clone the template to render and append to the dom
        var clone = document.importNode(githubContainer.content, true);
        postContainer.appendChild(clone);
      }
    });
  }
});