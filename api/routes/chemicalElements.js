exports.findAll = function (request, response) {
    response.send(findChemicalElements());
};

exports.findBySlug = function (request, response) {
    var slug = request.params.slug;
    response.send(findChemicalElementBySlug(slug));
};

function findChemicalElements() {
    return {
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
}

function findChemicalElementBySlug(slug) {
    return {
        "element":
        {
            "name": "Hydrogen",
            "symbol": "H",
            "slug": "h"
        }
    };
}