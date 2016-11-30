// functionality of index.html

const postForm = document.getElementById("post-form");
const postList = document.getElementById("posts");
const postTemplate = document.getElementById("post-container");
var page = "/posts?page=0";

var github_name = localStorage.getItem("github_username");

function loadPosts() {

  sendAJAX("GET", "/author" + page, "", function(results) {
    if (results.next) {
      // set the next page of posts
      page = results.next.split(".com")[1];
//      console.log(page);
    } else {
      // no more posts to show
      $("#load-posts").addClass("hidden");
//      console.log("no more posts");
    }

    for(var i=0; i < results.posts.length; ++i) {
           //console.log(posts);
      // fill the container with details
      postTemplate.content.querySelector(".post-title").textContent = results.posts[i].title;
      postTemplate.content.querySelector(".post-description").textContent = results.posts[i].description;
      postTemplate.content.querySelector(".post-author").textContent = results.posts[i].author.displayName;

      var cmreader = new commonmark.Parser();
      var writer = new commonmark.HtmlRenderer();
      var parsed = cmreader.parse(results.posts[i].content); // parsed is a 'Node' tree
      // transform parsed if you like...
      var commonmarkresult = writer.render(parsed);
      postTemplate.content.querySelector(".post-content").innerHTML = results.posts[i].content;
      if (results.posts[i].count > 0) {
        postTemplate.content.querySelector(".comments-num").textContent = "("+results.posts[i].count+")";
      }
      // postTemplate.content.querySelector(".post-date").textContent = Date(results.posts[i].published);

      // attach data to the links so it can be referenced when clicked
      var authorBtn = postTemplate.content.querySelector(".post-author");
      authorBtn.setAttribute("post-author-id", results.posts[i].author.id);

      var commentsBtn = postTemplate.content.querySelector(".comments");
      commentsBtn.setAttribute("post-comment-id", results.posts[i].id);
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
}

function loadGithub() {
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

      githubTemplate.content.querySelector(".github-date").textContent = new Date(events[i].created_at);

      // clone the template to render and append to the dom
      var clone = document.importNode(githubTemplate.content, true);
      sidebar.appendChild(clone);
    }
  });
}

$("#post-submit").click(function(e) {
  e.preventDefault();

  // encode form data as a JSON object
  var postData = {};
  postData["author_id"] = localStorage.getItem("author_id");
  postData["title"] = postForm.elements["title"].value;
  if (postForm.elements["desc"].value == null) {
    postData["description"] = "";
  }
  else {
    postData["description"] = postForm.elements["desc"].value;
  }
  postData["contentType"] = postForm.elements["text-type"].value;
  // console.log(postData["contentType"]);

  if (postForm.elements["text-type"].value == "text/x-markdown") {
    var cmreader = new commonmark.Parser();
    var writer = new commonmark.HtmlRenderer();
    var parsed = cmreader.parse(postForm.elements["post-text"].value); // parsed is a 'Node' tree
    // transform parsed if you like...
    var commonmarkresult = writer.render(parsed);
    // console.log(commonmarkresult);
    postData["content"] = commonmarkresult;
  }
  else {
    postData["content"] = postForm.elements["post-text"].value;
  }

  postData["visibility"] = postForm.elements["visibility"].value;

  // convert the image to base64 string and attach to the data
  var reader = new FileReader();
  reader.addEventListener("load", function () {
    postData["image"] = reader.result;
//    console.log(JSON.stringify(postData));
    sendAJAX("POST", "/posts", postData, function(result) {
//      console.log(result);
      window.location.reload();
    });
  }, false);

  // if there are images, we need to send the request after it decodes
  if (postForm.elements["image"].files[0]) {
    reader.readAsDataURL(postForm.elements["image"].files[0]);
    postData["image-ext"] = postForm.elements["image"].files[0].type;
  }
  // otherwise just send it
  else {
    sendAJAX("POST", "/posts", postData, function(result) {
//      console.log(result);
      window.location.reload();
    });
  }
});

$(document).ready(function() {
  // get the posts from authors I follow
  loadPosts();

  // if we have a github username, load the public events
  if (github_name) {
    loadGithub();
  }
});

// load more posts
$("#load-posts").click( function(e) {
  e.preventDefault();
  loadPosts();
});
