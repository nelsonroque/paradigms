<?php

# start session
session_start();

# get IP
if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
    $ip = $_SERVER['HTTP_CLIENT_IP'];
} elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
    $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
} else {
    $ip = $_SERVER['REMOTE_ADDR'];
}

# save IP in session
$_SESSION['CLIENT_IP'] = $ip;

?>
<html>
<head>
	<style>
		html, body {
		  margin: 0;
		  /*padding: 0.5em 2em 0.5em 2em;*/
		}

		input[type=submit] {
			border-radius: 6px;
			border: 2px solid black;
			padding: 0.5em 2em;
			font-size: 2em;
		}

		a {
			border-radius: 6px;
			border: 2px solid black;
			padding: 0.5em 2em;
			font-size: 2em;
		}

		a:hover {
			border-radius: 6px;
			border: 2px solid green;
			padding: 0.5em 2em;
			font-size: 2em;
		}
	</style>

    <title>Foraging | Nelson Roque</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
	<h4 id="circles_remain"></h4>
	<canvas class='responsive_canvas' id="canvas" height='300' width='300'>
	</canvas>
	<form action="save.php" method="post">
		<input type="hidden" name="click_data" id="click_data" value=''>
		<input type="hidden" name="participant_id" id="participant_id" value=''>
		<input type="hidden" name='data_header' id='data_header' value=''>
		<input type="submit" id="continue_button" value="Continue">
	</form>
		<script>

			// get window size
			// -------------------------------------------
			var w = window,
				x = w.innerWidth;
				y = w.innerHeight;

			// function definitions
			// -------------------------------------------

			function getRandomColor() {
				const r = Math.round(Math.random() * 255);
				const g = Math.round(Math.random() * 255);
				const b = Math.round(Math.random() * 255);
			 	return `rgb(${r},${g},${b})`;
			}

			function chooseRandomColor() {
				const objdec = Math.floor(Math.random() * 10);
				//alert(colorDecider);
				//alert(typeof(colorDecider));

				if(objdec >= 0 || objdec < 3){
					const r = 255;
					const g = 0;
					const b = 0;
				} else if(objdec >= 3 || objdec < 6){
					const r = 0;
					const g = 255;
					const b = 0;
				} else if(objdec >= 6 || objdec <= 10){
					const r = 0;
					const g = 0;
					const b = 255;
				} else {
					const r = 0;
					const g = 66;
					const b = 0;
				}

			 	return `rgb(${r},${g},${b})`;
			}

			function hasSameColor(color, shape) {
		  		return shape.color === color;
			}

			function cutCircle(context, x, y, radius){
			    context.globalCompositeOperation = 'destination-out';
			    context.beginPath();
			    context.arc(x, y, radius, 0, 2*Math.PI, false);
			    context.fill();
			}

			function isIntersect(point, circle) {
  				return Math.sqrt((point.x-circle.x) ** 2 + (point.y - circle.y) ** 2) < circle.radius;
			}

			// task parameters
			// -------------------------------------------
			const DEBUG_CODE = 0;

			// generate participant ID
			const participant_id = Date.now();

			const data_header = "participant_id" + "," + "cur_date" + "," + "cur_time" + "," + "micro_time" + "," + "object_spacer" + "," + "grid_buffer" + "," + "grid_padding" + "," + "jitter_amount" + "," + "circle_radius" + "," + "x" +"," + "y" + "," + "drawProbability" + "," + "setSize" + "," + "circles.length" + "," + "circles_remaining" + "," + "circle.id" + "," + "circle.color_R" + ","+ "circle.color_G" + ","+ "circle.color_B" + "," + "circle.x" + "," + "circle.y" + "," + "cur_mouse_x" + "," + "cur_mouse_y" + "," + "\n";

			// save participant id into holder
			var participant_id_holder = document.getElementById('participant_id');
			participant_id_holder.value = participant_id;

			var data_head = document.getElementById('data_header');
			data_head.value = data_header;

			var continue_button = document.getElementById('continue_button');
			continue_button.style.display = 'none';

			// display canvas
			const canvas = document.getElementById('canvas');
			const ctx = canvas.getContext('2d');

			// container for data output
			const data_area = document.getElementById("click_data");

			// container for circle count
			const count_area = document.getElementById("circles_remain");

			// initialize containerss
			const ids_clicked = [];

			// setup array for stimuli
			// -------------------------------------------
			// density of circles is controlled by this
			const drawProbability = Math.random();

			// set circle radius
			const circle_radius = Math.floor(Math.random() * 24) + 9;

			// object grid spacing parameters
			const grid_padding = 100;
			const grid_buffer = circle_radius * 2;
			const object_spacing_constant = 3;
			const object_spacer = circle_radius * object_spacing_constant;
			const jitter_amount = circle_radius-3;

			// resize canvas
			canvas.style.border = '3px solid darkgrey';
			canvas.style.borderRadius = '6px';
			canvas.width = x-grid_padding+(grid_padding/2);
			canvas.height = y-grid_padding;

			// object grid bound parameters
			const grid_x_max = x-grid_padding;//canvas.width;
			const grid_y_max = y-grid_padding;//canvas.height;

			// determine
			const numX = Math.floor(grid_x_max/object_spacer)+1;
			const numY = Math.floor(grid_y_max/object_spacer)+1;

			// determine set size from possible objects in grid
			const setSize = numX * numY;

			// initialize counter for holding circle data
			const circles = [];
			var circle_counter = 0;

			if(DEBUG_CODE == 1){
				alert(numX + " " + numY + " " + setSize);
			}

			for(var i = 0; i < numX; i++) {
				for(var j = 0; j < numY; j++) {
					// decide whether or not to draw object
					var drawDecider = Math.random();

					if(drawDecider > drawProbability) {	
						var jitter_x = Math.floor(Math.random() * jitter_amount);
						var jitter_y = Math.floor(Math.random() * jitter_amount);
						var x_coord_transform = (i * object_spacer) + jitter_x + grid_buffer;
						var y_coord_transform = (j * object_spacer) + jitter_y + grid_buffer;

						if(x_coord_transform > grid_x_max){
							jitter_x = Math.floor(Math.random() * jitter_amount);
							var x_coord_transform = (i * object_spacer) + jitter_x + grid_buffer;
						}

						if(y_coord_transform > grid_y_max){
							jitter_y = Math.floor(Math.random() * jitter_amount);
							var y_coord_transform = (j * object_spacer) + jitter_y + grid_buffer;
						}

						if(DEBUG_CODE == 1){
							//alert(i + " " + j);
							alert(jitter_x + " " + jitter_y);
							alert(x_coord_transform + " " + y_coord_transform);
						}

						circles.push({ id: circle_counter, 
				  		x: x_coord_transform,
				  		y: y_coord_transform, 
				  		radius: circle_radius,
				  	    //color: chooseRandomColor()});
				  		color: getRandomColor()});
				  		circle_counter++;
					}
				}
			}

			// container for circle count
			var circles_remaining = circles.length;

			// display circle count
			count_area.innerHTML = "Remaining: " + circles_remaining;

			// display instructions
			alert("Instructions: Click all " + circles_remaining + " circles as fast as possible");
			// future instructions overlay id on circles and click in order

			// draw circle stimuli onto canvas
			// -------------------------------------------
			circles.forEach(circle => {
			  ctx.beginPath();
			  ctx.arc(circle.x, circle.y, circle.radius, 0, 2*Math.PI, false);
			  ctx.fillStyle = circle.color;
			  ctx.fill();
			});

			// initialize counter
			var start_time = window.performance.now();


			// listen for object clicks
			// -------------------------------------------

			canvas.addEventListener('click', (e) => {
				const mousePos = {
					x: e.clientX - canvas.offsetLeft,
					y: e.clientY - canvas.offsetTop
				};

				circles.forEach(circle => {
				    if (isIntersect(mousePos, circle)) {

				    	// update circle count
				    	circles_remaining = circles_remaining - 1;
						count_area.innerHTML = "Remaining: " + circles_remaining;

						// another manipulation with circles remaining as instructional distractor
						// if(circles_remaining >= 5 & circles_remaining < 15) {
						// 	count_area.style.color = 'gold';
						// } else {
						// 	if(circles_remaining >= 3 & circles_remaining < 5){
						// 		count_area.style.color = 'orange';
						// 	} else {
						// 		if(circles_remaining >= 1 & circles_remaining < 3){
						// 			count_area.style.color = 'red';
						// 		}
						// 	}
						// }

				    	if(DEBUG_CODE == 1) {
				    		alert('click on circle: ' + circle.id);
				    		alert(circle.x+","+circle.y);
				    	}


				      	// keep track of all clicked object ids
					  	ids_clicked.push(circle.id);
					  	// can do cool things when certain ids are detected?
					    //console.log(ids_clicked);

					  	// remove clicked circle
					   cutCircle(ctx, circle.x, circle.y, circle_radius+2);
					
					  	// save instance variables for click
					  	var cur_mouse_x = mousePos.x;
					  	var cur_mouse_y = mousePos.y;
					  	var micro_time = window.performance.now();
					  	var cur_time = new Date().toLocaleTimeString();
					  	var cur_date = new Date().toLocaleDateString();
					    data_area.value = data_area.value + 
					    					  participant_id + "," + 
					    					  cur_date + "," + 
					    					  cur_time + "," + 
					    					  micro_time + "," + 
					    					  object_spacer + "," +
					    					  grid_buffer + "," +
					    					  grid_padding + "," +
					    					  jitter_amount + "," +
					    					  circle_radius + "," +
					    					  x + "," +
					    					  y + "," +
					    					  drawProbability + "," +
					    					  setSize + "," +
					    					  circles.length + "," +
					    					  circles_remaining + "," +
					    					  circle.id + "," + 
					    					  circle.color + "," +
					    					  circle.x + "," + 
					    					  circle.y + "," + 
					    					  cur_mouse_x + "," + 
					    					  cur_mouse_y + "," + 
					    					  "\n";

						if(circles_remaining == 0){
							canvas.style.display = "none";
							continue_button.style.display = 'block';
							var end_time = window.performance.now();
							var elapsed_time = end_time - start_time;
							count_area.innerHTML = "You finished in about " + Math.floor(elapsed_time/1000) + " seconds!";//"Remaining: " + circles_remaining;
							//alert("You finished in about " + Math.floor(elapsed_time/1000) + " seconds!");
						}
				  	} 
				  	// uncomment to track all clicks
				  	// ------------------------------------
				  	// also possible to track all clicks
			});
		});
	</script>
</body>
</html>