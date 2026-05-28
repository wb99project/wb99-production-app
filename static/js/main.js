const statusElement = document.getElementById("connection-status");
const payloadElement = document.getElementById("live-payload");

const socket = io();

function setStatus(text) {
  statusElement.textContent = text;
}

socket.on("connect", () => {
  setStatus("Connected");
});

socket.on("disconnect", () => {
  setStatus("Disconnected");
});

socket.on("connect_error", () => {
  setStatus("Connection error");
});

socket.on("new_data", (data) => {
  const formatted = JSON.stringify(data, null, 2);
  payloadElement.textContent = formatted;
});
