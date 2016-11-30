const postID = localStorage.getItem("fetch-post-id");
//const commentTemplate = $("#comment-template");
const commentTemplate = document.getElementById("comment-template")
//const commentsList = $("#posts");
const commentsList = document.getElementById("posts");
const commentform = document.getElementById("comment-form");
var origin = "";

// get the posts with the post-id in localStorage
$(document).ready(function() {
  var postList = document.getElementById("posts");
  // are we even supposed to be here
  if (postID) {

    // request the post from whatever the host is
    sendAJAX("GET", "/posts/"+postID, "", function(results) {
      // console.log(results);
      // fill the container with details
      localStorage.setItem("Author-host-url", results.posts.author.host);
      document.getElementById("post-title").textContent = results.posts.title;
      document.getElementById("post-author").textContent = results.posts.author.displayName;
      document.getElementById("post-description").textContent = results.posts.description;

      if(results.posts.contentType == "text/markdown" || results.posts.contentType == "text/x-markdown") {
         var cmreader = new commonmark.Parser();
         var writer = new commonmark.HtmlRenderer();
         var parsed = cmreader.parse(results.posts.content); // parsed is a 'Node' tree
         // transform parsed if you like...
         var commonmarkresult = writer.render(parsed);
         document.getElementById("post-content").innerHTML = commonmarkresult;
       }
       else {
         document.getElementById("post-content").innerHTML = results.posts.content;
       }

//      document.getElementById("post-content").innerHTML = results.posts.content;
      document.getElementById("post-date").textContent = new Date(results.posts.published);
      // get the origin for when we need to make a comment
      origin = results.posts.origin;
      localStorage.setItem("origin", results.posts.origin);
      // console.log(results.posts.comments.length);
//      for (var i=0; i < results.posts.comments.length; ++i) {
//          var commentsTemplate = document.getElementById("comment-template");
//          // console.log(results.posts.comments);
//          commentsTemplate.content.querySelector(".comment-author").textContent = results.posts.comments[i].author.displayName;
//          //        commentTemplate.content.querySelector(".comment-content").textContent = results.posts.comments[i].comment;
//
//         if(results.posts.comments[i].contentType == "text/markdown" || results.posts.comments[i].contentType == "text/x-markdown") {
//             var cmreader = new commonmark.Parser();
//             var writer = new commonmark.HtmlRenderer();
//             var parsed = cmreader.parse(results.posts.comments[i].comment); // parsed is a 'Node' tree
//             // transform parsed if you like...
//             var commonmarkresult = writer.render(parsed);
//             commentsTemplate.content.querySelector(".comment-content").innerHTML = commonmarkresult;
//         }
//         else {
//             commentsTemplate.content.querySelector(".comment-content").innerHTML = results.posts.comments[i].comment;
//         }
//
//         var authorBtn = commentsTemplate.content.querySelector(".comment-author");
//         authorBtn.setAttribute("post-author-id", results.posts.comments[i].author.id);
//
//         var clone = document.importNode(commentsTemplate.content, true);
//         postList.appendChild(clone);
//         $(".comment-author").click(function (e) {
//              e.preventDefault();
//              localStorage.setItem("fetch-author-id", $(this).attr("post-author-id"));
//              window.location.href = "authorpage.html";
//          });
//      }

      // bind the onclick to set author id in localStorage
      // and link the user to the author's profile
      $("#post-author").click(function(e) {
        e.preventDefault();
        // set this for authorpage to use
        localStorage.setItem("fetch-author-id", results.posts.author.id);
        window.location.href = "authorpage.html";
      });
    });

    // now fetch all the comments
    sendAJAX("GET", "/posts/"+postID+"/comments/", "", function(results) {
      for (var i=0; i < results.comments.length; ++i) {
        commentTemplate.content.querySelector(".comment-author").textContent = results.comments[i].author.displayName;
//        commentTemplate.content.querySelector(".comment-content").textContent = results.comments[i].comment;

         if(results.comments[i].contentType == "text/markdown" || results.comments[i].contentType == "text/x-markdown") {
         var cmreader = new commonmark.Parser();
         var writer = new commonmark.HtmlRenderer();
         var parsed = cmreader.parse(results.comments[i].comment); // parsed is a 'Node' tree
         // transform parsed if you like...
         var commonmarkresult = writer.render(parsed);
         commentTemplate.content.querySelector(".comment-content").innerHTML = commonmarkresult;
         }
         else {
         commentTemplate.content.querySelector(".comment-content").innerHTML = results.comments[i].comment;
         }


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
  commentData["post"] = localStorage.getItem("origin");
  commentData["comment"] = {};
  commentData["comment"]["host_id"] = localStorage.getItem("Author-host-url");
  commentData["comment"]["author"] = {};
  commentData["comment"]["author"]["id"] = localStorage.getItem("author_id");
  var hostname = "http://" + window.location.host;
  commentData["comment"]["author"]["host"] = hostname;
  commentData["comment"]["author"]["displayName"] = localStorage.getItem("display_name");
  commentData["comment"]["author"]["url"] = hostname + "/author/" + localStorage.getItem("author_id");
  commentData["comment"]["author"]["github"] = localStorage.getItem("github_username");

//  if ($("input[name=text-type]").val() == "text/x-markdown") {
  if (commentform.elements["text-type"].value == "text/x-markdown") {
    var cmreader = new commonmark.Parser();
    var writer = new commonmark.HtmlRenderer();
    var parsed = cmreader.parse(commentform.elements["post-text"].value); // parsed is a 'Node' tree
    // transform parsed if you like...
    var commonmarkresult = writer.render(parsed);
    // console.log(commonmarkresult);
    commentData["comment"]["comment"] = commonmarkresult;
  }
  else {
    commentData["comment"]["comment"] = commentform.elements["post-text"].value;;
  }

  commentData["comment"]["contentType"] = commentform.elements["text-type"].value;

  // console.log(JSON.stringify(commentData));

  // don't really care if it worked or not, that's the server's job
  sendAJAX("POST", "/posts/"+postID+"/comments/?size=50", commentData, function(results) {
    // console.log(results);
  });
  window.location.reload();
});
