$(document).ready(function() {

  var myTemplate = document.getElementById('post-container');
                  
  var td = myTemplate.content.querySelector(".post-content");
  td.textContent = "This is the changed content";
                  
  var normalContent = document.getElementById('posts');
                  
  var clonedTemplate = myTemplate.content.cloneNode(true);
  normalContent.appendChild(clonedTemplate)
});


