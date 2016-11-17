$(document).ready(function() {





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


  var normalContent = document.getElementById('profile');

  var clonedTemplate = myTemplate.content.cloneNode(true);
  normalContent.appendChild(clonedTemplate)

//                  var text1 = "Changed1";
//                  var text2 = "Changed2";
//                  var text3 = "Changed3";
//                  var text4 = "Changed4";
//
//                  document.getElementsByName('username')[0].placeholder=text1;
//                  document.getElementsByName('displayName')[0].placeholder=text2;
//                  document.getElementsByName('githubid')[0].placeholder=text3;
//                  document.getElementsByName('bio')[0].placeholder=text4;


});

$("#editprofilebtn").click(function (e) {

      var text1 = "Changed1";
      var text2 = "Changed2";
      var text3 = "ChangedHa";
      var text4 = "Changed4";

      document.getElementsByName('username')[0].placeholder=text1;
      document.getElementsByName('displayName')[0].placeholder=text2;
      document.getElementsByName('githubid')[0].placeholder=text3;
      document.getElementsByName('bio')[0].placeholder=text4;
});


$("#saveprofilechange").click(function (e) {
                              var editprofiledata = {}
                              editprofiledata["name"] = editprofiledata.elements["displayName"].value;
                              editprofiledata["github_id"] = editprofiledata.elements["githubid"].value;
                              editprofiledata["bio"] = editprofiledata.elements["bio"].value;

                              sendAJAX("POST", "/editProfile", editprofiledata, function(response) {



                                       });




                              });

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
