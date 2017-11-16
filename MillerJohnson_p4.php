<?php
$string = '{"foo": "bar", "cool": "attr"}';
//  Note, result is a stdObject unless we pass "true" to json_decode()
//  Then result is an array!

$result = json_decode($string, true);
//var_dump($result);
$count = 0;

// List out each key/value pair, keep count as we go.
// count() function would give us a total count if thats all we needed, btw.
foreach ($result as $key => $value) {
	$count++;
	echo "<br>";
	echo $count;
	echo ") $key = $value\n";
}

$justkeys = array_keys($result);
echo "<br>";
echo "-----\n";
//var_dump($justkeys);

// -------------------------------------------
// A different approach - objects vs. arrays.  Note the second parameter to
// json_decode().

$result2 = json_decode($string, false);
//var_dump($result2);

$count = 0;
foreach ($result2 as $key => $value) {
        echo "<br>";
	$count++;
	echo $count;
	echo ") $key = $value\n";
}

?>

