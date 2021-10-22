/**
 * name: listener.js
 * purpose: code to allow a user to choose to press the Start or ⏎ button, or to press the Enter key on their keyboard using the .keycode property.
*/

// listener is a variable to decide what input to look for
// -------------------------------------------------------------------
var enterListener = window;
var startListener = document.getElementById("startButton");
var sendListener = document.getElementById("sendButton");
var composer = document.getElementById("composer");

// Listen for the enter key on the start screen to start the chat
// -------------------------------------------------------------------
if (count == 0) {
  listenFor()
}

// A pair of functions that chain together to decide what part of the page to listen to, and then see if the 'enter' key is pressed. If it is, run the chat() function to submit an answer if there is one, and ask a new question.
function listenFor() {
  enterListener.addEventListener("keydown", listen);
  startListener.addEventListener("click", listen);
  sendListener.addEventListener("click", listen);
}

function listen(e) {
    // log individual keystrokes
    var keystroke_ts = new Date();

    // store keystroke record
    // -------------------------------------------------------------------
    keystroke_uuid_string = get_uuid_string();
    keystroke_arrival_time = new Date();
    keystroke_iso_time = keystroke_arrival_time.toISOString();

    // prepare keystroke record
    // -------------------------------------------------------------------
    keystroke_record = [keystroke_iso_time, session_uuid_string, message_uuid_string, keystroke_uuid_string, e.timeStamp, e.location, e.key, e.type, e.keyCode, e.which, e.ctrlKey, e.shiftKey, e.altKey, e.metaKey, e.repeat ];
    // for REST API: fruits.join("\t")
    keystroke_json = JSON.stringify(keystroke_record);

    // upload to API
    // -------------------------------------------------------------------
    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
    var theUrl = api_endpoint_base + "keystrokes.php";
    xmlhttp.open("POST", theUrl);
    xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlhttp.send(keystroke_json);

    // listen for enter or button click
    // -------------------------------------------------------------------
    if (e.keyCode === 13) {
        e.preventDefault();
        if (!e.shiftKey) {
            pauseListening();
            lookForChat();
        }
    }
    if (e.type == "click") {
        pauseListening();
        lookForChat(); 
    }
}
                                  
// To avoid double submitting on enter key if someone clicks the button we have top stop listening for enter until the robot sends a question.
function pauseListening() {
    enterListener.removeEventListener("keydown", listen);
    startListener.removeEventListener("click", listen);
    sendListener.removeEventListener("click", listen);
}