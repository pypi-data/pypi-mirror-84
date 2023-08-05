import re


def RegexBoxNewLine(value: str) -> str:
    subst = ""
    normalizedValue = ""
    r1 = r"%newline%"
    result = re.sub(r1, subst, value, 0, re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue


def RegexBoxDoubleQuote(value: str) -> str:
    subst = "\\\\\""
    normalizedValue = ""
    r1 = r"\""
    result = re.sub(r1, subst, value, 0, re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue


def RegexBoxAmp(value: str) -> str:
    subst = "&amp;"
    normalizedValue = ""
    r1 = r"&"
    result = re.sub(r1, subst, value, 0, re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue


def RegexBoxStrAt(value: str) -> str:
    normalizedValue = ""
    subst = "%@"
    r1 = r"%s"
    result = re.sub(r1, subst, value, 0, re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue

def RegexBoxBR(value: str) -> str:
    normalizedValue = ""
    subst = "<br>"
    r1 = r"<BR>"
    result = re.sub(r1, subst, value, 0, re.MULTILINE | re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue
def RegexBoxDF(value: str) -> str:
    subst = "%$1"
    normalizedValue = ""
    r1 = r"%([@df])"
    result = re.sub(r1, subst, value, 0, re.IGNORECASE)
    if result:
        normalizedValue = result
    else:
        normalizedValue = value

    return normalizedValue
