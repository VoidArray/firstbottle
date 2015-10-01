<html>
<head>
  <title>Быстрый сайт заметок</title>
  <link href="/main.css" rel="stylesheet" type="text/css"/>
</head>
<body>
% include("header.tpl")
<div class="maincontent">
<br>
{{message}} <!-- сообщение о событии для пользователя-->
% include(content+".tpl")
% include("footer.tpl")
</div>
</body>
</html> 
