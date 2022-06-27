import re;
from dateutil  import parser;

def checkJmbg(jmbg):
    if len(jmbg) != 13:
        return False;
    if not allDigits(jmbg):
        return False;
    dayString = jmbg[0:2];
    monthString = jmbg[2:4];
    yearString = jmbg[4:7];
    regionString = jmbg[7:9];
    if not okDay(dayString) or not okMonth(monthString) or not okYear(yearString):
        return False;
    if (not fromSerbia(regionString)):
        return  False;
    if (not controlDigitOk(jmbg)):
        return False;

    return True;

def checkEmail(email):
    if (len(email) > 256):
        return False;
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b';
    result = re.match(regex, email);
    return not (result is None);

def checkPassword(password):
    if (len(password) < 8 or len(password) > 256):
        return False;
    result = re.match(".*\d.*", password);
    if (result is None):
        return False;
    result = re.match(".*[a-z].*", password);
    if (result is None):
        return False;
    result = re.match(".*[A-Z].*", password);
    if (result is None):
        return False;
    return True;

def allDigits(inputSting):
    result = re.match("^\d+$", inputSting);
    return not (result is  None);

def okMonth(monthString):
    month = int(monthString);
    return month >= 1 and month <= 12;

def okYear(yearString):
    year = int(yearString);
    return year >= 0 and year <= 999;

def okDay(dayString):
    day = int(dayString);
    return day >= 1 and day <= 31;

def fromSerbia(regionString):
    region = int(regionString);
    return region >= 70 and region <= 99;

def controlDigitOk(jmbg):
    digits = [int(x) for x in jmbg];
    controlSum = 7 * (digits[0] + digits[6]) +\
                 6 * (digits[1] + digits[7]) +\
                 5 * (digits[2] + digits[8]) +\
                 4 * (digits[4] + digits[9])+\
                 3 * (digits[5] + digits[10])+\
                 2 * (digits[6] + digits[11]);
    controlSum = controlSum % 11;
    if (controlSum > 1):
        controlSum = 11 - controlSum;
    return controlSum == digits[-1];

def checkBool(b):
    return isinstance(b, bool);

def parseIsoDateTime(datetime):
    if (datetime is None):
        return None;
    try:
        d = parser.isoparse(datetime);
    except :
        return None;
    return d;