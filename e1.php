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
	
	showResults($results, $searchTerm);

	end_html();
}

function display_form() {
	start_html();
?>
	<form action="e1.php" method="get">
		Title:
		<select name='title'>
			<option value = "">Select...</option>

<?php
			$sports = json_decode(file_get_contents('Sports.json'), true);
			foreach ($sports['sport'] as $sport) {
				//echo implode('_', $sport['title']);
				echo '<option value="">' . $sport['title'] . '</option>';
			}
?>
		<select>
		&nbsp;&nbsp;&nbsp;
		Results:
		<select name='results'>
			<option value = "">Select...</option>
		</select>
		&nbsp;&nbsp;&nbsp;
		Search Term:
		<select name='searchTerm'>
			<option value = "">Select...</option>
		</select>
		&nbsp;&nbsp;&nbsp;
		<input type='submit' value='SEND IT'>
	</form>
<?php
	end_html();
}

function showResults($fileName, $sTerm) {
	if(!file_exists($fileName)) {
		echo "File not found!";
		return false;
	}

	$allData = json_decode(file_get_contents($fileName), true);

	if($allData == NULL || json_last_error() != JSON_ERROR_NONE) {
		echo "Input JSON is bad!";
		return false;
	}
	
	if(!isset($allData['comments']) || !isset($allData['games'])) {
		echo "JSON file missing comments or games!";
		return false;
	}
	
	echo "<h3>";
	foreach ($allData['comments'] as $line) {
		echo $line, "&nbsp;";
	}
	echo "</h3>";

	$wincount = 0;
	foreach ($allData['games'] as $game) {
		echo "~~~~~~~~~~<br>";
		$keys = array_keys($game);
		for ($i=0; $i<count($keys); $i++) {
			$cont = $keys[$i].": ".$game[$keys[$i]];
			if($sTerm === $keys[$i]) {
				echo "<b>".$cont."</b>";
			}
			else {
				echo "<p>".$cont."</p>";
			}
			//update win counter
			if($keys[$i] === "WinorLose" && $game[$keys[$i]] === "W") {
				$wincount++;
			}
		}
	}
	echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~<br>";
	echo "Wins: ".$wincount." out of ".count($allData['games'])."<br>";
	echo "Avg. Winrate: ".$wincount*100/count($allData['games'])."%";
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
