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


if __name__ == "__main__":
    unittest.main();
