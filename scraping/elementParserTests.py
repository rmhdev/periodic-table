import elementParser
import unittest

class ElementParserTest(unittest.TestCase):

    def testParseAtomicNumber(self):
        self.assertEqual(1, elementParser.parseAtomicNumber("1"))
        self.assertEqual(2, elementParser.parseAtomicNumber(" 2"))
        self.assertEqual(3, elementParser.parseAtomicNumber("3 "))

    def testParseGroup(self):
        self.assertEqual(1, elementParser.parseGroup("1"))
        self.assertEqual(2, elementParser.parseGroup(" 2"))
        self.assertEqual(3, elementParser.parseGroup("3 "))
        self.assertEqual(None, elementParser.parseGroup(""))
        self.assertEqual(None, elementParser.parseGroup(u'\xe2\x80\x93'))
        self.assertEqual(None, elementParser.parseGroup(None))

    def testParsePeriod(self):
        self.assertEqual(1, elementParser.parsePeriod("1"))
        self.assertEqual(2, elementParser.parsePeriod(" 2"))
        self.assertEqual(3, elementParser.parsePeriod("3 "))

    def testParseTemperatureKelvin(self):
        self.assertEqual(1.00, elementParser.parseTemperatureKelvin("1"))
        self.assertEqual(1.23, elementParser.parseTemperatureKelvin("1.23"))
        self.assertEqual(14.175, elementParser.parseTemperatureKelvin("14.175"))
        self.assertEqual(None, elementParser.parseTemperatureKelvin(""))
        self.assertEqual(None, elementParser.parseTemperatureKelvin(u'\xe2\x80\x93'))
        self.assertEqual(3915, elementParser.parseTemperatureKelvin("3915 (Sublimates)"))
        self.assertEqual(None, elementParser.parseTemperatureKelvin(None))

    def testParseAtomicWeight(self):
        self.assertEqual([1.008, 1], elementParser.parseAtomicWeight("1.008(1)"))
        self.assertEqual([4.002602, 2], elementParser.parseAtomicWeight("4.002602(2)"))
        self.assertEqual([44.955912, 6], elementParser.parseAtomicWeight("44.955912(6)"))
        self.assertEqual([98, None], elementParser.parseAtomicWeight("[98]"))

    def testParseDensity(self):
        self.assertEqual(7, elementParser.parseDensity("7"))
        self.assertEqual(9.32, elementParser.parseDensity("9.32"))
        self.assertEqual(None, elementParser.parseDensity(""))
        self.assertEqual(None, elementParser.parseDensity(u'\xe2\x80\x93'))
        self.assertEqual(None, elementParser.parseDensity(None))

    def testParseSymbol(self):
        self.assertEqual("H", elementParser.parseSymbol("h"))
        self.assertEqual("H", elementParser.parseSymbol(" h"))
        self.assertEqual("Al", elementParser.parseSymbol("al"))
        self.assertEqual("Al", elementParser.parseSymbol(" al"))
        self.assertEqual("Uup", elementParser.parseSymbol(" UUP"))

    def testParseElectronegativity(self):
        self.assertEqual(1, elementParser.parseElectronegativity("1"))
        self.assertEqual(2.20, elementParser.parseElectronegativity("2.20"))
        self.assertEqual(None, elementParser.parseElectronegativity(u'\xe2\x80\x93'))
        self.assertEqual(None, elementParser.parseElectronegativity(None))


if __name__ == "__main__":
    unittest.main();
