module.exports = {
    startServer: function(port) {
        var express             = require("express"),
            chemicalElements    = require("./../routes/chemicalElements.js");

        var server = express();
        server.listen(port);

        server.get("/", function(request, response) {
            response.send("Periodic table API");
        });

        server.get("/elements", function(request, response) {
            response.send(chemicalElements.findAll(request, response));
        });

        server.get("/elements/:slug", function(request, response) {
            response.send(chemicalElements.findBySlug(request, response));
        });

        return server;
    }
};
