// functionality of index.html

var postForm = document.getElementById("post-form");

$("#post-submit").click(function(e) {
  e.preventDefault();

  // encode form data as a JSON object
  var postData = {};
  postData["author_id"] = localStorage.getItem("author_id");
  postData["title"] = postForm.elements["title"].value;
  postData["description"] = postForm.elements["desc"].value;
  postData["contentType"] = postForm.elements["text-type"].value;
  postData["content"] = postForm.elements["post-text"].value;
  postData["visibility"] = postForm.elements["visibility"].value;

  // convert the image to base64 string and attach to the data
  var reader = new FileReader();
  reader.addEventListener("load", function () {
    postData["image"] = reader.result;
    console.log(JSON.stringify(postData));
  }, false);

  if (postForm.elements["image"].files[0]) {
    reader.readAsDataURL(postForm.elements["image"].files[0]);
  }

  sendAJAX("POST", "/posts", postData, function(result) {
    console.log(result);
    window.location.reload();
  });
});

// get the posts from authors I follow
$(document).ready(function() {
  var postList = document.getElementById("posts");
  var postTemplate = document.getElementById("post-container");
  sendAJAX("GET", "/author/posts", "", function(posts) {
    for(var i=0; i < posts.length; ++i) {
           //console.log(posts);
      // fill the container with details
      postTemplate.content.querySelector(".post-title").textContent = posts[i].title;
      postTemplate.content.querySelector(".post-description").textContent = posts[i].description;
      postTemplate.content.querySelector(".post-author").textContent = posts[i].author.displayname;
      postTemplate.content.querySelector(".post-content").textContent = posts[i].content;

      // attach data to the links so it can be referenced when clicked
      var authorBtn = postTemplate.content.querySelector(".post-author");
      authorBtn.setAttribute("post-author-id", posts[i].author.id);
           //console.log(authorBtn);

      var commentsBtn = postTemplate.content.querySelector(".comments");
      commentsBtn.setAttribute("post-comment-id", posts[i].id);
          //  console.log(commentsBtn);

      // clone the template to render and append to the dom
      var clone = document.importNode(postTemplate.content, true);
      postList.appendChild(clone);
    }

    // bind the onclick to set post host and id in localStorage
    // and link the user to the post's page
    $(".comments").click(function(e) {
      e.preventDefault();
      // set this for later
      localStorage.setItem("fetch-post-id", $(this).attr("post-comment-id"));
      window.location.href = "post.html";
    });

    // bind the onclick to set author id in localStorage
    // and link the user to the author's profile
    $(".post-author").click(function(e) {
      e.preventDefault();
      // set this for authorpage to use
      localStorage.setItem("fetch-author-id", $(this).attr("post-author-id"));
      window.location.href = "authorpage.html";
    });
  });
});

// get the user's public events
$(document).ready(function() {
  // this is the author's github_username, empty string if there isn't one
  var github_name = localStorage.getItem("github_username");
  if (github_name) {
    var github_url = "https://api.github.com/users/" + github_name + "/events",
        sidebar = document.getElementById("github"),
        githubTemplate = document.getElementById("github-container");

    // get the events and process them to be displayed in github-containers
    $("#git-alert").addClass("hidden");
    sendAJAX("GET", github_url, "", function(events) {
      for(var i=0; i < events.length; ++i) {
        var repo_url = "https://github.com/" + events[i].repo.name;

        // fill the container with details
        githubTemplate.content.querySelector(".github-type").innerHTML = events[i].type;
        githubTemplate.content.querySelector(".github-dp").href = "https://github.com/" + events[i].actor.login;
        githubTemplate.content.querySelector(".github-img").src = events[i].actor.avatar_url;
        githubTemplate.content.querySelector(".github-repo-url").href = repo_url;
        githubTemplate.content.querySelector(".github-repo-url").innerHTML = repo_url;

        githubTemplate.content.querySelector(".github-date").textContent = Date(events[i].created_at);

        // clone the template to render and append to the dom
        var clone = document.importNode(githubTemplate.content, true);
        sidebar.appendChild(clone);
      }
    });
  }
});
