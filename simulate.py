import basic
import asses
def findChess(x,y,posList):
    sub = 0
    for xi,yi in posList:
        if x==xi and y==yi:
            return sub
        else:
            sub += 1
def codeToStrength(type):
    if type==11 : # zhadan=11
        return 7 #炸弹=师长
    elif type==10: #dilei=10
        return 5 #地雷=团长
    else :
        return type
def simMove(node,x1,y1,x2,y2,isEne):
    newcMap=node.cMap[:] #新开一块棋盘做修改
    newPos= newcMap[y2][x2]
    oldPos= newcMap[y2][x2]
    if(newPos==0):
        if(isEne):
            enemyChess=findChess(x1,y1,node.posList)
            node.proTable[enemyChess]
        newPos=oldPos
        oldPos=0
        Ismove=True
        return newcMap,Ismove,node.posList
    else:
        if isEne==False:
            result=asses.ChessComparisons(oldPos,findChess(x2,y2,node.posList),node)
        else:
            result=asses.ChessComparisons(newPos,findChess(x1,y1,node.posList),node)
        if result==0:#实际的地方胜
            if isEne:
                enemyChess=findChess(x1,y1,node.posList)
                asses.setDie(enemyChess,node.proList)#e->setPos(x2, y2);
                newPos=oldPos
                oldPos=0
            else:
                oldPos=0
        elif result==1:#实际的我方胜
            if not isEne:
                enemyChess=findChess(x2,y2,node.proList)
                asses.setDie(enemyChess,node.posList)
                newPos=oldPos
                oldPos=0
            else:#老位置是实际的敌方，前进失败
                enemyChess=findChess(x1,y1,node.proList)
                asses.setDie(enemyChess,node.proList)
                oldPos=0
        elif result==2:#对死
            if isEne:
                enemyChess=findChess(x1,y1,node.posList)
            else:
                enemyChess=findChess(x2,y2,node.posList)
            asses.setDie(enemyChess,node.posList)
            newPos=0
            oldPos=0
        return newcMap,Ismove,node.posList