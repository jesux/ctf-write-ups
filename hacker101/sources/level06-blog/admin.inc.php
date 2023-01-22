<h2>Pending Comments</h2>
<?php
	if(isset($_GET["approve"]))
		mysql_query("UPDATE comments SET approved=1 WHERE id=" . $_GET["approve"]);
	$q = mysql_query("SELECT id, page, body FROM comments WHERE approved=0");
	while($row = mysql_fetch_assoc($q)) {
		?>
		<hr>
		<h3>Comment on <?php echo htmlentities($row["page"]); ?></h3>
		<p><?php echo htmlentities($row["body"]); ?></p>
		<a href="?page=admin.inc&approve=<?php echo $row["id"]; ?>">Approve Comment</a>
		<?php
	}

	$title = "Admin";
?>