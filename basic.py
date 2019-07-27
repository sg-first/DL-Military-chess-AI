''' ************************************************************************ */
/* 己方棋子编码约定:														*/
/*	1司令,2军长,3师长,4旅长,5团长,6营长,7连长,8排长,9工兵,10地雷，11炸弹,12军旗      */
/* 对方方棋子编码约定:														*/
/*	-1司令,-2军长,-3师长,-4旅长,-5团长,-6营长,-7连长,-8排长,-9工兵,-10地雷，-11炸弹,-12军旗      */
/*	13未知对方棋子,0空棋位													*/
/* ************************************************************************ '''
cMap=[[0]*5]*12#棋盘
''' ************************************************************************ */
/* 函数功能：i,j位置是否本方棋子											*/
/* 接口参数：																*/
/*     char cMap[12][5] 棋盘局面											*/
/*     i,j 棋盘位置行列号												*/
/* 返回值：																	*/
/*     1己方棋子，0空棋位或对方棋子											*/
/* ************************************************************************ '''
def IsMyChess(i,j):
    if (cMap[i][j]>=1 and cMap[i][j] <= 12) :
        return 1
    else:
        return 0
#是否为敌方棋子
def IsEneChess(i,j):
    if cMap[i][j] == 13 or cMap[i][j] == -12:
        return 1
    else:
        return 0
'''cMap[1][1]=13
print(IsEneChess(1,1))'''
'''/* ************************************************************************ */
/* 函数功能：i, j位置是否本方可移动的棋子 * /
/* 接口参数： * /
/* char cMap[12][5] 棋盘局面 * /
/* int i, j 棋盘位置行列号 * /
/* 返回值： * /
/* 1己方可移动棋子(司令, 军长, ..., 工兵, 炸弹)，0军旗, 地雷, 对方棋子或空棋位*/
/* ************************************************************************ */'''
def IsMyMovingChess(i,j):
    if cMap[i][j]>=1 and cMap[i][j]<=9 or cMap[i][j]==11:#warning :crossline?
        return 1
    else:
        return 0
#是否为敌方可移动棋子 未翻译
'''def IsEmeMovingChess(i,j):
    if cMap[i][j]==13:
'''
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
'''/* ************************************************************************ */
/* 函数功能：i, j位置是否大本营 * /
/* 接口参数： * /
/* int i, j 棋盘位置行列号 * /
/* 返回值： * /
/* 1是大本营，0不是大本营 * /
/* ************************************************************************ */'''
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
'''/* ************************************************************************ */
/* 函数功能：i, j位置是否有棋子占位的行营 * /
/* 接口参数： * /
/* char cMap[12][5] 棋盘局面 * /
/* int i, j 棋盘位置行列号 * /
/* 返回值： * /
/* 1有棋子占位的行营, 0不是行营或是空行营 * /
/* ************************************************************************ */'''
def IsFilledCamp(i,j):
    if (IsMoveCamp(i, j) and cMap[i][j] != 0): #warn: crossline
        return 1
    else:
        return 0
'''/* ************************************************************************ */
/* 函数功能：i, j位置是否有铁路 * /
/* 接口参数： * /
/* char cMap[12][5] 棋盘局面 * /
/* int i, j 棋盘位置行列号 * /
/* 返回值： * /
/* 1有铁路, 0无铁路 * /
/* ************************************************************************ */'''
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
 #未考虑斜向路线
'''/* ************************************************************************ */
/* 函数功能：双方布局后棋局初始化（完成） * /
/* 接口参数： * /
/* char * cOutMessage 布局字符序列 * /
/* ************************************************************************ */'''
def InitMap(cOutMessage): # 这个是用之前计算好的数据处理，所以是cOutMessage
    for i in range(6):
        for j in range(5):
            if IsMoveCamp(i,j):
                cMap[i][j]=0
            else:
                cMap[i][j]=13
    k=6
    for i in range(6,12):
        for j in range(5):
            if(IsMoveCamp(i,j)):
                cMap[i][j]=0
            else:
                cMap[i][j]=cOutMessage[k+1]
def getNearPos (i,j):
    result=[]
    if (i > 0 and not (IsAfterHill(i, j))):
        result.append((i - 1, j))
 #可以左移
    if (j > 0):
        result.append((i, j-1))
 #可以右移
    if (j < 4):
        result.append((i, j+1))
 #可以后移
    if (i < 11 and not(IsBeforeHill(i, j))):
        result.append((i+1, j))
 #可以左上进行营
    if (IsMoveCamp(i - 1, j - 1)):
        result.append((i-1, j-1))
 #可以右上进行营
    if (IsMoveCamp(i - 1, j + 1)):
        result.append((i-1, j+1))
 #可以左下进行营
    if (IsMoveCamp(i + 1, j - 1)):
        result.append((i+1, j-1))
 #可以右下进行营
    if (IsMoveCamp(i + 1, j + 1)):
        result.append((i+1, j+1))
    if (IsMoveCamp(i, j)):
        result.append((i-1, j-1))
        result.append((i-1, j+1))
        result.append((i+1, j-1))
        result.append((i+1, j+1))
    return result
#print(getNearPos(1,1)) #test