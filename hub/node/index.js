
// FrappeJS
// Do something awesome!
const frappe   = require("frappe")
const hub    = { }

frappe.socket.on("connection", (socket) =>
{
    // convention - [app].[domain].[object]:[action]
    socket.on("hub:ping", function () {
        console.log(`PING: ${socket.request.headers.origin}`)
        socket.emit("hub:pong", "pong")
    })

    
})

module.exports = hub
