<?php

session_start();

# site URL
$site_url = "http://cognitivetask.com/games/forage";

# get user data from POST
$user_data = $_POST['click_data'];
$part_id = $_POST['participant_id'];
$dh = $_POST['data_header'];
$_SESSION['PARTICIPANT'] = $part_id;

if(!empty($user_data) & !empty($part_id)){
	$filen = 'data/'.$_SESSION['CLIENT_IP']."_".$part_id.'.csv';

	if(!file_exists($filen)){
		$file = fopen($filen, "w");
		$file = $filen;
	} else {
		$file = $filen;
	}	
	
	// Open the file to get existing content
	$current = file_get_contents($file);

	// Append a new record to the file
	$current .= $dh;
	$current .= $user_data;

	// Write the contents back to the file
	file_put_contents($file, $current);

	# set task completion status
	$_SESSION['TASK_COMPLETED'] = 1;

	header('Location: ' . $site_url . "/thank_you.php");
	exit();
} else {
	header('Location: ' . $site_url);
	exit();
}
?>