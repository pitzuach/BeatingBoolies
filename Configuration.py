import csvAnalyzer, xmlAnalyzer

class Configuration:
    def __init__(self):
        self.schema_name = 'BULLYING_DATA'
        self.dataDir = 'C:\\Users\\User\\Downloads\\BayzickBullyingData\\Posts'
        self.tableName = 'RawData'
        self.filesFormatFunc = lambda f : f.endswith('.xml')
        self.dataAnalyzerFun = xmlAnalyzer.parseXml
        
        #self.dataDir = 'C:\\Users\\User\\Downloads\\BayzickBullyingData\\Human Concensus'
        #self.tableName = 'LabelData'
        #self.filesFormatFunc = lambda f : f.endswith('.csv')
        #self.dataAnalyzerFun = lambda f:  csvAnalyzer.analyzeFile(f, delimiter = ',', manipulationFunc = None, additionalConstFields = None)
        
        
