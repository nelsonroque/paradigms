<?php 

session_start();

$site_url = 'http://cognitivetask.com/games/forage';

if($_SESSION['TASK_COMPLETED'] == 1){
	echo("<h1>Thank you for playing!</h1>");
	echo("<hr>");
	echo("Completion Code: " . $_SESSION['PARTICIPANT']);
	echo("<hr>");
	echo("<a href=".$site_url.">play again?</a>");
} else {
	header('Location: ' . $site_url);
	exit();
}

?>

	<style>
		html, body {
		  margin: 0;
		  /*padding: 0.5em 2em 0.5em 2em;*/
		}

		input[type=submit] {
			margin-top: 1em;
			border-radius: 6px;
			border: 2px solid black;
			padding: 0.5em 0.5em;
			font-size: 2em;
		}

		a {
			border-radius: 6px;
			border: 2px solid black;
			padding: 0.5em 0.5em;
			font-size: 2em;
			color:black;
			text-decoration: none;
		}

		a:visited, a:active {
			border-radius: 6px;
			border: 2px solid black;
			padding: 0.5em 0.5em;
			font-size: 2em;
			color:black;
			text-decoration: none;
		}

		a:hover {
			border-radius: 6px;
			background-color: green;
			border: 2px solid green;
			padding: 0.5em 0.5em;
			font-size: 2em;
			color:white;
			text-decoration: none;
		}
	</style>