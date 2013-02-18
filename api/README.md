Periodic Table API

To install all dependencies:

`npm install`

To populate the DB:

`mongoimport --db elementDb --collection elements --jsonArray --file scraping/data/elements.json`

To launch tests:

`./node_modules/mocha/bin/mocha test/test.js --reporter spec`

To launch server:

`node server.js`
