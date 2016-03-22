import psycopg2, traceback, logging

class KaggleDB:

    def __init__(self, schema_name,  maxErrorToRest = 3):
        self.__conn = psycopg2.connect(database='postgres', user='postgres')
        self.__errorCount = 0
        self.__maxError = maxErrorToRest
        self.__logger = logging.getLogger(__name__)
        self.schema_name = schema_name

    def close(self):
        self.__conn.close()

    def __handleError(self):
        self.__logger.error(traceback.format_exc())
        traceback.print_exc()
        self.__errorCount = self.__errorCount + 1
        if (self.__errorCount >= self.__maxError):
            self.__errorCount = 0
            try:
                self.__conn.close()
            except:
                err = traceback.format_exc()
                self.__logger.error(err)
                print err
            self.__conn = psycopg2.connect(database='postgres', user='postgres') 

    def exeS(self, sql, hasRes = True):
        res = None
        if hasRes:
            res = self.__executeSql(sql, hasRes)
        else:
            self.__executeSql(sql, hasRes)
        return res
            
    def __executeSql(self, sql, hasRes = True):
        res = None
        try:
            self.__cur = self.__conn.cursor()
            self.__cur.execute(sql)
            if hasRes:
                res = self.__cur.fetchall()
            else:
                self.__conn.commit()
            self.__cur.close()
        except:
            print 'Query Was: %s'%sql
            self.__handleError()
        return res

    def checkSchema(self):
        existsSql = """ select count(*) from information_schema.schemata where schema_name = '%s' """%self.schema_name.lower()
        res = self.__executeSql(existsSql)
        return res[0][0]

    def __createTable(self, tableName, tblF):
        sqlRaw = 'SELECT '
        for kv in tblF:
            fName = kv[0].replace(' ', '_').replace('?','')
            fType = kv[1]
            if fType == 'int':
                sqlRaw = sqlRaw + '12345' + ' AS ' + fName + ' ,'
            elif fType == 'double':
                sqlRaw = sqlRaw + '12345.01' + ' AS ' + fName + ' ,'
            elif fType == 'bool':
                sqlRaw = sqlRaw + 'true' + ' AS ' + fName + ' ,'
            elif fType == 'string':
                sqlRaw = sqlRaw + "'" + 'A' * 500 + "'::text" + ' AS ' + fName + ' ,'
            else:
                raise NameError('Unrecognize Type %s'%fType)
        sqlRaw = sqlRaw[0:-1]
        sqlRaw = sqlRaw + ' WHERE 1=0'

        self.__executeSql(""" 
        CREATE TABLE %s.%s as 
        %s
        """%(self.schema_name, tableName , sqlRaw), False)
            
    def createSchema(self, trainTbl, testTbl):
        existsSql = """ select count(*) from information_schema.schemata where schema_name = '%s' """%self.schema_name.lower()
        res = self.__executeSql(existsSql)
        if res[0][0] == 1:
            return

        print 'Creating Schema'
        self.__executeSql(""" 
        CREATE SCHEMA %s
        """%self.schema_name, False)
        
        self.__createTable('TrainData', trainTbl)
        self.__createTable('TestData', testTbl)
        
    def getTableFields(self, tbl_name = 'eeg_subjects'): 
        fields = list()
        if (self.__conn == None):
            raise NameError('Connection already closed')
        try:
            self.__cur = self.__conn.cursor()   
            self.__cur.execute(""" SELECT  column_name 
FROM information_schema.columns where table_schema = %s
and table_name = %s 
order by ordinal_position
""", [self.schema_name.lower() ,tbl_name.lower()])    
            rowsTemp = self.__cur.fetchall()
            #print len(rowsTemp)
            self.__cur.close()
            rowsData = map(lambda row: row[0], rowsTemp)
            for r in rowsData:
                fields.append(r)
                
        except:
            self.__handleError()

        return fields


    
    def loadData(self, table_name, data, transFunction = None):
        tblFields = self.getTableFields(table_name)
        if transFunction <> None:
            allRows = map(lambda x: transFunction(tblFields, x), data)
        else:
            allRows = map( lambda rowDict: map(lambda h: rowDict[h] , tblFields) ,data)
        flCnt = len(tblFields)
        sHeader = '%s,' * flCnt 
        sHeader = sHeader[0:-1]
        if (self.__conn == None):
            raise NameError('Connection already closed')
        try:
            self.__cur = self.__conn.cursor()
            self.__cur.executemany("""insert into %s.%s values(%s)
                                ;"""%( self.schema_name ,table_name ,sHeader),
                               allRows)
            self.__cur.close()
            self.__conn.commit()
            return True
        except:
            #traceback.print_exc()
            self.__handleError()
            return False
