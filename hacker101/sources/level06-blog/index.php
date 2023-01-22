<?php
	// ^FLAG^df4533d3f24f22021aa842e87091d8567b239f59a174546b66c95fa2f82258ca$FLAG$
	mysql_connect("localhost", "root", "");
	mysql_select_db("level4");
	$page = isset($_GET['page']) ? $_GET['page'] : 'home.inc';
	if(strpos($page, ':') !== false && substr($page, 0, 5) !== "http:")
		$page = "home.inc";

	if(isset($_POST['body'])) {
		mysql_query("INSERT INTO comments (page, body, approved) VALUES ('" . mysql_real_escape_string($page) . "', '" . mysql_real_escape_string($_POST['body']) . "', 0)");
		if(strpos($_POST['body'], '<?php') !== false)
			echo '<p>^FLAG^5c9376d3de6ef5ba7b2af89f133b51a62f0911e6bd7f6bfd8a96cfd997ea2d55$FLAG$</p>';
?>
	<p>Comment submitted and awaiting approval!</p>
	<a href="javascript:window.history.back()">Go back</a>
<?php
		exit();
	}

	ob_start();
	include($page . ".php");
	$body = ob_get_clean();
?>
<!doctype html>
<html>
	<head>
		<title><?php echo $title; ?> -- Cody's First Blog</title>
	</head>
	<body>
		<h1><?php echo $title; ?></h1>
		<?php echo $body; ?>
		<br>
		<br>
		<hr>
		<h3>Comments</h3>
		<!--<a href="?page=admin.auth.inc">Admin login</a>-->
		<h4>Add comment:</h4>
		<form method="POST">
			<textarea rows="4" cols="60" name="body"></textarea><br>
			<input type="submit" value="Submit">
		</form>
<?php
	$q = mysql_query("SELECT body FROM comments WHERE page='" . mysql_real_escape_string($page) . "' AND approved=1");
	while($row = mysql_fetch_assoc($q)) {
		?>
		<hr>
		<p><?php echo $row["body"]; ?></p>
		<?php
	}
?>
	</body>
</html>