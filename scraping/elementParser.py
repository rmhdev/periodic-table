
def parseAtomicNumber(value):
    return int(value)

def parseGroup(value):
    if (value == "" or value == u'\xe2\x80\x93'):
        return None
    return int(value)

def parsePeriod(value):
    return int(value)

def parseTemperatureKelvin(value):
    if (value == "" or value == u'\xe2\x80\x93'):
        return None
    elements = value.split()
    if len(elements) > 1:
        return float(elements[0])
    return float(value)
    
def parseAtomicWeight(value):
    extra = None
    if value.find('[') == 0:
        weight = value[value.find('[')+1:value.find(']')]
    else:
        weight = value[:value.find('(')]
        extra = int(value[value.find('(')+1:value.find(')')])
    return [float(weight), extra]

def parseDensity(value):
    if (value == "" or value == u'\xe2\x80\x93'):
        return None
    return float(value)