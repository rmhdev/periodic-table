var request = require('supertest')
    , utils = require('../lib/utils')
    , assert = require('assert');

var app = utils.startServer(3000);

describe('Periodic table API', function() {

    //before(function(done){
    //    http.createServer(app,done);
    //});

    it('GET / should be successful', function(done) {
        request(app)
            .get('/')
            .expect(200, done);
    });

    describe('GET /elements call', function(done) {

        it('GET /elements should be successful', function(done) {
            request(app)
                .get('/elements')
                .expect(200)
                .expect('Content-Type', /json/, done);
        });

        it('GET /elements should return 5 elements in the first page', function(done) {
            request(app)
                .get('/elements')
                .expect(200, function(err, res) {
                    assert.equal(res.body.page, 1);
                    assert.equal(res.body.perPage, 5);
                    assert.equal(res.body.elements.length, 5);
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
