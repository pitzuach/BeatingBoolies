import re, sys, os

def analyzeCsv(csvContent, delimiter = ',', manipulationFunc = None, additionalConstFields = None):
    if manipulationFunc <> None and type(manipulationFunc) <> dict:
        raise NameError('passed manipulationFunc which should be dict object')
    if additionalConstFields <> None and type(manipulationFunc) <> dict:
        raise NameError('passed additionalConstFields which should be dict object')
    res = list()
    
    allLines = csvContent.splitlines()
    allLines = filter(lambda x: len(x.strip()) > 0, allLines)
    header = allLines[0]
    header = map(lambda x: x.strip().strip('"').lower() ,header.split(delimiter))
    
    fieldCnt = len(header)
    tokenSpliter = re.compile(delimiter)
    allLines = allLines[1:len(allLines)]    
    
    for line in allLines:
        allTokens = tokenSpliter.split(line)
        allTokens = map(lambda t: t.strip().strip('"') ,allTokens)
        d = dict()
        if len(allTokens) <> fieldCnt:
            sys.stderr.write('%s\n'%line)
            raise NameError('Csv Format Exception')
        for i in xrange(0, fieldCnt):
            if len(header[i]) == 0:
                continue
            if manipulationFunc <> None and manipulationFunc.has_key(header[i]):
                handleFunc = manipulationFunc[header[i]]
                d[header[i]] = handleFunc(allTokens[i])
            else:
                d[header[i]] = allTokens[i]
        if additionalConstFields <> None:
            for exF, exV in additionalConstFields.iteritems():
                d[exF] = exV
        res.append(d)
        
    header = filter(lambda x: len(x) > 0 ,header)    
    return res, header
def analyzeFile(fpath, delimiter = ',', manipulationFunc = None, additionalConstFields = None):
    if not(os.path.exists(fpath)):
        raise NameError('Path not exist')
    f = open(fpath, 'r')
    data = f.read()
    f.close()
    return analyzeCsv(data, delimiter, manipulationFunc, additionalConstFields)
