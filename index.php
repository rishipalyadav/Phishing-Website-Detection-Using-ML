<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Phis-Check</title>
    <link rel="stylesheet" href="index.css">
    <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
    <script>
      $(function () {
        $('button').on('click', function (event) {
//
event.preventDefault();// using this page stop being refreshing

var tablink = "";
tablink = document.getElementById("myForm").value;
$("#main_text").text("The URL being tested is: "+ tablink);
  var xhr = new XMLHttpRequest();
  params="url="+tablink;
  alert(params);
  var markup = "url="+tablink+"&html="+document.documentElement.innerHTML;
  xhr.open("POST","getSite.php",false);
  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhr.send(markup);
	alert(xhr.responseText);
  $("#response").text(xhr.responseText);
	return xhr.responseText;



        });
      });
    </script>
  </head>
  <body>
    <div class="main_body">
    <h1>Phis-Check v1.0</h1>
    <h1>Checks Phishing Websites!!</h1>
    <br><br>
    <form>
          Enter Website to check: <input name="website" type="text" id="myForm" class="search_box"><br><br>
          <button type="button" name="button">Check it Now!!</button>
        </form>
        <br><br><br>
        <div id="main_text"></div>
        <br><br><br><br><br>
        <div id="response"></div>
      </div>
  </body>
</html>
