// functionality of explore.html

var postList = document.getElementById("posts");
var postTemplate = document.getElementById("post-container");
var page = "/posts?page=0";

function loadPosts() {

  sendAJAX("GET", page, "", function(results) {
    if (results.next) {
      // set the next page of posts
      page = results.next.split(".com")[1];
      console.log(page);
    } else {
      // no more posts to show
      $("#load-posts").addClass("hidden");
      console.log("no more posts");
    }

    // fill the containers with results
    for(var i=0; i < results.posts.length; ++i) {
      postTemplate.content.querySelector(".post-title").textContent = results.posts[i].title;
      postTemplate.content.querySelector(".post-description").textContent = results.posts[i].description;
      postTemplate.content.querySelector(".post-author").textContent = results.posts[i].author.displayName;
          //  console.log(results.posts[i].author.id);

           var cmreader = new commonmark.Parser();
           var writer = new commonmark.HtmlRenderer();
           var parsed = cmreader.parse(results.posts[i].content); // parsed is a 'Node' tree
           // transform parsed if you like...
           var commonmarkresult = writer.render(parsed);

      //postTemplate.content.querySelector(".post-content").textContent = commonmarkresult;
      postTemplate.content.querySelector(".post-content").innerHTML = results.posts[i].content;
      postTemplate.content.querySelector(".post-date").textContent = Date(results.posts[i].published);

      // attach data to the links so it can be referenced when clicked
      var authorBtn = postTemplate.content.querySelector(".post-author");
      authorBtn.setAttribute("post-author-id", results.posts[i].author.id);

      var commentsBtn = postTemplate.content.querySelector(".comments");
      commentsBtn.setAttribute("post-id", results.posts[i].id);

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
                            console.log("clicked");
    	window.location.href = "authorpage.html";
    });

    // bind the onclick to set post host and id in localStorage
    // and link the user to the post's page
    $(".comments").click(function(e) {
      e.preventDefault();
      // set this for later
      localStorage.setItem("fetch-post-id", $(this).attr("post-id"));
      window.location.href = "post.html";
    });
  });
}

// get all the public posts on the server
$(document).ready(function() {
  loadPosts();
});

// load more posts
$("#load-posts").click( function(e) {
  e.preventDefault();
  loadPosts();
});
