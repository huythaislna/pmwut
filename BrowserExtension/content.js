console.log("From my extension")
var ws = new WebSocket("ws://localhost:8765");
let url = new URL(window.location.href);
let domain = url.hostname;
let pass = document.getElementById("pass");
let myDiv = document.createElement("div");

pass.parentNode.insertBefore(myDiv, pass)
let host = myDiv;
let root = host.attachShadow({ mode: 'closed' });
input = pass.cloneNode(true);
root.appendChild(input);
pass.style.display = "none"
input.addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
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
