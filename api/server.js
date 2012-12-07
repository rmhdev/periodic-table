var express = require("express")
    chemicalElements = require("./routes/chemicalElements.js");

var app = express();

app.get("/", function(request, response) {
    response.send("Periodic table API");
});

app.get("/elements", function(request, response) {
    response.send(chemicalElements.findAll(request, response));
});

var portNumber = 3000;
app.listen(portNumber);
console.log("Periodic table server: listening on port " + portNumber);
