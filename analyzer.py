import psycopg2, re, math, random

class Analyzer:
    def __init__(self, penaltyTh=1.0, useBigram = False):
       self.data = None
       self.curr_data = None
       self.test_data = None
       self.useBigram = useBigram
       self.penaltyTh = penaltyTh

    def prepareData(self, perc = 0.7):
        if self.data == None:
            self.fetchData()
        self.curr_data = list(self.data)
        random.shuffle(self.curr_data)

        good_cl = filter(lambda p: p[1] == 'Y' , self.curr_data)
        bad_cl = filter(lambda p: p[1] == 'N' , self.curr_data) 
        train_data = good_cl[0: int( math.ceil(len(good_cl) * perc))]
        train_data.extend( bad_cl[0: int( math.ceil(len(bad_cl) * perc))] )
        self.test_data = good_cl[int( math.ceil(len(good_cl) * perc)):]
        self.test_data.extend( bad_cl[int( math.ceil(len(bad_cl) * perc)):] )
        self.curr_data = train_data
       
    def fetchData(self):
        if self.curr_data <> None:
            return self.curr_data
        if self.data <> None:
            return self.data
        conn = psycopg2.connect(database='postgres', user='postgres')
        sql = '''SELECT body, is_cyberbullying_present
      FROM bullying_data.data_tagged'''

        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        conn.close()
        self.data = res
        return res

    def tryDictionary(self):
        data = self.fetchData()
        data2 = map(lambda x: [ re.findall("[\w']+", x[0]) , x[1] ] , data)
        
        data3 = list(data2)
        
        if self.useBigram:
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

    def analyzeDict(self):
        bullyDict, falseDict, wordDict, data = self.tryDictionary()
        model = dict()
        allW = filter(lambda x : len(x[0].split(' '))==1 , bullyDict.iteritems())
        allW = map(lambda x:x[1], allW)
        
        tot = sum(allW)
        #print 'Total Sum =%d'%tot
        for word,cnt in bullyDict.iteritems():
            #scoreDic[word] = float(cnt) / wordDict[word]
            #wc = 0
            #if falseDict.has_key(word):
            #    wc = falseDict[word]
            ww = word.split(' ')
            if len(ww) == 1:
                model[word] = float(cnt) / tot
            elif len(ww) == 2:
                if self.useBigram:
                    model[word] = float(cnt) / bullyDict[ww[0]]
            else:
                raise NameError('Unsupprted')
        #res = sorted(model.iteritems(), key = lambda x : -x[1])
        return data, bullyDict, wordDict, model

    def scorePost(self, model, post):
        #words = re.findall("[\w']+", post[0])
        words = post
        wordsU = set(words)
        #wordsU = words
        score = 0.0
        for word in wordsU:
            ww = word.split(' ')
            if len(ww) == 2 and not(self.useBigram):
                continue
            
            if not(model.has_key(word)) or model[word] <= 0.00001:
                score = score +  self.penaltyTh
            else:
                score = score +  (model[word] * -1 * math.log (model[word], 2)) 
        return score

    def analyzePPM(self):
        data, bullyDict, wordDict, model = self.analyzeDict()
        postsScore = list()
        if self.test_data <> None:
            data = self.test_data
        for post,tag in data:
            score = self.scorePost(model, post)
            postsScore.append([ score , tag, post ])
        postsScore = sorted(postsScore, key = lambda x: x[0] )
        return postsScore, model
            
    def printROC(self):
        postsScore, model = self.analyzePPM()
        goodNess = 0
        falsesCnt = 0
        tot_good = len( filter(lambda p: p[1] == 'Y' , postsScore) )
        for i in xrange(len(postsScore)):
            tag = postsScore[i][1]
            score = postsScore[i][0]
            if tag == 'Y':
                goodNess = goodNess + 1
            else:
                falsesCnt = falsesCnt + 1
            print 'Progress=%2.2f, found=%2.2f(%d), MAP=%2.2f - %2.5f' %(100.0*float(i+1) / (len(postsScore)), \
                                                                         (100.0 * goodNess) /  float(tot_good) , goodNess, 100.0 * goodNess / float(goodNess + falsesCnt) ,score)
        return postsScore, model

    def getResultsCrossedVal(self, perc = 0.7, numCross = 50, retVal = None):
        pScores = list()
        tot_good = None
        pSize = None
        for i in xrange(numCross):
            self.prepareData(perc)
            postsScore, model = self.analyzePPM()
            pScores.append(postsScore)
            if tot_good == None:
                tot_good = len( filter(lambda p: p[1] == 'Y' , postsScore) )
                pSize = len(postsScore)

        goodNessA = [0 for i in xrange(numCross)]
        falsesCntA = [0 for i in xrange(numCross)]
        scoresA = [0 for i in xrange(numCross)]
        res = 0.0
        for i in xrange(pSize):
            for k in xrange(numCross):
                postsScore = pScores[k]
                tag = postsScore[i][1]
                score = postsScore[i][0]
                scoresA[k] = score
                if tag == 'Y':
                    goodNessA[k] = goodNessA[k] + 1
                else:
                    falsesCntA[k] = falsesCntA[k] + 1

            tmp = sorted(goodNessA)
            goodNess = tmp[int(len(tmp)/2)]
            #falsesCnt = sum(falsesCntA) / float(numCross)
            tmp = sorted(falsesCntA)
            falsesCnt = tmp[int(len(tmp)/2)]
            tmp = sorted(scoresA)
            #score = sum(scoresA) / float(numCross)
            score =  tmp[int(len(tmp)/2)]
            if retVal <> None and i == retVal:
                res = goodNess
            if retVal == None:
                print 'Progress=%2.2f, found=%2.2f(%d), MAP=%2.2f - %2.5f' %(100.0*float(i+1) / pSize, \
                    (100.0 * goodNess) /  float(tot_good) , goodNess, 100.0 * goodNess / float(goodNess + falsesCnt) ,score)
        return res


    def printDict(self):
        scoreDic, bullyDict, wordDict = self.analyzeDict()
        ii = 0
        for tp in scoreDic:
            ii = ii +1
            print '%s - %2.2f (%d \ %d)'%(tp[0], 100*tp[1], bullyDict[tp[0]], wordDict[tp[0]])
            if ii == 100:
                break


a = Analyzer(penaltyTh = 0.1,useBigram = False)
#postsScore, model = a.printROC()

mm = None
mind = None
for p in xrange(50):
    a.penaltyTh = p/100.0
    
    res = a.getResultsCrossedVal(perc = 0.8, numCross = 10, retVal = 3)
    #res = a.getResultsCrossedVal(perc = 0.8, numCross = 10, retVal = None)
    if mm == None or res > mm:
        mm = res
        mind = a.penaltyTh
    print 'Running On %2.2f, Got %d'%(a.penaltyTh, res)

print 'Best For %2.2f With %d'%(mind, mm)
