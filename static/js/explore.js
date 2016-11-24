// functionality of explore.html

var postList = document.getElementById("posts"),
    postTemplate = document.getElementById("post-container");

// get all the public posts on the server
$(document).ready(function() {
  sendAJAX("GET", "/posts"+"?Foreign-Host=false", "", function(results) {
    console.log(results.posts);
    console.log(results.posts.length);

    for(var i=0; i < results.count; ++i) {
      // fill the container with details
      postTemplate.content.querySelector(".post-title").textContent = results.posts[i].title;
      postTemplate.content.querySelector(".post-description").textContent = results.posts[i].description;
      postTemplate.content.querySelector(".post-author").text = results.posts[i].author.displayName;
      postTemplate.content.querySelector(".post-content").textContent = results.posts[i].content;

      // attach data to the links so it can be referenced when clicked
      var authorBtn = postTemplate.content.querySelector(".post-author");
      authorBtn.setAttribute("post-author-id", results.posts[i].author.id);

      var commentsBtn = postTemplate.content.querySelector(".comments");
      commentsBtn.setAttribute("post-comment-id", results.posts[i].id);

      // clone the template to render and append to the dom
      var clone = document.importNode(postTemplate.content, true);
      postList.appendChild(clone);
    }

	  // bind the onclick to set author id in localStorage
    // and link the user to the author's profile
    $(".post-author").click(function(e) {
    	e.preventDefault();
    	// set this for authorpage to use
    	localStorage.setItem("fetch-author-id", $(this).attr("post-author-id"));
    	window.location.href = "authorpage.html";
    });

    // bind the onclick to set post host and id in localStorage
    // and link the user to the post's page
    $(".comments").click(function(e) {
      e.preventDefault();
      // set this for later
      // localStorage.getItem("fetch-post-host", $(this).data("post-host"));
      localStorage.setItem("fetch-post-id", $(this).attr("post-comment-id"));
      window.location.href("post.html")
    });
  });
});
