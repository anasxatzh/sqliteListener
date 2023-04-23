

from enum import Enum
from datetime import datetime as dt
from datetime import date 


def setType(values : list,
            newType) -> list:

    if newType == str:
        newVals = [str(x) for x in values]

    elif newType == int or newType == float:
        floatVals = [float(x) for x in values]
    
        if newType == int:
            newVals = [int(round(x)) for x in floatVals]
        else:
            newVals = floatVals
    
    else:
        raise ValueError("NOT SUPPORTED VALUE")

    return newVals


def _setType(values,
             newType) -> list:

    newVals = []

    for elem in values:
        if len(elem) > 0 : newVals.append(newType(elem))
        else: newVals.append(None)
    return newVals



def getType(values):

    # if itterable
    if hasattr(values, "__len__") and (type(values) != type):

        valTypes = []
        for elem in values:
            valTypes.append(_getType(elem))
        typeSet = set(valTypes)

        if len(typeSet) == 1: return typeSet.pop()
        elif len(typeSet) == 2 and {None}.issubset(typeSet):
            return typeSet.difference({None}).pop()
        elif len(typeSet) <= 3 and {int, float}.issubset(typeSet):
            diff_ = typeSet.difference({int, float})
            if not bool(diff_) or diff_ == {None}:return float
            else:return str
    elif isinstance(values, Enum):return _getType(values.value)
    else:return _getType(values)









def _getType(value):

    match value:
        case int():return int

        case dt():return dt

        case float():return float

        case date():return date

        case bool():return bool

        case str():return str

        case None:return None

        case _ : raise Exception("NOT VALID VAL")





def isPythonType(val) -> bool:
    return val in [int, float, dt, str, bool, None]



def isInteger(val) -> bool:
    try:
        int(val)
        return True
    except ValueError:return False


def isFloat(val) -> bool:
    try:
        float(val)
        return True
    except ValueError:return False













