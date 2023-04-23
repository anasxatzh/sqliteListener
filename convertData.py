
from .callHelper import NestedDictionary

import sqlalchemy

def valsFromChild(session_,
                  forTable,
                  forKey,
                  forVal,
                  childData) -> list:
    
    setData = set()

    if len(childData) > 999:setData = set(childData)
    if type(forTable) == sqlalchemy.sql.Selectable.Alias:
        convertDict = _valsToForKey(session_,
                                    forTable,
                                    forKey,
                                    forVal,
                                    setData or childData)
        return [convertDict[k] for k in childData]


    else:
        keyCol = [getattr(forTable,
                          forKey)]
        if isinstance(childData, dict):
            comp = True
            valColumns = [getattr(forTable,
                                  v) for v in childData.keys()]
            keys = list(childData.keys())
            filters = [valColumns[k].in_(childData[keys[k]]) for k in range(len(keys))]

        else:
            comp = False
            valColumns = [getattr(forTable, forVal)]
            filters = [valColumns[0].in_(setData or childData)]
        
        rows = session_.query(*keyCol, *valColumns).distinct().filter(*filters).all()


        if comp:
            nestedConvDict = NestedDictionary()
            for row in rows:
                nestedConvDict[[col for col in row[1:]]] = row[0]

            convKeys = []
            length_ = len(childData[list(childData.keys())[0]])

            for j in range(length_):
                convKeys.append([childData[k][j]] for k in childData.keys())

            return [nestedConvDict[k] for k in convKeys]
        else:
            convertDict = {getattr(row,
                                   forVal) : getattr(row,
                                                     forKey) for row in rows}

            return [convertDict[i] for i in childData]






def _valsToForKey(session_,
                  forSubQuer,
                  forKey,
                  forVal,
                  childData) -> dict:

    rows = session_.query(getattr(forSubQuer.c, forKey), getattr(forSubQuer.c, forVal)). \
        filter(getattr(forSubQuer.c, forVal).in_(childData)).all()
    conversion_dict = {getattr(row, forVal): getattr(row, forKey) for row in rows}

    return conversion_dict
