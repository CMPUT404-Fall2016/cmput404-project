// functionality of explore.html

var postList = document.getElementById("posts"),
    postTemplate = document.getElementById("post-container");

// get all the public posts on the server
$(document).ready(function() {
  sendAJAX("GET", "/explore", "", function(posts) {
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

      // clone the template to render and append to the dom
      var clone = document.importNode(postTemplate.content, true);
      postList.appendChild(clone);
    }
  });
});

// bind the onclick to set post host and id in localStorage
// and link the user to the post's page
$(".comments").click(function(e) {
  e.preventDefault();
  // set this for later
  localStorage("fetch-post-host", $(this).data("post-host"));
  localStorage("fetch-post-id", $(this).data("post-id"));
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
