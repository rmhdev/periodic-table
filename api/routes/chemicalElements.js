exports.findAll = function (request, response) {
    var chemicalElements = {
        "elements": [
            {
                "name": "Hydrogen",
                "symbol": "H",
                "slug": "h"
            },
            {
                "name": "Helium",
                "symbol": "He",
                "slug": "he"
            },
            {
                "name": "Lithium",
                "symbol": "Li",
                "slug": "li"
            }
        ]
    };
    response.send(chemicalElements);
};
