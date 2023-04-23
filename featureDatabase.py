
import os
from pathlib import Path
from sqlalchemy import Column, Integer, Table
from sqlalchemy import create_engine, MetaData, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, clear_mappers
from sqlalchemy.engine import Engine
from sqlalchemy.ext.automap import automap_base



class FeatureDatabase(object):



    class TableMapping(object):
        
        pass


    def __init__(self,
                 name,
                 directory = None):

        if not directory:
            self.location = r"sqlite:///{}.db".format(name)
            self.path = os.path.join(os.getcwd(), "{}.db".format(name))
        else:
            prefix = r"sqlite:///"
            self.path = Path(directory).joinpath("{}.db".format(name))
            self.location = "{}{}".format(prefix, self.path)

        self.engine = create_engine(self.location)
        self.metadata = MetaData(self.engine)
        self.Base = declarative_base()

    @property
    def dictOfTables(self) -> dict:

        meta_ = MetaData(self.engine)
        meta_.reflect(self.engine)
        return meta_.dictOfTables

    @property
    def mapTables(self):
        self.metadata.reflect(self.engine)
        Base = automap_base(self.metadata)
        Base.prepare()

        return Base.classes

    def doesTableExists(self,
                        tableName : str) -> bool:
        return tableName in self.dictOfTables



    def createTables(self):
        self.metadata.create_all(self.engine)


    def mapTable(self,
                 tableName,
                 columns_,
                 constrs = None):

        columns_ = self.generateColumns(columns_)

        if constrs is not None:
            table_ = Table(tableName,
                           self.metadata,
                           Column("id", Integer, primary_key=True),
                           *columns_,
                           *constrs
                           )

        else:
            table_ = Table(tableName,
                           self.metadata,
                           Column("id", Integer, primary_key=True),
                           *columns_,
                           )
        mapper(self.Template, table_)



    @staticmethod
    def generateColumns(columns_ : dict) -> list:

        columnList = []

        for colName, args in columns_.items():
            try:
                kwargs = []
                for idx in range(len(args)):
                    if type(args[idx]) is dict:
                        kwargs.append(args[idx])
                        args.pop(idx)
                col_ = Column(colName,
                              *args)

                for kwarg in kwargs:
                    keys = [*kwarg]
                    if len(keys) > 1:
                        raise Exception("Expected 1 key")
                    else:
                        key = keys[0]
                    
                    col_.__setattr__(key,
                                     kwarg[key])
                columnList.append(col_)

            except TypeError:
                columnList.append(Column(colName,
                                         args))
        return columnList


    @staticmethod
    def clearMappers():clear_mappers()



    def dropTable(self,
                  dropTable_) -> None:
        self.metadata.reflect(self.engine)
        dropTables = self.metadata.dictOfTables[dropTable_]
        dropTables.drop()
        self.metadata = MetaData(self.engine)


    def setSqlite(dbApiConnection,
                  connectRecord) -> None:
        cursor = dbApiConnection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()























































































