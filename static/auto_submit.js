window.onload = function() {
// Onload event of Javascript
// Initializing timer variable
var x = 3;
var y = document.getElementById("timer");
// Display count down for 3s
setInterval(function() {
if (x <= 4 && x >= 1) {
x--;
y.innerHTML = '' + x + '';
if (x == 1) {
x = 4;
}
}
}, 1000);

// Form Submitting after 3s
var auto_refresh = setInterval(function() {
submitform();
}, 5*60*1000);
// Form submit function
function submitform() {
document.getElementById("form").submit();
}
};
