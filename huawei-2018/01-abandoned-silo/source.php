<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="">
  <meta name="author" content="">
  <title>Blind Flag ! </title>
  <!-- Bootstrap core CSS -->
  <link href="css/bootstrap.min.css" rel="stylesheet">
  <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
  <!--[if lt IE 9]>
  <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
  <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
  <![endif]-->
</head>

<body>
<div class="container">
    <div class="navbar navbar-default">
        <div class="navbar-header">
            <a class="navbar-brand" href="#">Blind flag!</a>
</div>
<div class="navbar-collapse collapse">
    <ul class="nav navbar-nav">
  <li><a href="#">Home</a></li>
    </ul>
</div>
</div>

<div class="jumbotron">
<h1>Ping 127.0.0.1</h1>
<p class="lead">Recupera el contenido de <a href="flag.txt">flag.txt</a> en el servidor</p>

<?php
if(isset($_GET['host'])){
$host = $_GET['host'];
$output = exec('ping -c 1 '.$host, $output, $result);
if($result == 0){
echo("<div class='alert alert-info'>Host is alive! </div>");
}
else {
echo("<div class='alert alert-danger'>Host is down! </div>");
}
}
?>
<form action="index.php" method="GET">
<div class="form-group">
<label for="user">Ping:</label>
<input type="text" class="form-control" id="host" name="host" value="127.0.0.1">
</div>
<button type="submit" class="btn btn-default">Check</button>
</form>
</div>
</div>
</div> <!-- /container -->
</body>
</html>
