import numpy as np
class Cut:
    def __init__(self, MaxLen):
        self.MaxLen = MaxLen
        self.cutDic = self.loadDic1('.\dic\chineseDic.txt')  # 分词词典List类型
        self.frequencyDic = self.loadDic2('.\dic\WordFrequency.txt')  # 词频词典List类型

    # 读取词典chineseDic
    def loadDic1(self, dicFile):
        f = open(dicFile, 'r')
        fLine = f.readlines()
        dicList = []
        for line in fLine:
            temp = line.strip('\n').split(',',1)
            dicList.append(temp)
        return dicList

    # 读取词典WordFrequency
    def loadDic2(self, dicFile):
        f = open(dicFile, 'r')
        fLine = f.readlines()
        dicList = []
        for line in fLine:
            temp = line.strip('\n').split(',')
            dicList.append([temp[0], float(temp[2].strip('%')) * 0.01]) # 去除%，用*0.01替代
        return dicList

    # 匹配词典
    def matchDic(self, Dic, matchWord):
        matchFlag = False
        for i in range(len(Dic)):
            if matchWord == Dic[i][0]: # 这里的Dic要求是List类型
                matchFlag = True
        return matchFlag

    # 正向最大匹配法分词
    def maxMatch(self, sentence):
        cutSet = ""
        cutPoint = 0
        while cutPoint < len(sentence):
            Len = self.MaxLen
            temp = ""
            while Len > 1:
                temp = sentence[cutPoint:cutPoint + Len]
                if self.matchDic(self.cutDic, temp):
                    break
                elif Len > 1:
                    Len -= 1
            if Len == 1:
                temp = sentence[cutPoint:cutPoint + Len]
            cutSet += temp + '/'
            cutPoint += Len
        return cutSet

    # 逆向最大匹配法分词
    def reMaxMatch(self, sentence):
        cutSet = ""
        cutPoint = 0
        reSentence = sentence[::-1]
        while cutPoint < len(reSentence):
            Len = self.MaxLen
            temp = ""
            while Len > 1:
                temp = reSentence[cutPoint:cutPoint + Len][::-1]
                if self.matchDic(self.cutDic, temp):
                    break
                elif Len > 1:
                    Len -= 1
            if Len == 1:
                temp = reSentence[cutPoint:cutPoint + Len][::-1]
            cutSet = temp + '/' + cutSet
            cutPoint += Len
        return cutSet

    # 找到一句话的全部候选词（列表类型）；判断候选词是否是尾词，并返回（列表类型）
    def findCandidate(self, sentence):
        candidateSet = []
        candidateTail = []
        cutPoint = 0
        while cutPoint < len(sentence):
            Len = 1
            while Len <= self.MaxLen:
                if cutPoint + Len <= len(sentence):
                    temp = sentence[cutPoint:cutPoint + Len]
                    if self.matchDic(self.frequencyDic, temp): # self.frequencyDic是List类型
                        candidateSet.append(temp)
                        if temp[-1] == sentence[-1]:
                            candidateTail.append(temp)
                Len += 1
            cutPoint += 1
        return candidateSet, candidateTail

    # 根据词频词典，计算每个候选词的概率词，返回字典类型
    def computerP(self, candidateResult):
        pDic = {}
        tempDic = dict(self.frequencyDic)  # 为了带入computerP函数，需要将词频词典由List类型转为Dict类型
        for candidate in candidateResult:
            pDic[candidate] = tempDic[candidate]
        return pDic

    # 记录每个候选词的全部左邻词，返回字典类型
    def recordLeft(self, candidateResult, sentence):
        leftWord = []
        for candidate in candidateResult:
            leftWord.append([])
            index = sentence.find(candidate)
            if index > 0:
                canPoint = index - 1
                while canPoint >= 0:
                    temp = sentence[canPoint:index]
                    if temp in candidateResult:
                        leftWord[-1].append(temp)
                        canPoint -= 1
                    else:
                        break
        leftWordDic = dict(zip(candidateResult, leftWord))
        return leftWordDic

    # 计算每个候选词的累计概率（字典类型），记录每个候选词的最佳左邻词（字典类型），返回终点词
    def computerProductP(self, candidateResult, pDic, leftWordDic, candidateTail):
        productP = {} # 累计概率
        bestLeftWord = {} # 最佳左邻词
        endPoint = "" # 终点词
        tailP = []
        for candidate in candidateResult:
            leftWord = leftWordDic[candidate]
            leftWordSize = len(leftWord)
            if leftWordSize == 0:
                productP[candidate] = pDic[candidate]
                bestLeftWord[candidate] = "s"
            elif leftWordSize == 1:
                leftWordStr = "".join(leftWord)
                productP[candidate] = float(pDic[candidate]) * float(productP[leftWordStr])
                bestLeftWord[candidate] = leftWordStr
            else:
                leftWordArr = np.array(leftWord)
                index = np.argmax(leftWordArr)
                productP[candidate] = float(pDic[candidate]) * float(productP[leftWord[index]])
                bestLeftWord[candidate] = leftWord[index]
        for tail in candidateTail:
            tailP.append(productP[tail])
        tailPArr = np.array(tailP)
        endPoint = candidateTail[np.argmax(tailPArr)]
        return productP, bestLeftWord, endPoint

    # 最大概率分词
    def maxP(self, sentence):
        candidateResult, candidateTail = self.findCandidate(sentence)  # 找候选词（列表类型）；找尾词（列表类型）
        pDic = self.computerP(candidateResult)  # 根据词频词典，计算每个候选词的概率词，返回字典类型
        leftWordDic = self.recordLeft(candidateResult, sentence)  # 记录每个候选词的全部左邻词，返回字典类型
        productP, bestLeftWord, endPoint = self.computerProductP(candidateResult, pDic, leftWordDic,
                                                            candidateTail)  # 计算累计概率（字典类型），最佳左邻词（列表类型）,终点词
        # 自顶向下找到最优路径，得到分词结果
        maxPResult = ""
        temp = endPoint
        maxPResult = temp + '/' + maxPResult
        while 1:
            temp = bestLeftWord[temp]
            if temp == 's':
                break
            maxPResult = temp + '/' + maxPResult
        return maxPResult
