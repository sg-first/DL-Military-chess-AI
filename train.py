import numpy as np
import random

winList = []
loseList = []

class situation:
    def __init__(self, board:list, probMap:list, otherFeature:list, isWin:bool):
        self.board=np.array(board)
        for i in range(12):
            probMap[i].append(otherFeature[i][0])
            probMap[i].append(otherFeature[i][1])
        self.probMap=np.array(probMap)
        self.otherFeature=np.array(otherFeature)

        if isWin:
            winList.append(self)
        else:
            loseList.append(self)


def train(modelObj, epoch:int, batch_size:int, learning_rate):
    for i in range(epoch):
        allBoard = []
        allProbMap = []
        allOtherFeature = []
        allIsWin = []

        isWin = True
        for j in range(batch_size):
            sample = None
            if isWin:
                sample = random.choice(winList)
            else:
                sample = random.choice(loseList)

            allBoard.append(sample.board)
            allProbMap.append(sample.probMap)
            allOtherFeature.append(sample.otherFeature)
            allIsWin.append(int(isWin))
            isWin = not isWin

        allBoard = np.array(allBoard)
        allProbMap = np.array(allProbMap)
        allOtherFeature = np.array(allOtherFeature)
        allIsWin = np.array(allIsWin)
        modelObj.train_step(allBoard, allProbMap, allOtherFeature, allIsWin, learning_rate)