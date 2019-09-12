import numpy as np
import random

trainNum = 0
winList = []
loseList = []

def makeCompleteProbMap(probMap,posList):
    for i in range(25):
        probMap[i].append(posList[i][0]) # 会改变原来的probMap
        probMap[i].append(posList[i][1])
    return probMap

class situation:
    def __init__(self, board:list, probMap:list, posList:list, otherFeature:list, isWin:bool):
        self.board = np.array(board)
        self.probMap = np.array(makeCompleteProbMap(probMap,posList))
        self.probMap = self.probMap.T
        self.otherFeature = np.array(otherFeature)

        if isWin:
            winList.append(self)
        else:
            loseList.append(self)


def train(modelObj, epoch:int, batch_size:int, totEpoch:int):
    for _ in range(totEpoch):
        random.shuffle(winList)
        random.shuffle(loseList)
        total_size=min(len(winList),len(loseList))

        allBoard = []
        allProbMap = []
        allOtherFeature = []
        allIsWin = []

        def add(sample, isWin):
            allBoard.append([sample.board])
            allProbMap.append([sample.probMap])
            allOtherFeature.append(sample.otherFeature)
            allIsWin.append(isWin)

        for i in range(total_size):
            add(winList[i], 1)
            add(loseList[i], 0)

        allBoard = np.array(allBoard)
        allProbMap = np.array(allProbMap)
        allOtherFeature = np.array(allOtherFeature)
        allIsWin = np.array(allIsWin)
        modelObj.train(allBoard, allProbMap, allOtherFeature, allIsWin, epoch, batch_size)

        global trainNum
        modelObj.save_model('model'+str(trainNum)+'.pkl')
        trainNum += 1

def test(modelObj, batch_size:int):
    allBoard = []
    allProbMap = []
    allOtherFeature = []
    allIsWin = []

    isWin = True
    for j in range(batch_size):
        if isWin:
            sample = random.choice(winList)
        else:
            sample = random.choice(loseList)

        allBoard.append([sample.board])
        allProbMap.append([sample.probMap])
        allOtherFeature.append(sample.otherFeature)
        allIsWin.append(int(isWin))
        isWin = not isWin

    allBoard = np.array(allBoard)
    allProbMap = np.array(allProbMap)
    allOtherFeature = np.array(allOtherFeature)
    allIsWin = np.array(allIsWin)

    pos,neg=modelObj.test(allBoard,allProbMap,allOtherFeature,allIsWin)
    print(pos, '/', batch_size / 2)
    print(neg, '/', batch_size / 2)