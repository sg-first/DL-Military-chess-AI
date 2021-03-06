import basic
import eneSta

eneMax=0

def codeToStrength(type):
    if type==basic.zhadan:
        return basic.shizhang # 炸弹=师长
    elif type==basic.dilei:
        return basic.tuanzhang # 地雷=团长
    else :
        return type

def codeToStrength2(type):#19.8.5 update
    if (type == basic.junqi):
        return 12   #军棋子力值应为0，在大本营的棋子-12
    if (type == basic.zhadan or type == basic.shizhang):
        return 22
    if (type == basic.tuanzhang or type == basic.dilei):
        return 18
    if (type == basic.gongbing):
        return 10
    if (type == basic.paizhang):
        return 12
    if (type == basic.lianzhang):
        return 14
    if (type == basic.yingzhang):
        return 16
    if (type == basic.lvzhang):
        return 20
    if (type == basic.junzhang):
        return 24
    if (type == basic.siling):
        return 30

def getChessStrength(chess,node):
    if eneSta.isDie(chess,node.posList):
        return 0
    else:
        score = 0
        for i in range(len(node.probTable[chess])):
            weight=codeToStrength(i)
            score+=weight*node.probTable[chess][i]
        return score/sum(node.probTable[chess])

def isDetermine(node, chess):
    type=-1
    for i in range(len(node.probTable[chess])):
        if type==-1 and not(node.probTable[chess][i]==0) :
            type = i
        if not(type==-1) and not(node.probTable[chess][i]==0):
            return -1
    return type

def ChessComparisons(myc,enc,node):#finish
    mytype=codeToType(myc)
    encType=isDetermine(node, enc)
    # 涉及工兵地雷的特判
    if(mytype==1): # if mytype==gongbing
        if encType==1 or encType == 11:#(encType == gongbing or encType == zhadan)
            return 2
        elif encType==10: #encType == dilei:
            return 1
        else : 
            return 0
    elif mytype == 10: # mytype == dilei
        if encType == 1 :# encType == gongbing
            return 0
        elif encType==11:# encType == zhadan
            return 2
        else :
            return 1
    # 涉及炸弹的特判
    if mytype==11 or encType==11:
        return 2
    else:
        myStrength = codeToStrength(mytype)
        enemyStrength = getChessStrength(enc, node)
        if myStrength < enemyStrength:
            return 0
        elif myStrength > enemyStrength:
            return 1
        else:
            return 2

def codeToType(code):#finish
    if code==1:
        return basic.siling
    if code==2:
        return basic.junzhang
    if code==3:
        return basic.shizhang
    if code==4:
        return basic.lvzhang
    if code==5:
        return basic.tuanzhang
    if code==6:
        return basic.yingzhang
    if code==7:
        return basic.lianzhang
    if code==8:
        return basic.paizhang
    if code==9:
        return basic.gongbing
    if code==10:
        return basic.dilei
    if code==11:
        return basic.zhadan
    if code==12 or code==14:
        return basic.junqi
    return -1

def valueLocation(i,j):
    if(basic.IsAcrossRailway(i) or basic.IsVerticalRailway(i, j)):
        return 5
    elif (basic.IsBaseCamp(i, j)):
        return -12
    elif basic.IsMyMoveCamp(i, j):
        return 8
    elif basic.IsEnemyMoveCamp(i, j):
        return 10
    else:
        return 4

def valueMotivation(type):
    if not(type==basic.gongbing):
        return codeToStrength2(type)/4
    else:
        return codeToStrength2(type)/9

def shortestpathtojunqi(i,j,cMap):
    if (getselfjunqi(cMap)):
        return abs(11-i)+abs(3-j)
    else:
        return abs(11-i)+abs(1-j)

def valuelast3line(i,j,cMap):
    if i>8 and cMap[i][j] != 12:
        return 15/shortestpathtojunqi(i, j,cMap)
    else:
        return 0
def getselfjunqi(cmap):
    if(cmap[11][3]==12):
        return 1
    else:
        return 0

def valuecrosshill(i):
    if i<=5 and i>=3:
        return 55*(6-i)-eneMax
    elif i<3:
        return 70*(6-i)-eneMax
    else:
         return 0

def valueNear(i,j,node):
    allPos=basic.getNearPos(i,j)
    global eneMax
    eneMax=0
    friMax=0
    for p in allPos:
        i2, j2 = p
        if not node.cMap[i2][j2] == 0:
            if node.cMap[i2][j2] == 13:
                s = getChessStrength(eneSta.findChess(j2, i2, node.posList), node)
                if s > eneMax:
                    eneMax = s
            else:
                s = codeToStrength2(codeToType(node.cMap[i2][j2]))
                if s > friMax:
                    friMax = s
    value=0
    myStrength=codeToStrength2(codeToType(node.cMap[i][j]))
    if(eneMax>=myStrength):
        value=-eneMax
    if(friMax>myStrength):
        value+=friMax/2
    return value

def valueEstimation(node):
    ff1=ff2=ff3=ff4=ff5=ff6=ff7=0
    for i in range(12):
        for j in range(5):
            if basic.IsMyChess(i,j,node.cMap):
                type=codeToType(node.cMap[i][j])
                junqi = basic.findJunqi(node.probTable)
                if (not(junqi == -1)) and eneSta.isDie(junqi,node.posList):
                    ff7+=1000
                ff1 += codeToStrength2(type)
                ff2 += valueLocation(i, j)
                ff3 += valueMotivation(type)
                ff4 += valuelast3line(i, j,node.cMap)
                ff5 += valueNear(i, j,node)
                ff6 += valuecrosshill(i)
    return (ff1,ff2,ff3,ff4,ff5,ff6,ff7)
