// functionality of explore.html

var postList = document.getElementById("posts"),
    postTemplate = document.getElementById("post-container");

// get all the public posts on the server
$(document).ready(function() {
  sendAJAX("GET", "/explore", "", function(posts) {
    for(var i=0; i < posts.length; ++i) {
      // fill the container with details
      postTemplate.content.querySelector(".post-title").textContent = posts[i].title;
      postTemplate.content.querySelector(".post-author").textContent = posts[i].author.displayname;
      postTemplate.content.querySelector(".post-author-url").href = posts[i].author.url;
      postTemplate.content.querySelector(".post-content").textContent = posts[i].content;

      // clone the template to render and append to the dom
      var clone = document.importNode(postTemplate.content, true);
      postList.appendChild(clone);
    }
  });
});
