<?php

/*Authors: William Miller, Bryan Johnson
* 
*
*
*
*
*
*/


if (isset($_GET['title']) && isset($_GET['results'])) {
	process_form();
} else {
	display_form();
}


function process_form() {
	start_html();

	$title = $_GET['title'];
	$results = $_GET['results'];
	$searchTerm = $_GET['searchTerm'];
	
	echo showResults($searchTerm);

	end_html();
}

function display_form() {
	start_html();
?>
	<form action="e1.php" method="get">
		Title:
		<select name='title'><br><br>
			<option value = "">Select...</option>
			<option value = "idk what this is">Sport</option>
		</select>
		&nbsp;&nbsp;&nbsp;
		Results:
		<select name='results'><br><br>
			<option value = "">Select...</option>
		</select>
		&nbsp;&nbsp;&nbsp;
		Search Term:
		<select name='searchTerm'><br><br>
			<option value = "">Select...</option>
		</select>
		&nbsp;&nbsp;&nbsp;
		<input type='submit' value='SEND IT'>
	</form>
<?php
	end_html();
}

function showResults($fileName) {
	if(!file_exists($fileName)) {
		return false;
	}
	return "yes";

}

function start_html() {
	echo "
	<html>
	<head>
		<title>Sports!</title>
	</head>
	<body>
		<h1>FanXelk</h1>
	";
}

function end_html() {
	echo "
	</body>
	</html>
	";
}

?>
