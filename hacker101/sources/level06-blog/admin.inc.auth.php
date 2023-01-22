<form method="POST">
	Username: <input type="text" name="username"><br>
	Password: <input type="password" name="password"><br>
	<input type="submit" value="Log In"><br>
	<?php
		if(isset($_POST["username"]) || isset($_POST["password"]))
			echo '<span style="color: red;">Incorrect username or password</span>';
	?>
</form>
<?php $title = "Admin Login"; ?>