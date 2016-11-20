// functionality of index.html

$("#post-submit").click(function(e) {
  e.preventDefault();

  // encode form data as a JSON object
  var postForm = document.getElementById("post-form"),
      postData = {};
  postData["author_id"] = localStorage.getItem("author_id");
  postData["title"] = postForm.elements["title"].value;
  postData["description"] = postForm.elements["desc"].value;
  postData["contentType"] = postForm.elements["text-type"].value;
  postData["content"] = postForm.elements["post-text"].value;
  postData["visibility"] = postForm.elements["visibility"].value;

  // console.log(postData);
  sendAJAX("POST", "/service/posts", postData, null);
  window.location.reload();
});

// bind the onclick to set post host and id in localStorage
// and link the user to the post's page
$(".comments").click(function(e) {
  e.preventDefault();
  // set this for later
  localStorage.setItem("fetch-post-host", $(this).data("post-host"));
  localStorage.setItem("fetch-post-id", $(this).data("post-id"));
  window.location.href("post.html")
});

// bind the onclick to set author id in localStorage
// and link the user to the author's profile
$(".post-author-url").click(function(e) {
  e.preventDefault();
  // set this for later
  localStorage.setItem("fetch-author-id", $(this).data("post-author-id"));
  window.location.href("authorpage.html")
});

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

// get the posts from authors I follow
$(document).ready(function() {
  var postList = document.getElementById("posts");
  var postTemplate = document.getElementById("post-container");
  // page=<Page_No>&size=<Page_Zize>
  sendAJAX("GET", "/allPosts", "", function(posts) {
    for(var i=0; i < posts.length; ++i) {
      // fill the container with details
      postTemplate.content.querySelector(".post-title").textContent = posts[i].title;
      postTemplate.content.querySelector(".post-description").textContent = posts[i].description;
      postTemplate.content.querySelector(".post-author").textContent = posts[i].author.displayname;
      postTemplate.content.querySelector(".post-content").textContent = posts[i].content;

      // attach data to the links so it can be referenced when clicked
      var authorBtn = postTemplate.content.querySelector(".post-author-url");
      $(authorBtn).data("post-author-id", posts[i].author.id);

      var commentsBtn = postTemplate.content.querySelector(".comments");
      $(commentsBtn).data("post-host", posts[i].author.host);
      $(commentsBtn).data("post-id", posts[i].id);

      var clone = document.importNode(postTemplate.content, true);
      postList.appendChild(clone);
    }
  });
});

// get the user's public events
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
    $("#git-alert").addClass("hidden");
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


// http://stackoverflow.com/questions/34972072/how-to-send-image-to-server-with-http-post-in-javascript-and-store-base64-in-mon
// 11/01/2016
// converts an image to Base64 encoding for sending in http request
// not used
function convertToBase64(url, imagetype, callback) {

    var img = document.createElement('IMG'),
        canvas = document.createElement('CANVAS'),
        ctx = canvas.getContext('2d'),
        data = "";

    img.crossOrigin = 'Anonymous'

    // Because image loading is asynchronous, we define an event listening function that will be called when the image has been loaded
    img.onLoad = function() {
        // When the image is loaded, this function is called with the image object as its context or 'this' value
        canvas.height = this.height;
        canvas.width = this.width;
        ctx.drawImage(this, 0, 0);
        data = canvas.toDataURL(imagetype);
        callback(data);
    };

    // We set the source of the image tag to start loading its data. We define
    // the event listener first, so that if the image has already been loaded
    // on the page or is cached the event listener will still fire

    img.src = url;
}
