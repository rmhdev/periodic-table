"use strict";

module.exports = {
    startServer: function (port) {
        var express             = require("express"),
            chemicalElements    = require("./../routes/chemicalElements.js"),
            server              = express();

        server.listen(port);

        server.get("/", function (request, response) {
            response.send("Periodic table API");
        });

        server.get("/elements/:page?", function (request, response) {
            chemicalElements.findAll(request, response);
        });

        server.get("/element/:symbol", function (request, response) {
            chemicalElements.findBySymbol(request, response);
        });

        return server;
    }
};
