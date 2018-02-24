
// FrappeJS
// Do something awesome!
const frappe   = require("frappe");
const hub    = { };

frappe.socket.on("connection", (socket) =>
{
    frappe.log.info("FooBar")
});

module.exports = hub;
