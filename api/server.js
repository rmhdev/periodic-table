var utils   = require('./lib/utils'),
    port    = 3000,
    server  = utils.startServer(port);

console.log("Periodic table server: listening on port " + port);
