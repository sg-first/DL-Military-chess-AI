import train
import os
import inputHelp

if __name__=='__main__':
    for root, dirs, files in os.walk(r"D:/日记"):
        for file in files:
            filePath=os.path.join(root, file)
            f = open(filePath, "r")
            print(filePath)
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
                    chessMap=inputHelp.inputMap(tempmap,0,isfirst)
                    isfirst = False
                else:
                    chessMap=inputHelp.inputMap(tempmap,1,isfirst)
                chessProb = inputHelp.inputProb(tempProb1, 1)
                chessPos = inputHelp.inputPos(tempPos1, 1)
                tempRounds = inputHelp.inputRounds(tempRounds1)
                tempchessNum = [int(x) for x in tempchessNum]
                tempassess = [float(x) for x in tempassess]
                chessOther[0] = tempRounds
                for i in range(2):
                    chessOther[i + 1] = tempchessNum[i]
                for i in range(7):
                    chessOther[i + 3] = tempassess[i]
                train.situation(chessMap, chessProb, chessPos, chessOther, winorlose, filePath)

    winNum=len(train.winList)
    loseNum=len(train.loseList)
    print(winNum)
    print(loseNum)

    import value_net
    model=value_net.PolicyValueNet()
    batch_size = winNum*2
    totEpoch = int((winNum+loseNum)/batch_size)
    train.train(model, epoch=2000, batch_size=batch_size, totEpoch=totEpoch)
    train.test(model,1200) # fix:为了好数，建议设置为winNum*2取整百

    model.save_model('model0.pkl')