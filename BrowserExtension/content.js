console.log("From my extension")

// Connect to websocket
var ws = new WebSocket("ws://localhost:8765");


//get password input
let pass = document.querySelector('input[type="password"]')

//isolate dom
let myDiv = document.createElement("div");
pass.parentNode.insertBefore(myDiv, pass)
let host = myDiv;
let root = host.attachShadow({ mode: 'closed' });
input = pass.cloneNode(true);
input.setAttribute('placeholder', 'Master password')
root.appendChild(input);
pass.style.display = "none"

//get domain and listen user input
let url = new URL(window.location.href);
let domain = url.hostname;
input.addEventListener("keyup", function (event) {
    if (event.keyCode === 113) {
        ws.send("DOMAIN--" + domain + "|PASSWORD--" + input.value);
    }
})
ws.onopen = function () {
    // Web Socket is connected, send data using send()
    ws.send("Connected to web extension!!!")
};

ws.onmessage = function (event) {
    console.log(event.data);
    pass.value = event.data;
    input.setAttribute("style", "display:none");
    pass.style.display = "block"
    pass.focus();
}
