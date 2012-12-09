#!/usr/local/bin python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import csv, codecs, cStringIO

class ChemicalElementsScrapper:

    def __init__(self, logger):
        self.logger = logger
        self.elements = []
        self.categories = []
        #self.uri = "http://en.wikipedia.org/wiki/List_of_elements_by_symbol"
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
        elements_parser = ChemicalElementsParser(soup, self.logger);
        elements_parser.parse()
        self.elements = elements_parser.get_elements()
        self.save()

    def save(self):
        # with open("prueba.csv", 'wb') as f:
        #     writer = UnicodeWriter(f);
        #     writer.writerows(self.elements)
        #     f.close()


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
        self.logger.debug("Chemical elements found: %d" % len(self.elements))

    def __get_data_from_table_row(self, tr):
        tds = tr.find_all("td", recursive=False)
        atomic_number = tds[0].string
        color = self.__get_category_color_from_td(tds[1])
        category = self.categories_parser.find_by_color(color)
        self.logger.debug("[%3s] %s: %s", atomic_number, color, category)
        return {
            "atomic_number":            atomic_number,
            "symbol":                   tds[1].string,
            # "name":                     tds[2].find(text=True),
            "href":                     tds[2].a.get("href"),
            # "etymology":                tds[3].findAll(text=True),
            "group":                    tds[4].string,
            "period":                   tds[5].string,
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
        return cell_value

    def __is_dash(self, text):
        return (text == u'\xe2\x80\x93')

    def __process_temperature(self, td):
        return self.__process_numeric_cell(td)

    def __process_electronegativity(self, td):
        return self.__process_numeric_cell(td)

    def get_elements(self):
        return self.elements



class ElementCategoriesParser:
    def __init__(self, soup, logger):
        self.soup = soup
        self.logger = logger
        self.categories = {}
        self.table_attributes = { "cellpadding": "3" }

    def parse(self):
        categories_table = self.soup.find("table", self.table_attributes)
        self.__process_categories_table(categories_table)

    def __process_categories_table(self, table_categories):
        for td in table_categories.find_all("td"):
            category_name = ("".join(td.find_all(text=True))).replace("\n", " ")
            if category_name is not None:
                category_color = self.get_category_color_from_td(td)
                if (self.__is_category_color_correct(category_color)):
                    self.categories[category_color] = category_name

    def get_category_color_from_td(self, td):
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
        if color in self.categories:
            return self.categories[color]
        return None



class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)