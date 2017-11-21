<?php

/*Authors: William Miller, Bryan Johnson
* Purpose: FanXelk, a web service that displays sports statistics. 
* Functionality:
*  a) [Implemented] PHP program runs without runtime errors/warnings and
*     performs basic JSON reporting
*  b) [Implemented] PHP program performs searches, highlighting the included
*     search term
*  c) [Implemented] PHP correctly and properly reads files from the directory
*     and converts them to JSON objects
*  d) [Implemented] PHP program presents a dynamic, file-based HTML form
*  e) [Implemented] PHP program is secure and returns appropriate error
*     messages
*  f) [Implemented] PHP program is robust atainst missing/incorrect JSON 
*     elements
*/

//Starting action; if the form's been submitted, process it, otherwise
//display the form
if (isset($_GET['title']) && isset($_GET['results'])) {
	process_form();
} else {
	display_form();
}

//Process the form, checking for validity and printing off the requested
//records
function process_form() {
	start_html();

	$title = $_GET['title'];
	$results = $_GET['results'];
	$searchTerm = $_GET['searchTerm'];
	
	//showResults($results, $searchTerm);
	
	//Fix the input fields: they will come in with _'s instead of spaces
	$title = str_replace('_', ' ', $title);
	$results = str_replace('_', ' ', $results);
	$searchTerm = str_replace('_', ' ', $searchTerm);

	//Start from scratch for security
	$sports = json_decode(file_get_contents('Sports.json'), true);
	$titleFailed = true;
	foreach($sports['sport'] as $sport) {
		if($sport['title'] === $title) {
			$titleFailed = false;
			foreach($sport['results'] as $key => $fileName) {
				if($key === $results) {
					showResults($fileName, $searchTerm);
					end_html();
					return;
				}
			}
		}
	}
	if($titleFailed) {
		echo "<p> Title not found, please use the HTML form! </p>";
	}
	else {
		echo "<p> Results not found! Try a different season. </p>";	
	}

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
				$tmp = str_replace(' ', '_', $sport['title']);
				if(!$tmp=="") {
					echo '<option value='.$tmp.'>' . $sport['title'] . '</option>';
				}
			}
?>
		<select>
		&nbsp;&nbsp;&nbsp;
		Results:
		<select name='results'>
			<option value = "">Select...</option>
<?php
			foreach ($sports['sport'] as $res) {
				$resKeys = array_keys($res['results']);
				for ($p=0; $p<count($resKeys); $p++) {
					//possibly not really needed here but makes it more robust
					$tmp = str_replace(' ', '_', $resKeys[$p]);
					if(!$tmp=="") {
						echo '<option value='.$tmp.'>' . $resKeys[$p] . '</option>';
					}
				}
			}
?>

		</select>
		&nbsp;&nbsp;&nbsp;
		Search Term:
		<select name='searchTerm'>
			<option value = "">Select...</option>
<?php
			$allTerms = [];
			$termDupe = false;
			foreach ($sports['sport'] as $sport) {
				foreach($sport['searchterms'] as $term1) {
					$termDupe = false;
					foreach($allTerms as $term2) {
						if($term1==$term2) {
							$termDupe = true;	
						}
					}
					if(!$termDupe) {
						array_push($allTerms, $term1);
						$tmp = str_replace(' ', '_', $term1);
						if(!$tmp=="") {
						echo '<option value='.$tmp.'>' . $term1 . '</option>';
						}
					}
				}
			}
?>
		</select>
		&nbsp;&nbsp;&nbsp;
		<input type='submit' value='Submit'>
	</form>
<?php
	end_html();
}

//Show results of a given fileName along with an optional search term.
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

//HTML header
function start_html() {
	echo "
	<html>
	<head>
		<title>Sports!</title>
	</head>
	<body>
		<h1>FanXelk</h1>
		<p>Disclaimer: A particular sport may not have information for a selected season.</p>
		<p>Disclaimer2: If a particular search term is not found, it will be ignored.</p>
	";
}

//HTML closing tags
function end_html() {
	echo "
	</body>
	</html>
	";
}

?>
