"use strict";

var request = require('supertest'),
    utils = require('../lib/utils'),
    assert = require('assert'),
    app = utils.startServer(3000);

describe('GET / call', function () {

    it('GET / should be successful', function (done) {
        request(app)
            .get('/')
            .expect(200, done);
    });

});

describe('GET /elements call', function (done) {

    it('GET /elements should be successful', function (done) {
        request(app)
            .get('/elements')
            .expect(200)
            .expect('Content-Type', /json/, done);
    });

    var perPage = 5;

    it('GET /elements should return ' + perPage + ' elements', function (done) {
        request(app)
            .get('/elements')
            .expect(200, function (err, res) {
                assert.equal(res.body.perPage, perPage);
                assert.equal(res.body.elements.length, perPage);
                done();
            });
    });

    it('GET /elements should return the first page', function (done) {
        request(app)
            .get('/elements')
            .expect(200, function (err, res) {
                assert.equal(res.body.page, 1);
                assert.equal(res.body.nextPage, 2);
                assert.equal(res.body.previousPage, 0);
                done();
            });
    });

    it('GET /elements/2 should return the second page', function (done) {
        request(app)
            .get("/elements/2")
            .expect(200, function (err, res) {
                assert.equal(res.body.page, 2);
                assert.equal(res.body.previousPage, 1);
                assert.equal(res.body.nextPage, 3);
                done();
            });
    });

    it("GET /elements/X (where X is the last page) should indicate there's no next page", function (done) {
        var lastPage;
        request(app)
            .get("/elements")
            .expect(200, function (err, res) {
                var total = res.body.totalElements;
                lastPage = Math.ceil(total / perPage);
            });
        request(app)
            .get("/elements/" + lastPage)
            .expect(200, function (err, res) {
                assert.equal(res.body.nextPage, 0);
                done();
            });
    });

    it("GET /elements/1 should indicate there's no previous page", function (done) {
        request(app)
            .get("/elements/1")
            .expect(200, function (err, res) {
                assert.equal(res.body.previousPage, 0);
                done();
            });
    });

    it("GET /elements/1234 should return error", function (done) {
        request(app)
            .get("/elements/1234")
            .expect(404, done);
    });

    it("GET /elements/0 should return error", function (done) {
        request(app)
            .get("/elements/0")
            .expect(404, done);
    });

    it("GET /elements/qwerty should return error", function (done) {
        request(app)
            .get("/elements/qwerty")
            .expect(404, done);
    });

});


describe('GET /element call', function () {

    it("GET /element/h should be succesfull", function (done) {
        request(app)
            .get("/element/h")
            .expect(200, done);
    });

});

// it('GET /elements/h should be successful', function(done) {
//     request(app)
//         .get('/elements/h')
//         .expect(200, done);
// });


