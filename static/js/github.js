// searches cookies for a github_username
function getGithubUsername() {
  // look for the github_name in cookies
  var cookies = document.cookie.split(";");
  for(var i=0; i < cookies.length; i++) {
    var gname = cookies[i].split("=");
    if(gname[0].trim() == "cookie_cmput404_github_id") {
      return gname[1];
    }
  }
  return "";
}

$(document).ready(function() {

  // debug
  // document.cookie = "cookie_cmput404_github_id=stat3kk; expires=Thu, 18 Dec 2018 12:00:00 UTC";

  // this is the author's github_username, empty string if there isn't one
  var github_name = getGithubUsername(),
      github_url = "https://api.github.com/users/" + github_name + "/events",
      sidebar = document.getElementById("github"),
      githubTemplate = document.getElementById("github-container");

  // get the events and process them to be displayed in github-containers
  if(github_name) {
    sendAJAX("GET", github_url, "", function(events) {
      for(var i=0; i < events.length; ++i) {
        var repo_url = "https://github.com/" + events[i].repo.name;

        // fill the container with details
        githubTemplate.content.querySelector(".github-type").innerHTML = events[i].type;
        githubTemplate.content.querySelector(".github-dp").href = events[i].actor.url;
        githubTemplate.content.querySelector(".github-repo-url").href = repo_url;
        githubTemplate.content.querySelector(".github-repo-url").innerHTML = repo_url;
        githubTemplate.content.querySelector(".github-date").innerHTML = events[i].created_at;

        // clone the template to render and append to the dom
        var clone = document.importNode(githubTemplate.content, true);
        sidebar.appendChild(clone);
      }
    });
  }
});
