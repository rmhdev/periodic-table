var request = require('supertest'),
    utils = require('../lib/utils'),
    assert = require('assert'),
    app = utils.startServer(3000);

describe('Periodic table API', function () {

    it('GET / should be successful', function (done) {
        request(app)
            .get('/')
            .expect(200, done);
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
                    done();
                });
        });

        // it('GET /elements/2 should return the second page', function(done) {
        //     request(app)
        //         .get('/elements/2')
        //         .expect(400, function(err, res) {
        //             assert.equal(res.body.page, 2)
        //         });
        // });
    });

    // it('GET /elements/h should be successful', function(done) {
    //     request(app)
    //         .get('/elements/h')
    //         .expect(200, done);
    // });

});
