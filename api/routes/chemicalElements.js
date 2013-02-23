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

exports.findBySlug = function (request, response) {
    var symbol = request.params.symbol,
        collection = db.collection("elements");

    collection.findOne({"symbol": symbol}, fields, function (err, element) {
        if (err) {
            console.log("error retrieving element by slug");
        }
        var apiData = {
            "element": element
        };
        response.json(apiData);
    });
};
