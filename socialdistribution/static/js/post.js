// get the posts with the post-id in localStorage
$(document).ready(function() {

  var host = localStorage.getItem("fetch-post-host");
  var postID = localStorage.getItem("fetch-post-id");
  var commentTemplate = $("#comment-template");
  var commentsList = $("#comment-list");

  // are we even supposed to be here
  if (host && postID) {

    // request the post from whatever the host is
    sendAJAX("GET", host+"/posts/"+postID, "", function(post) {
      // fill the container with details
      ("$post-title").textContent = post.title;
      ("$post-author").textContent = post.author.displayName;
      ("$post-description").textContent = post.description;
      ("$post-content").textContent = post.content;
    });

    // now fetch all the comments
    sendAJAX("GET", host+"/posts/"+postID+"/comments", "", function(comments) {
      for (var i=0; i<comments.length; ++i) {
        commentTemplate.content.querySelector(".comment-author").textContent = comments[i].author.displayName;
        commentTemplate.content.querySelector(".comment-content").textContent = comments[i].comment;

        // bind the author's ID to the author link
        var authorBtn = commentTemplate.content.querySelector(".comment-author-url");
        $(authorBtn).data("author-id", comments[i].author.id);

        var clone = document.importNode(commentTemplate.content, true);
        commentsList.append(clone);
      }
    });
  }
  else {
    // redirect to error page
    window.location.href = "error.html";
  }
});

// bind the onclick to set author id in localStorage
// and link the user to the author's profile
$(".comment-author-url").click(function (e) {
  e.preventDefault();
  localStorage.setItem("fetch-author-id", $(this).data("author-id"));
  window.location.href = "authorpage.html";
});
