"use strict";

var limitPerPage = 2;

exports.findAll = function (request, response) {
    response.send(findChemicalElements(1));
};

exports.findBySlug = function (request, response) {
    var slug = request.params.slug.toLowerCase();
    response.send(findChemicalElementBySlug(slug));
};

var mongodb = require('mongodb'),
    server = new mongodb.Server("127.0.0.1", 27017, {}),
    db = new mongodb.Db("elementsDb", server, {safe:true});

db.open(function(err, db) {
    if (!err) {
        console.log("Opening connection to DB: OK");
    }
    //db.collection("elements", listAllData);
});

var listAllData = function (err, collection) {
    if (err) {
        console.log("error");
    }
    return collection.find().skip(10).limit(limitPerPage).toArray(function (err, results) {
        return results;
    });
};

function findChemicalElements(page) {
//    var skip = limitPerPage * (page - 1);
//    var elements = db.elements.find().skip(skip).limit(limitPerPage).toArray(function (err, results) {
//        if (err) {
//            console.log("error retrieving list of elements");
//            return [];
//        }
//        return results;
//    });

    var elements = db.collection("elements", listAllData);
    return {
        "page":     page,
        "perPage":  limitPerPage,
        "elements": "prueba"
    };
}

function findChemicalElementBySlug(symbol) {
    var element = db.elements.findOne({"symbol":symbol}, function (err, result) {
        if (err) {
            console.log("error retrieving element by slug");
            return {};
        }
        return element;
    });
    return {
        "element":element
    };
}