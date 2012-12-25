"use strict";

var limitPerPage = 5,
    fields = {
        "_id": false,
        "atomic_number": true,
        "symbol": true,
        "group": true,
        "period": true,
        "category": true
    };

var mongodb = require('mongodb'),
    server = new mongodb.Server("127.0.0.1", 27017, {}),
    db = new mongodb.Db("elementsDb", server, {safe:true});

db.open(function(err, db) {
    if (!err) {
        console.log("Opening connection to DB: OK");
    }
});

exports.findAll = function (request, response) {
    var page = 1;//request.params.page
    var skip = limitPerPage * (page - 1);
    var queryOptions = {
        "limit": limitPerPage,
        "skip": skip,
        "sort": "symbol"
    };
    var collection = db.collection("elements");
    collection.find({}, fields, queryOptions).toArray(function(err, elements) {
        var apiData = {
            "page":     page,
            "perPage":  limitPerPage,
            "elements": elements
        };
        response.json(apiData);
    });
};

exports.findBySlug = function (request, response) {
    var symbol = request.params.symbol;
    var collection = db.collection("elements");
    collection.findOne({"symbol":symbol}, fields, function (err, element) {
        if (err) {
            console.log("error retrieving element by slug");
        }
        var apiData = {
            "element": element
        };
        response.json(apiData);
    });
};
