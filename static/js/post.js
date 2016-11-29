// get the posts with the post-id in localStorage
$(document).ready(function() {

  var postID = localStorage.getItem("fetch-post-id");
  var commentTemplate = $("#comment-template");
  var commentsList = $("#posts");

  // are we even supposed to be here
  if (postID) {

    // request the post from whatever the host is
    sendAJAX("GET", "/posts/"+postID, "", function(results) {
      // fill the container with details
      $("#post-title").text() = results.posts.title;
      $("#post-author").text() = results.posts.author.displayName;
      $("#post-description").text() = results.posts.description;
      //$("#post-content").text() = posts.content;
      document.getElementById("post-content").innerHTML = results.posts.content;

      // bind the onclick to set author id in localStorage
      // and link the user to the author's profile
      $(".post-author").click(function(e) {
        e.preventDefault();
        // set this for authorpage to use
        localStorage.setItem("fetch-author-id", results.post.author.id);
        window.location.href = "authorpage.html";
      });
    });

    // now fetch all the comments
    sendAJAX("GET", "/posts/"+postID+"/comments", "", function(results) {
      for (var i=0; i < results.comments.length; ++i) {
        commentTemplate.content.querySelector(".comment-author").textContent = results.comments[i].author.displayName;
        commentTemplate.content.querySelector(".comment-content").textContent = results.comments[i].comment;

        // bind the author's ID to the author link
        var authorBtn = commentTemplate.content.querySelector(".comment-author");
        authorBtn.setAttribute("post-author-id", results.comments[i].author_id);

        var clone = document.importNode(commentTemplate.content, true);
        commentsList.append(clone);
      }

      // bind the onclick to set author id in localStorage
      // and link the user to the author's profile
      $(".comment-author").click(function (e) {
        e.preventDefault();
        localStorage.setItem("fetch-author-id", $(this).attr("post-author-id"));
        window.location.href = "authorpage.html";
      });
    });
  }
  else {
    // redirect to error page
    window.location.href = "error.html";
  }
});


// send the comment to our server, who sends it to their server
$("#comment-submit").click(function (e) {
  e.preventDefault();

  var commentData = {};
  commentData["post_id"] = postID;
  commentData["author_id"] = localStorage.getItem("author_id");
  commentData["comment_text"] = $("#comment-content").val();

  console.log(JSON.stringify(commentData));

  // don't really care if it worked or not, that's the server's job
  sendAJAX("POST", "/makePost", commentData, function(response) {
    console.log(response);
  });
  window.location.reload();
});
