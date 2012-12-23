#!/usr/local/bin python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import json

class ChemicalElementsScrapper:

    def __init__(self, logger):
        self.logger = logger
        self.elements_parser = None
        #self.uri = "http://en.wikipedia.org/wiki/List_of_elements"
        self.uri = "http://192.168.1.102/~rober/wikipedia/List_of_elements.html"
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
                element = self.__get_data_from_table_row(tr)
                self.elements.append(element)
        self.logger.info("Chemical elements found: %d" % len(self.elements))

    def __get_data_from_table_row(self, tr):
        tds = tr.find_all("td", recursive=False)
        atomic_number = self.__process_int(tds[0].string)
        color = self.__get_category_color_from_td(tds[1])
        category = self.categories_parser.find_by_color(color)
        return {
            "atomic_number":            atomic_number,
            "symbol":                   tds[1].string,
            # "name":                     tds[2].find(text=True),
            "href":                     tds[2].a.get("href"),
            # "etymology":                tds[3].findAll(text=True),
            "group":                    self.__process_int(                tds[4].string),
            "period":                   self.__process_int(                tds[5].string),
            "atomic_weight":            self.__process_atomic_weight(      tds[6]  ),
            "density":                  self.__process_density(            tds[7]  ),
            "melting_point":            self.__process_temperature(        tds[8]  ),
            "boiling_point":            self.__process_temperature(        tds[9]  ),
            "specific_heat_capacity":   self.__process_temperature(        tds[10] ),
            "electronegativity":        self.__process_electronegativity(  tds[11] ),
            "category":                 category
            # "abundance":                tds[12].string
        }

    def __get_category_color_from_td(self, td):
        category_color = ""
        m = re.search("background-color:(.+?)$", td["style"])
        if m:
            category_color = m.group(1)
        return category_color

    def __process_int(self, digit):
        if digit is not None and self.__is_numeric(digit):
            digit = int(digit)
        return digit

    def __process_float(self, digit):
        if digit is not None and self.__is_numeric(digit):
            digit = float(digit)
        return digit

    def __is_numeric(self, item):
        if isinstance(item, str):
            return item.isdigit()
        return isinstance( item, ( int, long, float ))

    def __process_atomic_weight(self, td):
        weight = td.find("span", {"class": "sorttext"})
        if (weight):
            weight = weight.find(text=True)
        if (weight == None):
            weight = td.find(text=True)
        return weight

    def __process_density(self, td):
        return self.__process_numeric_cell(td)

    def __process_numeric_cell(self, cell):
        cell_value = cell.find(text=True)
        if (self.__is_dash(cell_value)):
            cell_value = None
        if cell_value is not None:
            if not cell_value.isdigit():
                digits = [float(s) for s in cell_value.split() if s.isdigit()]
                if len(digits) > 0:
                    cell_value = str(digits[0])
        return cell_value

    def __is_dash(self, text):
        return (text == u'\xe2\x80\x93')

    def __process_temperature(self, td):
        return self.__process_numeric_cell(td)

    def __process_electronegativity(self, td):
        return self.__process_numeric_cell(td)

    def get_elements(self):
        return self.elements

    def get_categories(self):
        return self.categories_parser.get_categories()


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
