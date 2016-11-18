// get the posts with the post-id in localStorage
$(document).ready(function() {

  var host = localStorage("fetch-post-host");
  var postID = localStorage("fetch-post-id");
  var commentTemplate = $("#comment-template");
  var commentsList = $("#comment-list");

  // request the post from whatever the host is
  sendAJAX("GET", host+"/posts/"+postID, "", function(post) {
    // fill the container with details
    ("$post-title").textContent = post.title;
    ("$post-author").textContent = post.author.displayName;
    ("$post-description").textContent = post.description;
    ("$post-content").textContent = post.content;
  });

  sendAJAX("GET", host+"/posts/"+postID+"/comments", "", function(comments) {
    // now fetch all the comments
    for (var i=0; i<comments.length; ++i) {
      commentTemplate.content.querySelector(".comment-author").textContent = comments[i].author.displayName;
      commentTemplate.content.querySelector(".comment-content").textContent = comments[i].comment;

      // bind the author's ID to the author link
      commentTemplate.content.querySelector(".comment-author-url").data("author-id", comments[i].author.id);

      var clone = document.importNode(commentTemplate.content, true);
      commentsList.append(clone);
    }
  });
});

$(".comment-author-url").click(function (e) {
  e.preventDefault();
  localStorage("fetch-author-id", this.data("author-id"));
  window.location.href = "authorpage.html";
});
