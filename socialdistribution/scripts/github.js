$(document).ready(function() {

  var github_id = "stat3kk";
  var url = "https://api.github.com/users/" + github_id + "/events";

  var postContainer = document.getElementById("posts");
  var githubContainer = document.getElementById("github-container");

  var processEvents = function (json) {
    var result = JSON.parse(json);
    // var 30days = new Date().setDate(today.getDate()-30)
    for(var i=0; i < result.length; ++i) {
      var repo = "https://github.com/" + result[i].repo.name;
      githubContainer.content.querySelector(".github-type").innerHTML = result[i].type;
      githubContainer.content.querySelector(".github-dp").href = result[i].actor.url;
      githubContainer.content.querySelector(".github-repo-url").href = repo;
      githubContainer.content.querySelector(".github-repo-url").innerHTML = repo;
      githubContainer.content.querySelector(".github-date").innerHTML = result[i].created_at;
      var clone = document.importNode(githubContainer.content, true);
      postContainer.appendChild(clone);
    }
  }

  var xhr = new XMLHttpRequest();
  xhr.open('GET', url);
  xhr.onreadystatechange = function(){
    if (xhr.readyState==4) {
      try {
        if (xhr.status==200) {
          processEvents(xhr.responseText);
        }
      } 
      catch(e) {
        alert('Error: ' + e.name);
      }
    }
  }

  xhr.send(null);
});