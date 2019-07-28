def setDie(sub,posList):
    posList[sub] = (-1,-1)
def isDie(sub,posList):
    x,y = posList[sub]
    return x==-1 and y==-1
def codeToStrength(type):#finish
    if type==11 : # zhadan=11
        return 7 #炸弹=师长
    elif type==10: #dilei=10
        return 5 #地雷=团长
    else :
        return type
def getChessStrength(chess,node):#棋子死亡作为参数传进来？finish
    if isDie(chess,node.posList):
        return 0
    else :
        score = 0
        for i in range(len(node.probTable)):
            weight=codeToStrength(i)
            score+=weight*node.proTable(i)#?
def isDetermine(node):#finish
    type=-1
    for i in range(len(node.probTable)):
        if type==-1 and not(node.proTable ==0) :
            type=i
        if not(type==-1 ) and not(node.proTable[i]==0):
            return -1
    return type
def ChessComparisons(myc,enc,node):#finish
    mytype=codeToType(myc)
    encType=isDetermine(enc)
    #涉及工兵地雷的特判
    if(mytype==1):#if mytype==gongbing
        if encType==1 or encType == 11:#(encType == gongbing || encType == zhadan)
            return 2
        elif encType==10: #encType == dilei:
            return 1
        else : 
            return 0
    elif mytype == 10: #mytype == dilei
        if encType == 1 :#encType == gongbing
            return 0
        elif encType==11:#encType == zhadan
            return 2
        else :
            return 1
    #涉及炸弹的特判
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
    if code==1:#siling
        return 9
    if code==2:#junzhang
        return 8
    if code==3:#shizhang
        return 7
    if code==4:#lvzhang
        return 6
    if code==5:#tuanzhang
        return 5
    if code==6:#yingzhang
        return 4
    if code==7:#lianzhang
        return 3
    if code==8:#paizhang
        return 2
    if code==9:#gongbing
        return 1
    if code==10:#dilei
        return 10
    if code==11:#zhadan
        return 11
    if code==12 or code==14:
        return 0
    return -1