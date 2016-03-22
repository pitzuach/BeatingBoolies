import os, socket, traceback
import time, logging
from KaggleDB import KaggleDB
import csvAnalyzer
from Configuration import *

class DataLoader:
    def __init__(self):
        self.cfg = Configuration()
        self.__initLogging()
        self.__db = None
        self.__trainDataH = None
        self.__testDataH = None
        
    def __initLogging(self):
        if not(os.path.exists('log')):
            os.makedirs('log')
        serverName = socket.gethostname()
        logfmt = '%(asctime)s\t' + serverName + '\t%(levelname)s\t%(name)s\t%(threadName)s\t%(message)s'
        datef = '%d-%m-%Y %H:%M:%S'
        fname = os.path.join('log', '%s.log'%time.strftime('%d-%m-%Y', time.localtime()))
        logging.basicConfig(level=logging.INFO, format=logfmt, datefmt=datef, filename=fname)
        
    def __logFile(self, fpath):
        f = open('insert.log', 'a')
        f.write('%s\n'%fpath)
        f.close()
        
    def __getAllDone(self):
        if not(os.path.exists('insert.log')):
            return []
        f = open('insert.log', 'r')
        data = f.readlines()
        f.close()
        data = map(lambda line: line.strip(), data)
        return data

    def __tryDouble(self, raw):
        try:
            float(raw)
            return True
        except:
            return False

    def __convertToType(self, rawData, fieldType, header):
        res = None
        #print 'Format Error, Got "%s" to type "%s" of header "%s"'%(rawData, fieldType, header)
        #raise NameError('Quit')
        try:
            if fieldType == 'double':
                if rawData==None or len(rawData) == 0:
                    res = None
                else:
                    res = float(rawData)
            elif fieldType == 'int':
                if rawData==None or len(rawData) == 0:
                    res = None
                else:
                    res = int(rawData)
            elif fieldType == 'bool':
                if rawData==None or len(rawData) == 0:
                    res = None
                else:
                    res= bool(rawData)
            elif fieldType == 'string':
                if rawData==None or len(rawData) == 0:
                    res = None
                else:
                    res = rawData
            else:
                raise NameError('unknown type %s'%fieldType)
        except:
            print 'Format Error, Got "%s" to type "%s" of header "%s"'%(rawData, fieldType, header)
            traceback.print_exc()
        
        return res

    def __prepareDataType(self, folderPath, filesFormatFunc, analyzerFun):
        if not(os.path.exists(folderPath)):
            raise NameError('Path not exist')
        allFiles = self.__recursiveList(folderPath)
        allFiles = filter(lambda f : filesFormatFunc(f) , allFiles)
        if len(allFiles) == 0:
            print folderPath
            raise NameError('haven''t found training examples')
        exampleFile = allFiles[0]
        fullPath = os.path.join(folderPath, exampleFile)
        #[data, headers] = analyzerFun(fullPath, self.cfg.csv_delimeter, self.cfg.csv_transFunc, self.cfg.csv_additionalDict)
        [data, headers] = analyzerFun(fullPath)
        #if len(data) == 0:
        #    raise NameError('data file is empty')
        
        #headers = data[0].keys()
        tableTypes=  list()
        for h in headers:
            dataType = 'double'
            for rowDict in data:
                rawData = rowDict[h]
                if len(rawData) == 0:
                    continue
                if not(self.__tryDouble(rawData)):
                    dataType = 'string'
                    break
            tableTypes.append([h ,dataType])
        return tableTypes

    def initDB(self):
        self.__db = KaggleDB(self.cfg.schema_name)
        alreadyExists = self.__db.checkSchema()
        
        print 'Analyzing Train...'
        self.__trainDataH = self.__prepareDataType(self.cfg.trainDir, self.cfg.filesFormatFuncTrain, self.cfg.trainAnalyzerFun)
        print 'Analyzing Test...'
        self.__testDataH = self.__prepareDataType(self.cfg.testDir, self.cfg.filesFormatFuncTest, self.cfg.testAnalyzerFun)

        if alreadyExists:
            print 'DB Already Exists'
            return
        
        print 'Createing Schema'
        self.__db.createSchema(self.__trainDataH, self.__testDataH)
        print 'Finished!'

    def __loadData(self, fpath, dbFunc, fieldTypes, analyzeFun):
        if not(os.path.exists(fpath)):
            raise NameError('Path not exist')
        allDone = self.__getAllDone()
        if allDone.count(fpath):
            print 'Already Done!'
            return
        print 'Loading File "%s"...'%os.path.basename(fpath)
        [data, headers] = analyzeFun(fpath)
        if data == None:
            return
        print 'Inserting To DB...'
        convFunc = lambda allFields, rowDict:  map(lambda kvFieldType: self.__convertToType( rowDict[kvFieldType[0]], kvFieldType[1], kvFieldType[0] ) , fieldTypes)
        succ = dbFunc(data, convFunc)
        if succ:
            self.__logFile(fpath)
            print 'Done!'
        else:
            print 'Error, please see logs...'

    def __loadTrainData(self, fpath, fieldTypes):
        dbFunc = lambda x, transFunc: self.__db.loadData('TrainData', x, transFunc)
        self.__loadData(fpath, dbFunc, fieldTypes, self.cfg.trainAnalyzerFun)

    def __loadTestData(self, fpath, fieldTypes):
        dbFunc = lambda x, transFunc: self.__db.loadData('TestData', x, transFunc)
        self.__loadData(fpath, dbFunc, fieldTypes, self.cfg.testAnalyzerFun)

    def __recursiveList(self, fDir):
        allFiles = os.listdir(fDir)
        allFiles = map(lambda f: os.path.join(fDir, f), allFiles)
        for fullCan in allFiles:
            if os.path.isdir(fullCan):
                sonsFiles = self.__recursiveList(fullCan)
                allFiles.extend(sonsFiles)
        return allFiles

    def __loadAllData(self, fDir, filtF, func):
        if not(os.path.exists(fDir)):
            raise NameError('Path not exist')
        allFiles = self.__recursiveList(fDir)
        allFiles = filter(lambda f : filtF(f) , allFiles)
        for fil in allFiles:
            fullPath = os.path.join(fDir, fil)
            func(fullPath)

    def loadAllTrain(self):
        func = lambda x: self.__loadTrainData(x, self.__trainDataH)
        self.__loadAllData(self.cfg.trainDir , self.cfg.filesFormatFuncTrain, func)

    def loadAllTest(self):
        func = lambda x: self.__loadTestData(x, self.__testDataH)
        self.__loadAllData(self.cfg.testDir, self.cfg.filesFormatFuncTest, func)

    def close(self):
        if self.__db <> None:
            self.__db.close()
            self.__db = None

if __name__ == '__main__':
    dl = DataLoader()
    dl.initDB()

    dl.loadAllTrain()
    dl.loadAllTest()

    dl.close()

