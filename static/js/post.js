const postID = localStorage.getItem("fetch-post-id");
const commentTemplate = $("#comment-template");
const commentsList = $("#posts");

// get the posts with the post-id in localStorage
$(document).ready(function() {

  // are we even supposed to be here
  if (postID) {

    // request the post from whatever the host is
    sendAJAX("GET", "/posts/"+postID, "", function(results) {
      // fill the container with details
      document.getElementById("post-title").textContent = results.posts[0].title;
      document.getElementById("post-author").textContent = results.posts[0].author.displayName;
      document.getElementById("post-description").textContent = results.posts[0].description;
      document.getElementById("post-content").innerHTML = results.posts[0].content;

      // bind the onclick to set author id in localStorage
      // and link the user to the author's profile
      $("#post-author").click(function(e) {
        e.preventDefault();
        // set this for authorpage to use
        localStorage.setItem("fetch-author-id", results.post[0].author.id);
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
        authorBtn.setAttribute("post-author-id", results.comments[i].author.id);

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
  commentData["post"] = postID;
  commentData["author_id"] = localStorage.getItem("author_id");
  commentData["comment_text"] =
  commentData["contentType"] = $("input[name=text-type]").val();

  if ($("input[name=text-type]").val() == "text/x-markdown") {
    var cmreader = new commonmark.Parser();
    var writer = new commonmark.HtmlRenderer();
    var parsed = cmreader.parse($("#comment-content").val()); // parsed is a 'Node' tree
    // transform parsed if you like...
    var commonmarkresult = writer.render(parsed);
    // console.log(commonmarkresult);
    commentData["content"] = commonmarkresult;
  }
  else {
    commentData["content"] = $("#comment-content").val();
  }

  console.log(JSON.stringify(commentData));

  // don't really care if it worked or not, that's the server's job
  sendAJAX("POST", "/posts/"+postID+"/comments", commentData, function(results) {
    console.log(response);
  });
  window.location.reload();
});
