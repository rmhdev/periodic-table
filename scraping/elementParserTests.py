from elementParser import *
import unittest

class ElementParserTest(unittest.TestCase):

    def testParseAtomicNumber(self):
        self.assertEqual(1, parseAtomicNumber("1"))
        self.assertEqual(2, parseAtomicNumber(" 2"))
        self.assertEqual(3, parseAtomicNumber("3 "))

    def testParseGroup(self):
        self.assertEqual(1, parseGroup("1"))
        self.assertEqual(2, parseGroup(" 2"))
        self.assertEqual(3, parseGroup("3 "))
        self.assertEqual(None, parseGroup(""))
        self.assertEqual(None, parseGroup(u'\xe2\x80\x93'))

    def testParsePeriod(self):
        self.assertEqual(1, parsePeriod("1"))
        self.assertEqual(2, parsePeriod(" 2"))
        self.assertEqual(3, parsePeriod("3 "))

    def testParseTemperatureKelvin(self):
        self.assertEqual(1.00, parseTemperatureKelvin("1"))
        self.assertEqual(1.23, parseTemperatureKelvin("1.23"))
        self.assertEqual(14.175, parseTemperatureKelvin("14.175"))
        self.assertEqual(None, parseTemperatureKelvin(""))
        self.assertEqual(None, parseTemperatureKelvin(u'\xe2\x80\x93'))
        self.assertEqual(3915, parseTemperatureKelvin("3915 (Sublimates)"))

    def testParseAtomicWeight(self):
        self.assertEqual([1.008, 1], parseAtomicWeight("1.008(1)"))
        self.assertEqual([4.002602, 2], parseAtomicWeight("4.002602(2)"))
        self.assertEqual([44.955912, 6], parseAtomicWeight("44.955912(6)"))
        self.assertEqual([98, None], parseAtomicWeight("[98]"))

    def testParseDensity(self):
        self.assertEqual(7, parseDensity("7"))
        self.assertEqual(9.32, parseDensity("9.32"))
        self.assertEqual(None, parseDensity(""))
        self.assertEqual(None, parseDensity(u'\xe2\x80\x93'))



if __name__ == "__main__":
    unittest.main();
