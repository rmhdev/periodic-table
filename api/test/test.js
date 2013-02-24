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

                request(app)
                    .get("/elements/" + lastPage)
                    .expect(200, function (err, res) {
                        assert.equal(res.body.nextPage, 0);
                        done();
                    });
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
            .expect('Content-Type', /json/)
            .expect(404, done);
    });

    it("GET /elements/0 should return error", function (done) {
        request(app)
            .get("/elements/0")
            .expect('Content-Type', /json/)
            .expect(404, done);
    });

    it("GET /elements/qwerty should return error", function (done) {
        request(app)
            .get("/elements/qwerty")
            .expect('Content-Type', /json/)
            .expect(404, done);
    });

});


describe('GET /element call', function () {

    it("GET /element/h should be successful", function (done) {
        request(app)
            .get("/element/h")
            .expect(200)
            .expect('Content-Type', /json/, done);
    });

    it("GET /element/h should return Hydrogen information", function (done) {
        request(app)
            .get("/element/H")
            .expect(200, function (err, res) {
                assert.equal(res.body.element.symbol, "H");
                done();
            });
    });

    it("GET /element/H should return Hydrogen information", function (done) {
        request(app)
            .get("/element/H")
            .expect(200, function (err, res) {
                assert.equal(res.body.element.symbol, "H");
                done();
            });
    });

    it("GET /element/al should return Aluminium information", function (done) {
        request(app)
            .get("/element/al")
            .expect(200, function (err, res) {
                assert.equal(res.body.element.symbol, "Al");
                done();
            });
    });

    it("GET /element/AL should return Aluminium information", function (done) {
        request(app)
            .get("/element/AL")
            .expect(200, function (err, res) {
                assert.equal(res.body.element.symbol, "Al");
                done();
            });
    });

    it("GET /element/uut should return Ununtrium information", function (done) {
        request(app)
            .get("/element/uut")
            .expect(200, function (err, res) {
                assert.equal(res.body.element.symbol, "Uut");
                done();
            });
    });

    it("GET /element/UUT should return Ununtrium information", function (done) {
        request(app)
            .get("/element/UUT")
            .expect(200, function (err, res) {
                assert.equal(res.body.element.symbol, "Uut");
                done();
            });
    });

    it("GET /element (no parameter) should return error", function (done) {
        request(app)
            .get("/element")
            .expect(404, done());
    });

    it("GET /element/qwerty should return error", function (done) {
        request(app)
            .get("/element/qwerty")
            .expect(404)
            .end(function (err, res) {
                done();
            });
    });
});

// it('GET /elements/h should be successful', function(done) {
//     request(app)
//         .get('/elements/h')
//         .expect(200, done);
// });


