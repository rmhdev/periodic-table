#!/usr/local/bin python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import json
import elementParser

class ChemicalElementsScrapper:

    def __init__(self, logger):
        self.logger = logger
        self.elements_parser = None
        #self.uri = "http://en.wikipedia.org/wiki/List_of_elements"
        self.uri = "http://localhost/~rober/wikipedia/List_of_elements.html"
        self.http_headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; es-ES)'
        }

    def start(self):
        req = requests.get(self.get_uri(), headers=self.get_http_headers())
        if req.status_code != 200:
            self.logger.debug("error in request")
            exit()
        self.__process_request(req)

    def get_uri(self):
        return self.uri

    def get_http_headers(self):
        return self.http_headers

    def __process_request(self, request):
        soup = BeautifulSoup(request.text)
        self.elements_parser = ChemicalElementsParser(soup, self.logger);
        self.elements_parser.parse()
        self.save()

    def save(self):
        self.__save_json('data/elements.json', self.elements_parser.get_elements())
        self.__save_json('data/categories.json', self.elements_parser.get_categories())

    def __save_json(self, filename, data):
        with open(filename, 'wb') as fp:
            json.dump(data, fp, indent=2)
            fp.close()


class ChemicalElementsParser:

    def __init__(self, soup, logger):
        self.logger = logger
        self.soup = soup
        self.table_attributes = { "class": "wikitable" }
        self.elements = []
        self.categories_parser = None

    def parse(self):
        self.categories_parser = ElementCategoriesParser(self.soup, self.logger)
        self.categories_parser.parse()
        self.elements = []
        rowNumber = 0
        table_elements = self.soup.find("table", self.table_attributes)
        for tr in table_elements.find_all("tr", recursive=False):
            if "style" in tr.attrs:
                continue
            if (rowNumber == 0):
                rowNumber = 1
            else: 
                chemicalElementParser = ChemicalElementParser(tr, self.logger)
                color = chemicalElementParser.get_category_color()
                category = self.categories_parser.find_by_color(color)
                element = chemicalElementParser.get_json(category)
                self.elements.append(element)
        self.logger.info("Chemical elements found: %d" % len(self.elements))
    
    def get_elements(self):
        return self.elements

    def get_categories(self):
        return self.categories_parser.get_categories()



class ChemicalElementParser:

    def __init__(self, tr, logger):
        self.tr = tr
        self.logger = logger        
        self.tds = tr.find_all("td", recursive=False)

    def get_category_color(self):
        td = self.tds[1]
        category_color = ""
        m = re.search("background-color:(.+?)$", td["style"])
        if m:
            category_color = m.group(1)
        return category_color

    def get_json(self, category):
        atomic_weight = elementParser.parseAtomicWeight(self.__process_atomic_weight())
        atomic_mass = atomic_weight[0]
        atomic_mass_uncertainty = atomic_weight[1]
        jsonElement = {
            "atomic_number":            elementParser.parseAtomicNumber(      self.tds[0].find(text=True)),
            "symbol":                   elementParser.parseSymbol(            self.tds[1].find(text=True)),
            # "name":                   tds[2].find(text=True),
            # "etymology":              tds[3].findAll(text=True),
            "group":                    elementParser.parseGroup(             self.tds[4].find(text=True)),
            "period":                   elementParser.parsePeriod(            self.tds[5].find(text=True)),
            "density":                  elementParser.parseDensity(           self.tds[7].find(text=True)),
            "melting_point":            elementParser.parseTemperatureKelvin( self.tds[8].find(text=True)),
            "boiling_point":            elementParser.parseTemperatureKelvin( self.tds[9].find(text=True)),
            "specific_heat_capacity":   elementParser.parseTemperatureKelvin( self.tds[10].find(text=True)),
            "electronegativity":        elementParser.parseElectronegativity( self.tds[11].find(text=True)),
            "atomic_mass":              atomic_mass,
            "atomic_mass_uncertainty":  atomic_mass_uncertainty,
            "category":                 category
            # "abundance":              tds[12].string
        }
        jsonElement["href"] = self.tds[2].a.get("href")
        return jsonElement

    def __process_atomic_weight(self):
        td = self.tds[6]
        weight = td.find("span", {"class": "sorttext"})
        if (weight):
            weight = weight.find(text=True)
        if (weight == None):
            weight = td.find(text=True)
        return weight






class ElementCategoriesParser:

    def __init__(self, soup, logger):
        self.soup = soup
        self.logger = logger
        self.categories = []
        self.categories_by_color = {}
        self.table_attributes = { "cellpadding": "3" }

    def parse(self):
        categories_table = self.soup.find("table", self.table_attributes)
        self.__process_categories_table(categories_table)

    def __process_categories_table(self, table_categories):
        for td in table_categories.find_all("td"):
            category_name = self.__get_category_name_from_td(td)
            if category_name is not None:
                category_color = self.__get_category_color_from_td(td)
                if (self.__is_category_color_correct(category_color)):
                    self.categories_by_color[category_color] = category_name
                    link = td.find("a")
                    href = None
                    if link is not None:
                        href = link.get("href")
                    self.categories.append({
                        "name": category_name,
                        "href": href,
                    })

    def __get_category_name_from_td(self, td):
        return ("".join(td.find_all(text=True))).replace("\n", " ")

    def __get_category_color_from_td(self, td):
        category_color = ""
        m = re.search("background:(.+?);", td["style"])
        if m:
            category_color = m.group(1)
        return category_color

    def __is_category_color_correct(self, color):
        return (color and color != "#f0f0f0")

    def get_categories(self):
        return self.categories

    def find_by_color(self, color):
        if color in self.categories_by_color:
            return self.categories_by_color[color]
        return None
