
import convertTypes
from sqlalchemy import Integer, Float, String, DateTime, Boolean, Date

import pandas as pd
from datetime import datetime as dt
from datetime import date



class ManData(object):

    def __init__(self,
                 data):
        self.data = self._formatData(data)



    @property
    def columns_(self) -> dict:
        pyTypes = self.getPyType()
        sqlTypes = self.pyTypeToSqlType(pyTypes)
        return sqlTypes



    @staticmethod
    def _formatData(data):
        if isinstance(data, dict):return data
        elif isinstance(data, list):
            keys = data[0].keys()
            dictData = {key : [] for key in keys}
            for dat in data:
                if dat.keys() == keys:
                    for key in keys:
                        dictData[key].append(dat[key])
            return dictData
        else:raise ValueError("Input data is not list or dict")


    @staticmethod
    def pyTypeToSqlType(pyTypes_) -> dict:

        sqlTypes = dict()

        for key in pyTypes_:
            pyType = pyTypes_[key]
            if pyType == "integer" or pyType is int:
                sqlTypes[key] = [Integer]
            elif pyType == "float" or pyType is float:
                sqlTypes[key] = [Float]
            elif pyType == "string" or pyType is str:
                sqlTypes[key] = [String]
            elif pyType == "datetime" or pyType is dt:
                sqlTypes[key] = [DateTime]
            elif pyType == "date" or pyType is date:
                sqlTypes[key] = [Date]
            elif pyType == "bool" or pyType is bool:
                sqlTypes[key] = [Boolean]
            elif pyType is None:
                continue
            else:
                raise Exception("Type is not integer, float, str, bool, date, or datetime object!")
        return sqlTypes


    @property
    def dataframe_(self):
        try:return pd.DataFrame(self.data)
        except ValueError:raise ValueError("Not same len of arrays")


    def getPyType(self) -> dict:
        
        pyDict = {}
        if isinstance(self.data, dict):
            tableKeys = list(self.data.keys())
            pyTypes = [convertTypes.getType(self.data[key]) for key in tableKeys]
            pyDict = dict(zip(tableKeys,
                            pyTypes))

        elif isinstance(self.data, list):
            if isinstance(self.data[0], dict):
                data = self.data[0]
                tableKeys = list(data.keys())
                pyTypes = [convertTypes.getType(data[key]) for key in tableKeys]
                pyDict = dict(zip(tableKeys,
                                pyTypes))
        
            else:
                raise Exception("WRONG DATA TYPE")


        return pyDict



    @property
    def importRows(self):
        if isinstance(self.data, dict):return self.dictToRows()
        elif isinstance(self.data, list):
            if self.listToRowsd():
                return self.data
            else:
                raise ValueError("Input data is not list or dict")
        else:
            raise ValueError("Input data is not list or dict")





    def dictToRows(self) -> list:

        rows_ = []
        keys = list(self.data.keys())
        length_ = len(self.data[keys[0]])
        for k_ in range(length_):
            rowDict = dict()
            for key in keys:
                rowDict[key] = self.data[key][k_]
            rows_.append(rowDict)
        return rows_


    def listToRows(self) -> bool:
        keys = self.data[0].keys()
        for k_ in self.data:
            if k_.keys() == keys:
                continue
            else:return False
        return True



    def validateData(self) -> bool:
        keys = self.data.keys()
        lengths_ = []
        for key in keys:lengths_.append(len(self.data[key]))
        lengthSet = set(lengths_)
        return len(lengthSet) == 1



    def numRows(self):
        keys = self.data.keys()

        lengths_ = []
        [lengths_.append(len(self.data[key])) for key in keys if self.data[key]]
        return max(lengths_)



    def fillColumn(self,
                   key,
                   val) -> None:
        
        if self.data[key]:
            columnLen = len(self.data[key])
        else:columnLen = 0
        dataLen = self.numRows()
        for k in range(columnLen, dataLen):
            self.data[key].append(val)



