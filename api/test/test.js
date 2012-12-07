var request = require('supertest')
    , utils = require('../lib/utils');

var app = utils.startServer(3000);

describe('Periodic table API', function() {

    //before(function(done){
    //    http.createServer(app,done);
    //});

    it('GET / should return 200', function(done) {
        request(app)
            .get('/')
            .expect(200, done);
    });

    it('GET /elements should return 200', function(done) {
        request(app)
            .get('/elements')
            .expect(200, done);
    });

    it('GET /elements/h should return 200', function(done) {
        request(app)
            .get('/elements/h')
            .expect(200, done);
    });


});
