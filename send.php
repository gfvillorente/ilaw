<?php
header('Cache-Control: no-cache, must-revalidate');
header('Expires: Mon, 26 Jul 1997 05:00:00 GMT');
header('Content-type: application/json');

//echo "\nSending JSON data...\n";

$handle = fopen("/var/www/readings.txt", "r");
if ($handle) {
	$readings = array();
    $ctr = 1;
	while (($line = fgets($handle)) !== false) {
		$pwrReading = explode(",", $line);
		$timestamp = str_replace("\n", '', $pwrReading[8]);
		if($pwrReading[0]=="")
		{
			$data = array(
				"stat" => $pwrReading[1],
				"watts" => $pwrReading[2],
				"va" => $pwrReading[3],
				"var" => $pwrReading[4],
				"pf" => $pwrReading[5],
				"volt" => $pwrReading[6],
				"ampere" => $pwrReading[7],
				"timestamp" => $timestamp
			);
		}
		else
		{
			$data = array(
				"stat" => $pwrReading[0],
				"watts" => $pwrReading[1],
				"va" => $pwrReading[2],
				"var" => $pwrReading[3],
				"pf" => $pwrReading[4],
				"volt" => $pwrReading[5],
				"ampere" => $pwrReading[6],
				"timestamp" => $timestamp
			);
		}
		array_push($readings, $data);
			
    }
	$json  = json_encode($readings);
	echo $json."\n";
} else {
    // error opening the file.
}

fclose($handle);

//Rewrite text file after sending
$handle = fopen("readings.txt", "w");
fwrite($handle, "");
fclose($handle);

?>
