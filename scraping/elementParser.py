
def parseAtomicNumber(value):
    return int(value)

def parseGroup(value):
    if (value == ""):
        return None
    return int(value)

def parsePeriod(value):
    return int(value)

def parseTemperatureKelvin(value):
    if (value == "" or value == u'\xe2\x80\x93'):
        return None
    return float(value)
