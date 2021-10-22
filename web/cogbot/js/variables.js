// declaring variables for later use
// -------------------------------------------------------------------

// chatArea is the variable that stores the place on the screen the chats will appear.
var chatArea = document.getElementById('chat-area');

// declare counters
// -------------------------------------------------------------------

var randomize_questions = true;

// count is a variable that stores how many total chats have been sent.
var count = 0;

// botCount and userCount are variables that store how many chats each the bot and the suer have sent.
var botCount = 0;
var userCount = 0;

// for invalid responses
var invalid_resp_count = 0;
var invalid_resp_max = 3;

// declare messaging params
// -------------------------------------------------------------------

// nextMessage is an object variable that stores the next message that will be sent and who will be sending it.
var nextMessage = {
  message: "",
  sender: ""
};

// sendSpecialChat is a variable that stores if the bot should say something off script, and what that should be.
var intervening_msg = [false, ""];

// botSilent is a variable that stores when the bot is done speaking because it has said all of the things in the script.
var botSilent = false;

// declare API information
// -------------------------------------------------------------------

var api_endpoint_base = "https://cogtasks.com/api/cogbot/";

// declare identifier variables
// -------------------------------------------------------------------

var session_uuid_string = '';
var session_start_dateobj = '';
var session_start_time = '';
var session_end_dateobj = '';
var session_end_time = '';

var message_uuid_string = '';
var message_arrival_time = '';
var message_iso_time = '';

// for consistent formatting
// -------------------------------------------------------------------
var alert_spacer_string = "\r\n";

// bot's assessments
// -------------------------------------------------------------------

var bot_script = [
  "What is your study word code?",
  "What is your age?",
  "On a bright sunny day in New Orleans, the music was playing through the streets. If you are paying attention and reading this, type the number: ",
  "Complete the next 3 letters of the alphabet following: ",
  "What is today's date? (format: MM/DD/YYYY)",
  "Enter the number that matches the current day of the week:\n[1] Sunday\n[2] Monday\n[3] Tuesday\n[4] Wednesday\n[5] Thursday\n[6] Friday\n[7] Saturday",
  /* "Provide three keywords describing positive events you experienced today (e.g., snow, pets, programming)", */
  "Retype the sequence: ",
];

// goodbye is a variable that stores what the robot will say when it runs out of other things to say.
var goodbye = "Thank you for your time! Your data is instrumental in guiding this line of research to measure cognition in naturalistic environments. You may now close this window.";