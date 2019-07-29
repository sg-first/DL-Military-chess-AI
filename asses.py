import basic

def setDie(sub,posList): # 仅该函数对posList产生副作用
    posList[sub] = (-1,-1)

def isDie(sub,posList):
    x,y = posList[sub]
    return x==-1 and y==-1

def codeToStrength(type):
    if type==basic.zhadan:
        return basic.shizhang # 炸弹=师长
    elif type==basic.dilei:
        return basic.tuanzhang # 地雷=团长
    else :
        return type

def getChessStrength(chess,node): # 棋子死亡作为参数传进来？finish
    if isDie(chess,node.posList):
        return 0
    else:
        score = 0
        for i in range(len(node.probTable)):
            weight=codeToStrength(i)
            score+=weight*node.probTable[i]

def isDetermine(node): # finish
    type=-1
    for i in range(len(node.probTable)):
        if type==-1 and not(node.probTable[i]==0) :
            type = i
        if not(type==-1) and not(node.probTable[i]==0):
            return -1
    return type

def ChessComparisons(myc,enc,node):#finish
    mytype=codeToType(myc)
    encType=isDetermine(enc)
    # 涉及工兵地雷的特判
    if(mytype==1): # if mytype==gongbing
        if encType==1 or encType == 11:#(encType == gongbing || encType == zhadan)
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
        myStrength=codeToStrength(mytype)
        enemyStrength=getChessStrength(enc,node)
        if myStrength<enemyStrength:
            return 0
        elif myStrength > enemyStrength:
            return 1
        else :
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