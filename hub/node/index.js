
// FrappeJS
// Do something awesome!
const frappe   = require("frappe");
const hub    = { };

frappe.socket.on("connection", (socket) =>
{
    socket.on("ping", () => socket.emit("pong"));
});

module.exports = hub;
