
// Utility functions for potarig application web interface

// Set the page timeout in seconds - will cause a page reload.
var pageTimeout = 60;
var pageCountdown = pageTimeout;
var reloadPaused = false;

// Execute a HTTP request to set rig frequency and mode via flrig.
function set_flrig(freq, mode) {
  var url = window.location.href;
  var request = url.concat('/flrig?freq=', freq, '&mode=', mode);
  fetch(request);
}

// Save log data to a file.
function log_data(call, freq, mode, ref, name) {
  var url = window.location.href;
  var request = url.concat('/logdata?call=', call, '&freq=', freq, '&mode=', mode, '&ref=', ref, '&name=', name);
  fetch(request);
}

// Decrement the page timeout value, reload the page when zero.
function decrementPageTimeout() {
  if (reloadPaused == false) {
    pageCountdown -= 1;
    document.getElementById('timeout-seconds').innerText = pageCountdown;
    if (pageCountdown <= 0) {
      // This will refresh the page without performing a POST operation
      location.href = location.href;
    }
  } 
  else {
    document.getElementById('timeout-seconds').innerText = '--';
  }
}

// Set a timeout counter to reload the page.
function timedReload(timeout, el) {
  pageCountdown = timeout;
  setInterval(decrementPageTimeout, 1000);
}

// Pause/restart the page reload countdown.
function pauseReload() {
    if (reloadPaused == false) {
      reloadPaused = true;
      document.getElementById('timeout-seconds').innerText = '--';
      document.querySelector('#btn_pause').innerText = 'Restart'
    }
    else {
      document.getElementById('timeout-seconds').innerText = pageTimeout;
      document.querySelector('#btn_pause').innerText = ' Pause '
      pageCountdown = pageTimeout;
      reloadPaused = false;
    }
}

// Add an element to the current page to perform an automatic reload.
$(document).ready(function(){
    document.getElementById('timeout-seconds').innerText = pageTimeout;
    timedReload(pageTimeout);
});
