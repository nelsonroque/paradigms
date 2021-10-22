// custom functions
function generateUUID() { 
  // Public Domain/MIT
  var d = new Date().getTime();
  if (typeof performance !== 'undefined' && typeof performance.now === 'function'){
  d += performance.now(); //use high-precision timer if available
  }
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
  var r = (d + Math.random() * 16) % 16 | 0;
  d = Math.floor(d / 16);
  return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
}

function randomStr(len, arr) { 
  var ans = ''; 
  for (var i = len; i > 0; i--) { 
      ans +=  
        arr[Math.floor(Math.random() * arr.length)]; 
  } 
  return ans; 
}

/** functions **/
function alphabetRange (start, end) {
  return new Array(end.charCodeAt(0) - start.charCodeAt(0) + 1).fill().map((d, i) => String.fromCharCode(i + start.charCodeAt(0)));
}
function keyCodeRange (start, end) {
  var start = start.charCodeAt(0);
  return new Array(end.charCodeAt(0) - start + 1).fill().map((d, i) => i + start);
}
function numberRange (start, end) {
  return new Array(end - start + 1).fill().map((d, i) => i + start);
}