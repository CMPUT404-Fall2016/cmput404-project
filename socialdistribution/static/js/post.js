$("#post-submit").click(function(e) {
  e.preventDefault();

  // encode form data as a JSON object
  var postForm = document.getElementById("post-form"),
  postData = {};
  postData["title"] = postForm.elements["title"].value;
  postData["description"] = postForm.elements["desc"].value;
  postData["contentType"] = postForm.elements["text-type"].value;
  postData["content"] = postForm.elements["post-text"].value;
  postData["visibility"] = postForm.elements["visibility"].value;
  // encode the current time in ISO 8601
  var timestamp = new Date();
  postData["published"] = timestamp.toISOString();

  // debug
  // console.log(postData);
  sendAJAX("POST", "/makePost", postData, null)
  window.location.reload();
});

// http://stackoverflow.com/questions/34972072/how-to-send-image-to-server-with-http-post-in-javascript-and-store-base64-in-mon
// 11/01/2016

// converts an image to Base64 encoding for sending in http request
// not used
function convertToBase64(url, imagetype, callback) {

    var img = document.createElement('IMG'),
        canvas = document.createElement('CANVAS'),
        ctx = canvas.getContext('2d'),
        data = "";

    img.crossOrigin = 'Anonymous'

    // Because image loading is asynchronous, we define an event listening function that will be called when the image has been loaded
    img.onLoad = function() {
        // When the image is loaded, this function is called with the image object as its context or 'this' value
        canvas.height = this.height;
        canvas.width = this.width;
        ctx.drawImage(this, 0, 0);
        data = canvas.toDataURL(imagetype);
        callback(data);
    };

    // We set the source of the image tag to start loading its data. We define
    // the event listener first, so that if the image has already been loaded
    // on the page or is cached the event listener will still fire

    img.src = url;
}
