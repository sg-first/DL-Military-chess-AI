'''  
 己方棋子编码约定:														
	1司令,2军长,3师长,4旅长,5团长,6营长,7连长,8排长,9工兵,10地雷，11炸弹,12军旗      
 对方方棋子编码约定:
    14军旗 13未知对方棋子
    0空棋位
'''

# i,j位置是否本方棋子
def IsMyChess(i,j,cMap):
    if (cMap[i][j]>=1 and cMap[i][j] <= 12) :
        return 1
    else:
        return 0

# 是否为敌方棋子
def IsEneChess(i,j,cMap):
    if cMap[i][j] == 13 or cMap[i][j] == 14:
        return 1
    else:
        return 0

# i,j位置是否本方可移动的棋子
def IsMyMovingChess(i,j,cMap):
    if cMap[i][j]>=1 and cMap[i][j]<=9 or cMap[i][j]==11: # warning :crossline?
        return 1
    else:
        return 0

#是否为敌方可移动棋子 未翻译

def IsAfterHill(i,j):
    if i*5+j==31 or i*5+j==33:
        return 1
    else:
        return 0

def IsBeforeHill(i,j):
    if (i * 5 + j == 26 or i * 5 + j == 28):
        return 1
    else:
        return 0

def IsMoveCamp(i,j):
    if i * 5 + j == 11 or i * 5 + j == 13 or i * 5 + j == 17 or i * 5 + j == 21 or i * 5 + j == 23 or i * 5 + j == 36 or i * 5 + j == 38 or i * 5 + j == 42 or i * 5 + j == 46 or i * 5 + j == 48:
        return 1
    else:
        return 0

def IsMyMoveCamp(i,j):
    if i * 5 + j == 36 or i * 5 + j == 38 or i * 5 + j == 42 or i * 5 + j == 46 or i * 5 + j == 48:
        return 1
    else:
        return 0

def IsEnemyMoveCamp(i, j):
    if i * 5 + j == 11 or i * 5 + j == 13 or i * 5 + j == 17 or i * 5 + j == 21 or i * 5 + j == 23 :
        return 1
    else:
        return 0

# i,j位置是否大本营
def IsBaseCamp(i,j):
    if (i * 5 + j == 1 or i * 5 + j == 3 or i * 5 + j == 56 or i * 5 + j == 58):
        return 1
    else:
        return 0

def IsMyBaseCamp(i, j):
    if (i * 5 + j == 56 or i * 5 + j == 58):
        return 1
    else:
        return 0

def IsEnemyBaseCamp(i,j):
    if (i * 5 + j == 1 or i * 5 + j == 3):
        return 1
    else:
        return 0

# i,j位置是否有棋子占位的行营
def IsFilledCamp(i,j,cMap):
    if (IsMoveCamp(i, j) and cMap[i][j] != 0): # warn: crossline
        return 1
    else:
        return 0

# i,j位置是否有铁路
def IsAcrossRailway(i):
    if (i == 1 or i == 5 or i == 6 or i == 10):
        return 1
    else:
        return 0
def IsVerticalRailway(i, j):
    if ((j == 0 or j == 4)and (i > 0 and i < 11)):
        return 1
    else:
        return 0
def IsEngineerRailway(i,j):
    if (j == 2 and (i == 5 or i == 6)):
        return 1
    else:
        return 0
def shortestpathtojunqi(i,j):
        return abs(11 - i) + abs(3 - j)
# 未考虑斜向路线

def getNearPos(i,j):
    result=[]
    if (i > 0 and not (IsAfterHill(i, j))):
        result.append((i - 1, j))
    # 可以左移
    if (j > 0):
        result.append((i, j-1))
    # 可以右移
    if (j < 4):
        result.append((i, j+1))
    # 可以后移
    if (i < 11 and not(IsBeforeHill(i, j))):
        result.append((i+1, j))
    # 可以左上进行营
    if (IsMoveCamp(i - 1, j - 1)):
        result.append((i-1, j-1))
    # 可以右上进行营
    if (IsMoveCamp(i - 1, j + 1)):
        result.append((i-1, j+1))
    # 可以左下进行营
    if (IsMoveCamp(i + 1, j - 1)):
        result.append((i+1, j-1))
    # 可以右下进行营
    if (IsMoveCamp(i + 1, j + 1)):
        result.append((i+1, j+1))
    if (IsMoveCamp(i, j)):
        result.append((i-1, j-1))
        result.append((i-1, j+1))
        result.append((i+1, j-1))
        result.append((i+1, j+1))
    return result

def getAccessibility(i,j,isEne):
    result = []
    if isEne:
        isMovingChess = IsEmeMovingChess # fix:这个函数没翻译，还要翻译
        isChess = IsEneChess
        isInvChess = IsMyChess
    else:
        isMovingChess = IsMyMovingChess
        isChess = IsMyChess
        isInvChess = IsEneChess

    # fix:后面翻译扩展部分


# 概率表棋子对应下标
siling = 9
junzhang = 8
shizhang = 7
lvzhang = 6
tuanzhang = 5
yingzhang = 4
lianzhang = 3
paizhang = 2
gongbing = 1
junqi = 0
dilei = 10
zhadan = 11

def findJunqi(probTable):
    for i in range(12):
        nowList = probTable[i]
        if not nowList[junqi] > 0.5: # 军棋位非0
            isFind = True
            for j in range(1,12):
                if nowList[j] > 0.5: # 只允许一个非0
                    isFind = False
                    break
            if isFind:
                return i
    return -1

usBeatHand = None # 我方上次吃子手数
eneBeatHand = None # 敌方上次吃子手数
handNum = None # 目前手数
_maxMoveNum = 31 # 最大不吃子次数

def game_end(node):
    findEneJunqi = False
    findEne = False
    findUs = False
    findUsJunqi = False

    for i in range(12):
        for j in range(5):
            if node.cMap[i][j]==14:
                findEneJunqi = True
            if IsEneChess(i,j,node.cMap):
                findEne = True
            if node.cMap[i][j]==12:
                findUsJunqi = True
            if IsMyChess(i,j,node.cMap):
                findUs = True

    if not findUsJunqi: # 未找到我方军棋，我方输
        return True,False
    if not findUs: # 未找到我方棋子，我方输
        return True,False
    if not findEne: # 未找到敌方棋子，敌方输
        return True,True
    if (not findEneJunqi) and node.probTable[junqi]==1: # 归一化之后为1，已经确定敌方军棋
        return True,True # 未找到敌方军棋，敌方输

    handNum_i = handNum + node.layer # 目前总手数
    moveNum = handNum_i - max(eneBeatHand, usBeatHand) # 目前已有多少步未吃子
    if moveNum < _maxMoveNum: # 不满足磨棋的先决条件
        return False,None
    else:
        maxMoveNum = moveNum - _maxMoveNum  # 剩余最大不吃子次数
        count = 0
        node_i = node
        isMoqi = False
        while(1):
            if node_i.move is None: # 确定不是第二层（最大只能到第二层）
                break
            else:
                _,_,isMove = node_i.move
                # 看本手是否吃子，调整计数
                if isMove: # 没有吃子
                    count += 1
                else:
                    break # 吃子了，未磨棋
                # 到达指定步数未吃子，确定磨棋
                if count == maxMoveNum:
                    isMoqi = True
                    break
                # 看上一手
                node_i = node_i.parent # 前面已经确定不是第二层，这里不用判断了

        if not isMoqi:
            return False,None
        else: # 确认磨棋胜方
            while(1):
                node_i = node_i.parent # 看上一手
                if node_i.move is None:  # 确定不是第二层（最大只能到第二层）
                    break
                else:
                    _, _, isMove = node_i.move
                    if not isMove: # 吃子了
                        return False,node_i.isEne # 吃子是它的父节点走的，所以是isEne，相当于not not isEne
            # 上次吃子不在模拟里
            if eneBeatHand > usBeatHand:  # 大的后吃子，胜出
                return True, False
            else:
                return True, True
