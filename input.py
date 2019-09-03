import train
import os

def inputMap(inmap:str, start=0, isFirst=True, splitToken='\n'):        # 读入棋盘
    inmap = inmap.split(splitToken)
    end = start + 12
    temmap = [[0 for _ in range(5)] for _ in range(12)]
    for i in range(start,end):
        if(isFirst==True):
            temmap1 = inmap[i].split()
            temmap2 = ['0' if i == '\x00' else i for i in temmap1]
            temmap2 = [int(x) for x in temmap2]
            temmap[i] = temmap2
        else:
            temmap1 = inmap[i].split()
            temmap2 = ['0' if i == '\x00' else i for i in temmap1]
            temmap2 = [int(x) for x in temmap2]
            temmap[i-1] = temmap2
    return temmap

def inputProb(inprob:str, start=0, splitToken='\n'):
    inprob = inprob.split(splitToken)
    end = start + 25
    temProb = [[0 for _ in range(12)] for _ in range(25)]
    for i in range(start, end):
        temProb1 = inprob[i].split()
        temProb1 = [float(x) for x in temProb1]
        temProb[i - 1] = temProb1
    return temProb

def inputPos(inpos:str, start=0, splitToken='\n'):
    inpos = inpos.split(splitToken)
    end = start + 25
    temPos = [[0 for _ in range(2)] for _ in range(25)]
    for i in range(start, end):
        temPos1 = inpos[i].split()
        temPos1 = [int(x) for x in temPos1]
        temPos[i - 1] = temPos1
    return temPos

def inputRounds(temRounds:str):
    temmRounds = temRounds.split()
    return int(temmRounds[0])

if __name__=='__main__':
    for root, dirs, files in os.walk(r"D:/日记"):
        for file in files:
            f = open(os.path.join(root, file), "r")
            fr = f.read()
            diary = fr.split("@")
            outdiary = [[0 for _ in range(6)] for i in range(len(diary) - 1)]
            chessMap = [[0 for _ in range(5)] for i in range(12)]
            chessProb = [[0 for _ in range(12)] for i in range(25)]
            chessPos = [[0 for _ in range(2)] for i in range(25)]
            chessOther = [0 for _ in range(10)]
            tempwinorlose = diary[len(diary) - 1].split()
            tempwinorlose = [int(x) for x in tempwinorlose]
            winorlose = bool(tempwinorlose[0])
            isfirst = True
            for i in range(len(diary) - 1):
                outdiary[i] = diary[i].split("$")  # 读入日记
                tempmap = outdiary[i][0]
                tempProb1 = outdiary[i][1]
                tempPos1 = outdiary[i][2]
                tempRounds1 = outdiary[i][4]
                tempchessNum = outdiary[i][3].split()
                tempassess = outdiary[i][5].split()
                if(isfirst==True):
                    chessMap=inputMap(tempmap,0)
                    isfirst = False
                else:
                    chessMap=inputMap(tempmap,1)
                chessProb=inputProb(tempProb1,1)
                chessPos=inputPos(tempPos1,1)
                tempRounds = inputRounds(tempRounds1)
                tempchessNum = [int(x) for x in tempchessNum]
                tempassess = [float(x) for x in tempassess]
                chessOther[0] = tempRounds
                for i in range(2):
                    chessOther[i + 1] = tempchessNum[i]
                for i in range(7):
                    chessOther[i + 3] = tempassess[i]
                train.situation(chessMap, chessProb, chessPos, chessOther, winorlose)

    print(len(train.winList))
    print(len(train.loseList))

    import value_net
    model=value_net.PolicyValueNet()
    train.train(model,1000,5000)
    train.test(model,5000)