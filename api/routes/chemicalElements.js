"use strict";

var limitPerPage = 5,
    fields = {
        "_id": false,
        "atomic_number": true,
        "symbol": true,
        "group": true,
        "period": true,
        "category": true
    },
    mongodb = require('mongodb'),
    server = new mongodb.Server("127.0.0.1", 27017, {}),
    db = new mongodb.Db("elementsDb", server, {safe: true});

db.open(function (err, db) {
    if (err) {
        console.log("Error opening connection to DB.");
    }
});

exports.findAll = function (request, response) {
    var page = request.params.page ? parseInt(request.params.page, 10) : 1,
        skip = limitPerPage * (page - 1),
        collection = db.collection("elements"),
        queryOptions = {
            "limit": limitPerPage,
            "skip": skip,
            "sort": "symbol"
        };
    if (isNaN(page)) {
        response.json(404, {error: "Parameter must be an integer"});
    }

    collection.count(function (err, countTotal) {
        var lastPage = Math.ceil(countTotal / limitPerPage);
        if ((page < 1) || (page > lastPage)) {
            response.json(404, {error: "Page doesn't exist"});
        }
        collection.find({}, fields, queryOptions).toArray(function (err, elements) {
            var apiData = {
                "page":     page,
                "nextPage": (page < lastPage) ? page + 1 : 0,
                "previousPage": page - 1,
                "perPage":  limitPerPage,
                "totalElements": countTotal,
                "elements": elements
            };
            response.json(apiData);
        });
    });


};

exports.findBySymbol = function (request, response) {
    var symbol = request.params.symbol.toString(),
        searchSymbol = "",
        collection = db.collection("elements");

    if (symbol.length < 1) {
        response.json(404, {error: "You must specify a parameter"});
    }
    searchSymbol = symbol.charAt(0).toUpperCase() + symbol.slice(1).toLowerCase();

    collection.findOne({"symbol": searchSymbol}, fields, function (err, document) {
        //if (err) {
        //    console.log("error retrieving element by slug");
        //}
        if (!document) {
            response.json(404, {error: "Element doesn't exist"});
        }
        var apiData = {
            "element": document
        };
        response.json(apiData);
    });
};
