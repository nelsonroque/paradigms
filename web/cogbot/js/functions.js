// get time difference in minutes
// -------------------------------------------------------------------
function diff_minutes(dt2, dt1) {
    var diff =(dt2.getTime() - dt1.getTime()) / 1000;
    diff /= 60;
    return Math.abs(Math.round(diff));
}

// for displaying session information (during development, not intended for production)
// -------------------------------------------------------------------

function display_results_alert(session_uuid_string, session_start_time, session_end_time) {

    // for building final string
    var alert_string = "";

    // build alert string
    alert_string += "Screenshot this popup and email it to nelsonroquejr@gmail.com to submit a data request";
    alert_string += alert_spacer_string;
    alert_string += alert_spacer_string;
    alert_string += "session uuid: ";
    alert_string += session_uuid_string;
    alert_string += alert_spacer_string;
    alert_string += "session start time: ";
    alert_string += session_start_time;
    alert_string += alert_spacer_string;
    alert_string += "session end time: ";
    alert_string += session_end_time;

    // display alert
	alert(alert_string);
}

// for creating a UUID string
// -------------------------------------------------------------------

function get_uuid_string() {
    return(Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15));
}


/**
 * name: userChat()
 * purpose: waits for the user to send a message.
*/

// -------------------------------------------------------------------

function userChat() {

  // Find where the user is inputing text.
  // -------------------------------------------------------------------
  compose_area = document.getElementById('composer');

  // Set the user as the sender of the next message.
  // -------------------------------------------------------------------
  nextMessage.sender = "user";

  // Get the user's input in the compose_area and clear the compose_area.
  // -------------------------------------------------------------------
  nextMessage.message = compose_area.value;
  compose_area.value = "";
    
  // We need to convert the user's message to upper case to check if it matches with any prompts using the .toUpperCase() function.
  // -------------------------------------------------------------------
  uppercase = nextMessage.message.toUpperCase();

  // validate user input against special keywords
  // -------------------------------------------------------------------
  if (uppercase == "EASTER EGG") {
    intervening_msg = [true, "This is just the tip of the iceberg. More easter eggs inside."];
  } else if (uppercase == "GOTCHA" || uppercase == "MICHAEL SCOTT") {
    intervening_msg = [true, "<img src='https://media.giphy.com/media/55SfA4BxofRBe/giphy.gif'>"];
  } else if (uppercase === "") {
    invalid_resp_count += 1;

    if(invalid_resp_count >= invalid_resp_max) {
        intervening_msg = [true, "Sorry, this assessment is now closed. Too many invalid responses received."];
    } else {
        intervening_msg = [true, "Yikes! You did not make a response. Please respond to the previous question."];
    }
  }

  // sendSpecialChat is an array that will override the next thing the bot says with the second value if the first value is true. 
  // If the first value is false the bot will say the next thing in the script.

  // Send user's message.
  // -------------------------------------------------------------------
  send(nextMessage.sender, nextMessage.message);

  // Count 1 more chat that the user has sent.
  // -------------------------------------------------------------------
  userCount += 1;

  // Ask the bot for another chat.
  // -------------------------------------------------------------------
  lookForChat()
}

/**
 * name: botChat()
 * purpose: picks the bot's next message.
*/

// -------------------------------------------------------------------

function botChat() {
    // Set the bot as the sender of the next message.
    // -------------------------------------------------------------------
    nextMessage.sender = "bot";

    // if this is the last message, log session end time
    // -------------------------------------------------------------------
    if (botCount >= bot_script.length) {
        nextMessage.message = goodbye;
        botSilent = true;

        session_end_dateobj = new Date();
        session_end_time = session_end_dateobj.toISOString();

        // display results
        // -------------------------------------------------------------------
        display_results_alert(session_uuid_string, session_start_time, session_end_time);

        // potentially save just these details in a seperate table

    } else {
        // Set the bot's next message as the next string in the bot_script array.
        // -------------------------------------------------------------------

        // save next message into variable for further checking
        var check_next_msg = bot_script[botCount];

        if(check_next_msg == "Complete the next 3 letters of the alphabet following: ") {
          var rand_opts = ["ABCD", "EFGH", "STUV", "OPQR"];
          var rand_choice = rand_opts[Math.floor(Math.random() * rand_opts.length)];
          check_next_msg += rand_choice;
        } else if(check_next_msg == "On a bright sunny day in New Orleans, the music was playing through the streets. If you are paying attention and reading this, type the number: ") {
          var rand_opts = ["0", "3", "36", "369"];
          var rand_choice = rand_opts[Math.floor(Math.random() * rand_opts.length)];
          check_next_msg += rand_choice;
        } else if (check_next_msg == "Retype the sequence: ") {
          var rand_opts = ["162-235-984", "162235984", "16-2235984", "162-235984", "1622-35984", "16223-5984"];
          var rand_choice = rand_opts[Math.floor(Math.random() * rand_opts.length)];
          check_next_msg += rand_choice;
        }

        // assign final result of message after dynamic elements
        nextMessage.message = check_next_msg;
    }

    // Check intervening_msg to see if anything special should happen.
    // -------------------------------------------------------------------
    if (intervening_msg[0]) {
        nextMessage.message = intervening_msg[1]; 
    }

    // Send the bot's message.
    // -------------------------------------------------------------------
    send(nextMessage.sender, nextMessage.message);

    // Count 1 more chat that the bot has sent unless the chat was a intervening_msg.
    // -------------------------------------------------------------------
    if (intervening_msg[0]) {
        intervening_msg = [false, ""];
    } else {
        botCount += 1;
    }

    // Start listening again after the bot has sent a message.
    // -------------------------------------------------------------------
    listenFor();
}

/**
 * name: chatEngine.js
 * purpose: code to find chats from the bot and user and create the chat interface. Because the chat window will change as you type we need to manipulate the DOM (Document Object Model) and add HTML to display on the screen.
*/

// -------------------------------------------------------------------

function lookForChat() {
  // If there have been no chats yet, start the bot.
  if (count == 0) {
    startBot();
  }
  
  // check who sent the last chat
  last = nextMessage.sender; 
  
  if (last == "bot") {
    // if the bot chatted last wait for the user to send a chat
    userChat();
    
  } else {
    // Send the cursor to the compose text area.
    composer.focus();
    
    // If botSilent is true the bot is done chatting
    // Set nextMessage.sender to "bot" to make the user chat next
    // Run listenFor() to wait for the user to chat.
    if (botSilent) {
      nextMessage.sender = "bot";
      nextMessage.message = "";
      listenFor();
      
    } else {
      
      // If the user chatted last or the chat just started have the bot send a chat.
      // Set the appropriate wait time to make the bot feel realistic.
      // Then run the botChat function which will find the right message for the bot
      if (count == 0) {
        wait = 100;
      } else {
        wait = 500;
      }
      setTimeout(function(){
        botChat();
      }, wait);
    }
  }
}

// -------------------------------------------------------------------


// startBot is a function that starts the bot for the first time. It clears away the start button from the HTML.
function startBot(){

    // clear chat area
    // -------------------------------------------------------------------
    chatArea.innerHTML = '';
    document.getElementById('compose-area').style.display = 'block';

    // set session identifiers
    // -------------------------------------------------------------------
    session_uuid_string = get_uuid_string();
    session_start_dateobj = new Date();
    session_start_time = session_start_dateobj.toISOString();
}


/**
 * name: send()
 * purpose: sends the next message stored in nextMessage object.
 * @param  {String} sender sender of message
 * @param  {String} message message content
*/

function send(sender, message) {
    // store message record
    // -------------------------------------------------------------------
    message_uuid_string = get_uuid_string();
    message_arrival_time = new Date();
    message_iso_time = message_arrival_time.toISOString();

    // prepare message record
    // -------------------------------------------------------------------
    message_record = [message_iso_time, session_uuid_string, message_uuid_string, count, sender, message];
    message_json = JSON.stringify(message_record);

    // upload to API
    // -------------------------------------------------------------------
    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
    var theUrl = api_endpoint_base + "messages.php";
    xmlhttp.open("POST", theUrl);
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(message_json);
    
    // Insert the nextMessage into the HTML
    // -------------------------------------------------------------------
    chatArea.insertAdjacentHTML("beforeend", "<div id='chat-" + count + "' class='chat-container'><div class='chat-wrapper' id='chat-a-" + count + "'><div class='avatar avatar-" + sender + "'></div><p id='a-' class='chat-" + sender + "'>" + message + "</p></div></div>");

    // Scroll the most recent message onto the screen.
    // -------------------------------------------------------------------
    document.getElementById('chat-' + count).scrollIntoView();

    // increase message counter
    // -------------------------------------------------------------------
    count += 1;
}