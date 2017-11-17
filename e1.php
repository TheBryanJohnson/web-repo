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
	
	showResults($searchTerm);

	end_html();
}

function display_form() {
	start_html();
?>
	<form action="e1.php" method="get">
		Title:
		<input type='number' name='title'><br><br>
		Results:
		<input type='number' name='results'><br><br>
		Search Term:
		<input type='text' name='searchTerm'><br><br>
		<input type='submit' value='Pls'>
	</form>
<?php
	end_html();
}

function showResults($fileName) {
	if(!file_exists($fileName)) {
		echo "File not found!";
		return false;
	}

	$allData = json_decode(file_get_contents($fileName), true);

	if($allData == NULL || json_last_error() != JSON_ERROR_NONE) {
		echo "Input JSON is bad!";
		return false;
	}
	
	if(!isset($allData['comments'])) {
		echo "JSON file missing comments!";
		//var_dump($allData);
		return false;
	}
	
	echo "<h3>"	
	

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
