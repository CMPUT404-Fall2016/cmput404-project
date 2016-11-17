function sendAJAX(method, url, message, callback) {
  var xhr = new XMLHttpRequest();
  xhr.open(method, url);
  xhr.onreadystatechange = function(){
    if (xhr.readyState==4) {
      try {
        if (xhr.status==200) {
          if(callback) {
            callback(JSON.parse(xhr.responseText));
          }
        }
      }
      catch(e) {
        alert('Error: ' + e.name);
      }
    }
  }
  //  if(message) {
  //    xhr.setHeader("Content-Type", "application/json");
  //  }
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify(message));
}

function getCookieid() {
  // look for the github_name in cookies
  var cookies = document.cookie.split(";");
  for(var i=0; i < cookies.length; i++) {
    var gname = cookies[i].split("=");
    if(gname[0] == "cookie_cmput404_author_id") {
      return gname[1];
    }
  }
  return "";
}

function getCookiehost() {
  // look for the github_name in cookies
  var cookies = document.cookie.split(";");
  for(var i=0; i < cookies.length; i++) {
    var gname = cookies[i].split("=");
    if(gname[0] == "cookie_cmput404_author_host") {
      return gname[1];
    }
  }
  return "";
}

$("#addfriendbtn").click(function(e) {
                         e.preventDefault();
                         
                         //                              var friendrequestdata = {};
                         //                              friendrequestdata["author"].id = getCookieid();
                         //                              friendrequestdata["authod"].host = getCookiehost();
                         //                              friendrequestdata["friend"].id = "thisauthorid";
                         //                              friendrequestdata["friend"].host = "thisauthorhost";
                         
                         var friendrequestdata = {};
                         friendrequestdata["author"] = myauthorid;
                         
                         sendAJAX("POST", "http://127.0.0.1:5000/friendrequest", friendrequestdata, function(response) {
                                  console.log(response);
                                  //window.location.href="friendspage.html";
                                  });
                         
                         
                         
                         });





function editauthorpage() {
  document.getElementById("profiledname").textContent = document.getElementById("pdn").value;
  //document.getElementById("pdn").placeholder = document.getElementById("profiledname").textContent;
  document.getElementById("pdn").value = document.getElementById("profiledname").textContent;
}

$(document).ready(function() {
<<<<<<< HEAD
                  
                  var myauthorid = getCookieid();
                  
                  
                  
                  

  var myTemplate = document.getElementById('profiledatas');
                  
  var phname = myTemplate.content.querySelector("#profilehname");
  phname.textContent = "Author";
                
                  
  var td = myTemplate.content.querySelector(".profileid");
  td.textContent = myauthorid;
//  var pu = myTemplate.content.querySelector(".profilename");
//                  profilenametext = "This is the changed content";
//  pu.textContent = "This is the changed username";
                  myTemplate.content.querySelector("#profiledname").textContent = "test1";
                  
                  myTemplate.content.querySelector("#profilehost").textContent = "test2";
                  
                  myTemplate.content.querySelector("#profileurl").textContent = "test3";
//  var pg = myTemplate.content.querySelector(".profilegithubid");
//                  profilegithubidtext = "This is the changed content";
//  pg.textContent = "This is the changed github id";
//  var pb = myTemplate.content.querySelector(".profilebio");
//                  profilebiotext = "This is the changed content";
//  pb.textContent = "This is the changed bio";
                  
                  
=======





  var myTemplate = document.getElementById('profiledatas');

  //var phname = myTemplate.content.querySelector(".profilehname");
  //phname.textContent = "This is the changed pname";


  var td = myTemplate.content.querySelector(".profileusername");
                  profileusernametext = "This is the changed content";
  td.textContent = profileusernametext;
  var pu = myTemplate.content.querySelector(".profilename");
                  profilenametext = "This is the changed content";
  pu.textContent = "This is the changed username";
  var pg = myTemplate.content.querySelector(".profilegithubid");
                  profilegithubidtext = "This is the changed content";
  pg.textContent = "This is the changed github id";
  var pb = myTemplate.content.querySelector(".profilebio");
                  profilebiotext = "This is the changed content";
  pb.textContent = "This is the changed bio";


>>>>>>> dd3fa2e2bef0feec409ea202bd8d45013e0253d5
  var normalContent = document.getElementById('profile');

  var clonedTemplate = myTemplate.content.cloneNode(true);
  normalContent.appendChild(clonedTemplate)
<<<<<<< HEAD
                  
                  
                  var mypTemplate = document.getElementById('profiledatas');
                  
                  var myprofilelink = "/author/" + myauthorid;
                  //sendAJAX("GET",)
                  
                  if (myauthorid = getCookieid()) {
                  
                          sendAJAX("GET", myprofilelink, "", function(response) {
                                   
                                   var td = mypTemplate.content.querySelector("#profilehname");
                                   profileusernametext = result.displayName;
                                   td.textContent = profileusernametext;
                  
                                   mypTemplate.content.querySelector("#profiledname").textContent = result.displayName;
                                   
                                   mypTemplate.content.querySelector("#profilehost").textContent = result.host;
                                   
                                   mypTemplate.content.querySelector("#profileurl").textContent = result.url;
                                   
                                   
                                   
                                   
                                   
                                   
                          });
                  
                      document.getElementById("editprofilebtn").style.display="";
                  
                  }
                  else {
                      document.getElementById("editprofilebtn").style.display="none";
                  }
                  
=======

>>>>>>> dd3fa2e2bef0feec409ea202bd8d45013e0253d5
//                  var text1 = "Changed1";
//                  var text2 = "Changed2";
//                  var text3 = "Changed3";
//                  var text4 = "Changed4";
//
//                  document.getElementsByName('username')[0].placeholder=text1;
//                  document.getElementsByName('displayName')[0].placeholder=text2;
//                  document.getElementsByName('githubid')[0].placeholder=text3;
//                  document.getElementsByName('bio')[0].placeholder=text4;
<<<<<<< HEAD
                  
                  document.getElementById("pid").placeholder = document.getElementById("profileid").textContent;
                  //document.getElementById("pdn").placeholder = document.getElementById("profiledname").textContent;
                  document.getElementById("pdn").value = document.getElementById("profiledname").textContent;
                  
                  document.getElementById("phost").placeholder = document.getElementById("profilehost").textContent;
                   document.getElementById("purl").placeholder = document.getElementById("profileurl").textContent;
});

=======


});

>>>>>>> dd3fa2e2bef0feec409ea202bd8d45013e0253d5
$("#editprofilebtn").click(function (e) {
                           e.preventDefault();
                           
                           //var text1 = document.getElementById("profileid").textContent;
                           //      var text2 = profileeditmode.elements["profilename"].value;
                           //      var text3 = profileeditmode.elements["profilehost"].value;
                           //      var text4 = profileeditmode.elements["profileurl"].value;
                           
                           
                           //document.getElementById("testid").placeholder= "123";
                           //      document.getElementsByName('pdisplayName')[0].placeholder=text2;
                           //      document.getElementsByName('phost')[0].placeholder=text3;
                           //      document.getElementsByName('purl')[0].placeholder=text4;
                           
                           document.getElementById("testid").placeholder = document.getElementById("profileid").textContent;
                           document.getElementById("pdn").value = document.getElementById("profiledname").textContent;
                           });


$("#saveprofilechange").click(function (e) {
<<<<<<< HEAD
                              e.preventDefault();
                              //                              var editprofiledata = {}
                              //                              editprofiledata["name"] = profileeditmode.elements["displayName"].value;
                              //                              editprofiledata["github_id"] = profileeditmode.elements["githubid"].value;
                              //                              editprofiledata["bio"] = editprofiledata.elements["bio"].value;
                              //
                              //                              sendAJAX("POST", "/editProfile", editprofiledata, function(response) {
                              //
                              //
                              //
                              //                                       });
                              
                              //var editprofileform = document.getElementById("editprofileform");
                              
                              //document.getElementById("profiledname").textContent = document.getElementById("pdn").value;
                              
                              
                              
                              
                              
                              });



$("#addfriendbtn").click(function(e) {
                              e.preventDefault();
                         console.log("button works");
//                              var friendrequestdata = {};
//                              friendrequestdata["author"].id = getCookieid();
//                              friendrequestdata["authod"].host = getCookiehost();
//                              friendrequestdata["friend"].id = "thisauthorid";
//                              friendrequestdata["friend"].host = "thisauthorhost";
                         
                              var friendrequestdata = {};
                              friendrequestdata["author"] = "123";
                         
                              sendAJAX("POST", "/friendrequest", friendrequestdata, function(response) {
                                       console.log(response);
                                       //window.location.href="friendspage.html";
                                  });
                         
              
                              
});


=======
                              var editprofiledata = {}
                              editprofiledata["name"] = editprofiledata.elements["displayName"].value;
                              editprofiledata["github_id"] = editprofiledata.elements["githubid"].value;
                              editprofiledata["bio"] = editprofiledata.elements["bio"].value;

                              sendAJAX("POST", "/editProfile", editprofiledata, function(response) {



                                       });




                              });

>>>>>>> dd3fa2e2bef0feec409ea202bd8d45013e0253d5
//
//$(document).ready(function() {
//
//                  var myTemplate = document.getElementById('profiledatas');
//
////                  var displaynameh = document.getElementById('profilehname');
////                  var displaynameb = document.getElementById('profileusername');
////                  var pname = document.getElementById('profilename');
////                  var githubid = document.getElementById('profilegethubid');
////                  var pbio = document.getElementById('profilebio');
//
//                  var pu = myTemplate.content.querySelector(".profilehname");
//                  pu.textContent = "This is the changed pname";
//
//                  var pu = myTemplate.content.querySelector(".profileusername");
//                  pu.textContent = "This is the changed username";
//
//                  var pn = myTemplate.content.querySelector(".profilename");
//                  pn.textContent = "This is the changed name";
//
//                  var pg = myTemplate.content.querySelector(".profilegithubid");
//                  pg.textContent = "This is the changed github id";
//
//                  var pb = myTemplate.content.querySelector(".profilebio");
//                  pb.textContent = "This is the changed bio";
//
//                  var normalContent = document.getElementById('profile');
//
//                  var clonedTemplate = myTemplate.content.cloneNode(true);
//                  normalContent.appendChild(clonedTemplate)
//});
