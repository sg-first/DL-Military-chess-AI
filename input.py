import train
import os

for root, dirs, files in os.walk(r"E:/特种兵的一整本日记(第二本2)"):
    for file in files:
        f = open(os.path.join(root, file), "r")
        fr = f.read()
        diary = fr.split("@")
        outdiary = [[0 for i in range(6)] for i in range(len(diary) - 1)]
        chessMap = [[0 for i in range(5)] for i in range(12)]
        chessProb = [[0 for i in range(12)] for i in range(25)]
        chessPos = [[0 for i in range(2)] for i in range(25)]
        chessOther = [0 for i in range(10)]
        winorlose = bool(diary[len(diary) - 1])
        for i in range(len(diary) - 1):
            outdiary[i] = diary[i].split("$")  # 读入棋盘
            tempmap1 = outdiary[i][0].split("\n")
            tempProb1 = outdiary[i][1].split("\n")
            tempPos1 = outdiary[i][2].split("\n")
            tempRounds = outdiary[i][4].split()
            tempchessNum = outdiary[i][3].split()
            tempassess = outdiary[i][5].split()
            for i in range(12):
                tempmap2 = tempmap1[i].split()
                tempmap3 = ['0' if i == '\x00' else i for i in tempmap2]
                tempmap3 = [int(x) for x in tempmap3]
                chessMap[i] = tempmap3  # 输出正确  可直接调用类函数
            for i in range(1, 26):
                tempProb2 = tempProb1[i].split()
                tempProb2 = [float(x) for x in tempProb2]
                chessProb[i - 1] = tempProb2  # 输出问题已解决
            for i in range(1, 26):
                tempPos2 = tempPos1[i].split()
                tempPos2 = [int(x) for x in tempPos2]
                chessPos[i - 1] = tempPos2
            tempRounds = [int(x) for x in tempRounds]
            tempchessNum = [int(x) for x in tempchessNum]
            tempassess = [float(x) for x in tempassess]
            chessOther[0] = tempRounds[0]
            for i in range(2):
                chessOther[i + 1] = tempchessNum[i]
            for i in range(7):
                chessOther[i + 3] = tempassess[i]
            train.situation(chessMap, chessProb, chessPos, chessOther, winorlose)
