import train
import os

for root, dirs, files in os.walk(r"E:/日记"):
    for file in files:
        f = open(os.path.join(root, file), "r")
        fr = f.read()
        diary = fr.split("@")
        outdiary = [[0 for i in range(6)] for i in range(len(diary) - 1)]
        chessMap = [[0 for i in range(5)] for i in range(12)]
        chessProb = [[0 for i in range(12)] for i in range(25)]
        chessPos = [[0 for i in range(2)] for i in range(25)]
        chessOther = [0 for i in range(10)]
        tempwinorlose = diary[len(diary) - 1].split()
        tempwinorlose = [int(x) for x in tempwinorlose]
        winorlose = bool(tempwinorlose[0])
        isfirst = False
        j = 0
        for i in range(len(diary) - 1):
            outdiary[i] = diary[i].split("$")  # 读入棋盘
            tempmap1 = outdiary[i][0].split("\n")
            tempProb1 = outdiary[i][1].split("\n")
            tempPos1 = outdiary[i][2].split("\n")
            tempRounds = outdiary[i][4].split()
            tempchessNum = outdiary[i][3].split()
            tempassess = outdiary[i][5].split()
            for i in range(12):
                if ((isfirst == False) or (j < 12)):
                    tempmap2 = tempmap1[i].split()
                    tempmap3 = ['0' if i == '\x00' else i for i in tempmap2]
                    tempmap3 = [int(x) for x in tempmap3]
                    chessMap[i] = tempmap3
                    j = j + 1
                    isfirst = True
                else:
                    tempmap2 = tempmap1[i + 1].split()
                    tempmap3 = ['0' if i == '\x00' else i for i in tempmap2]
                    tempmap3 = [int(x) for x in tempmap3]
                    chessMap[i] = tempmap3
            train.situation(chessMap, chessProb, chessPos, chessOther, winorlose)

print(len(train.winList))
print(len(train.loseList))

import value_net
model=value_net.PolicyValueNet()
train.train(model,5000,100)
