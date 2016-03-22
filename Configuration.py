import csvAnalyzer, xmlAnalyzer

class Configuration:
    def __init__(self):
        self.schema_name = 'BULLYING_DATA'
        self.trainDir = 'C:\\Users\\User\\Downloads\\BayzickBullyingData\\Posts'
        self.testDir = 'C:\\Users\\User\\Downloads\\BayzickBullyingData\\Human Concensus'
        self.csv_delimeter = ','
        self.csv_transFunc = None
        self.csv_additionalDict = None
        self.filesFormatFuncTrain = lambda f : f.endswith('.xml')
        self.filesFormatFuncTest = lambda f : f.endswith('.csv')
        self.trainAnalyzerFun = xmlAnalyzer.parseXml
        self.testAnalyzerFun = lambda f:  csvAnalyzer.analyzeFile(f, self.csv_delimeter, self.csv_transFunc, self.csv_additionalDict)
        
        
