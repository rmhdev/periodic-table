
def parseAtomicNumber(value):
    return int(value)

def parseGroup(value):
    if (__isUndefinedValue(value)):
        return None
    return int(value)

def parsePeriod(value):
    return int(value)

def parseTemperatureKelvin(value):
    if (__isUndefinedValue(value)):
        return None
    elements = value.split()
    if len(elements) > 1:
        return float(elements[0])
    return float(value)
    
def parseAtomicWeight(value):
    extra = None
    if value.find('[') == 0:
        weight = __getValueBetween(value, '[', ']')
    else:
        weight = value[:value.find('(')]
        extra = int(__getValueBetween(value, '(', ')'))
    return [float(weight), extra]

def parseDensity(value):
    if (__isUndefinedValue(value)):
        return None
    return float(value)

def parseSymbol(value):
    return str(value).strip().capitalize()

def parseElectronegativity(value):
    if (__isUndefinedValue(value)):
        return None
    return float(value)

def __isUndefinedValue(value):
    return (value == "" or value == u'\xe2\x80\x93' or value == None)

def __getValueBetween(value, itemFrom, itemTo):
    return value[value.find(itemFrom)+1:value.find(itemTo)]
