<?php

 $file = "/var/www/lightvalues.txt";
 $filePtr = fopen($file, 'w');
 
 //$status = "off"
// $brightness = 20;
 //$mode = "control";
 
 if(isset($_GET['state']))
	$status = $_GET['state'];
 if(isset($_GET['level']))
	$brightness = $_GET['level'];
 if(isset($_GET['mode']))
	$mode = $_GET['mode'];

if($brightness > 100)
	$brightness = 100;
	
 $data = $status.",".$brightness.",".$mode;
 fwrite($filePtr, $data);
 echo "Brightness = ".$brightness;
 fclose($filePtr);
 
 ?>
