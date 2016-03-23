import psycopg2, re, math

def fetchData():
    conn = psycopg2.connect(database='postgres', user='postgres')
    sql = '''SELECT body, is_cyberbullying_present
  FROM bullying_data.data_tagged'''

    cur = conn.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res

def tryDictionary(useBig = True):
    data = fetchData()
    data2 = map(lambda x: [ re.findall("[\w']+", x[0]) , x[1] ] , data)
    
    data3 = list(data2)
    
    if useBig:
        for k in xrange(len(data2)):
            wordList = data2[k][0]
            cpW = list(wordList)
            if len(wordList) > 1:
                for i in xrange(len(wordList)-1):
                    bigram = wordList[i] + ' ' + wordList[i+1]
                    cpW.append(bigram)
            data3[k][0] = cpW
    
    
    wordDict = dict()
    bullyDict = dict()
    falseDict = dict()
    for x in data3:
        tWord = dict()
        tBully = dict()
        tFalse = dict()
        for word in x[0]:
            tWord[word] = 1
            if x[1] == 'Y':
                tBully[word] = 1
            else:
                tFalse[word] = 1

            """    
            if not(wordDict.has_key(word)):
                wordDict[word] = 0
            wordDict[word] = wordDict[word] + 1
            if x[1] == 'Y':
                if not(bullyDict.has_key(word)):
                    bullyDict[word] = 0
                bullyDict[word] = bullyDict[word] + 1
            else:
                if not(falseDict.has_key(word)):
                    falseDict[word] = 0
                falseDict[word] = falseDict[word] + 1
            """
        for word in tWord.keys():
            if not(wordDict.has_key(word)):
                wordDict[word] = 0
            wordDict[word] = wordDict[word] + 1

        for word in tBully.keys():
            if not(bullyDict.has_key(word)):
                bullyDict[word] = 0
            bullyDict[word] = bullyDict[word] + 1

        for word in tWord.keys():
            if not(falseDict.has_key(word)):
                falseDict[word] = 0
            falseDict[word] = falseDict[word] + 1
    return bullyDict, falseDict, wordDict, data3

def analyzeDict(useBig = True):
    bullyDict, falseDict, wordDict, data = tryDictionary(useBig)
    model = dict()
    allW = filter(lambda x : len(x[0].split(' '))==1 , bullyDict.iteritems())
    allW = map(lambda x:x[1], allW)
    
    tot = sum(allW)
    print 'Total Sum =%d'%tot
    for word,cnt in bullyDict.iteritems():
        #scoreDic[word] = float(cnt) / wordDict[word]
        #wc = 0
        #if falseDict.has_key(word):
        #    wc = falseDict[word]
        ww = word.split(' ')
        if len(ww) == 1:
            model[word] = float(cnt) / tot
        elif len(ww) == 2:
            if useBig:
                model[word] = float(cnt) / bullyDict[ww[0]]
        else:
            raise NameError('Unsupprted')
    #res = sorted(model.iteritems(), key = lambda x : -x[1])
    return data, bullyDict, wordDict, model

def scorePost(model, post, useBig = True):
    #words = re.findall("[\w']+", post[0])
    words = post
    wordsU = set(words)
    #wordsU = words
    score = 0.0
    for word in wordsU:
        ww = word.split(' ')
        if len(ww) == 2 and not(useBig):
            continue
        
        if not(model.has_key(word)) or model[word] <= 0.00001:
            score = score +  10 #TODO: penalty
        else:
            score = score +  (model[word] * -1 * math.log (model[word], 2)) 
    return score

def analyzePPM(useBig = True):
    data, bullyDict, wordDict, model = analyzeDict(useBig)
    postsScore = list()
    for post,tag in data:
        score = scorePost(model, post, useBig)
        postsScore.append([ score , tag, post ])
    postsScore = sorted(postsScore, key = lambda x: x[0] )
    return postsScore, model
        
def printROC(useBig = True):
    postsScore, model = analyzePPM(useBig)
    goodNess = 0
    falsesCnt = 0
    for i in xrange(len(postsScore)):
        tag = postsScore[i][1]
        score = postsScore[i][0]
        if tag == 'Y':
            goodNess = goodNess + 1
        else:
            falsesCnt = falsesCnt + 1
        print '%2.2f - %2.2f(%d) - %2.5f' %(100.0*float(i+1) / (len(postsScore)), (100.0 * goodNess) /  39.0 , goodNess, score)
    return postsScore, model
    

def printDict():
    scoreDic, bullyDict, wordDict = analyzeDict()
    ii = 0
    for tp in scoreDic:
        ii = ii +1
        print '%s - %2.2f (%d \ %d)'%(tp[0], 100*tp[1], bullyDict[tp[0]], wordDict[tp[0]])
        if ii == 100:
            break

postsScore, model = printROC(True)

    
