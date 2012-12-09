#!/usr/local/bin python
# -*- coding: utf-8 -*-

from elements import *
import logging

def get_logger():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    log = logging.getLogger("myapp")
    #sth = logging.StreamHandler()
    #sth.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    #log.addHandler(sth)
    log.setLevel(logging.DEBUG)
    return log

if __name__ == "__main__":
    logger = get_logger()
    logger.info("Scraping chemical elements list")
    scrapper = ChemicalElementsScrapper(logger)
    scrapper.start()
