import eneSta
import asses
import help

def simMove(node,x1,y1,x2,y2,isEne):
    cMap = help.copy2DList(node.cMap)
    posList = help.copy2DList(node.posList)

    if(cMap[y2][x2]==0):
        if isEne:
            enemyChess=eneSta.findChess(x1,y1,posList)
            posList[enemyChess] = [y2,x2]
        cMap[y2][x2]=cMap[y1][x1]
        cMap[y1][x1]=0
        return cMap, True, posList
    else:
        if isEne==False:
            result=asses.ChessComparisons(cMap[y1][x1],eneSta.findChess(x2,y2,posList),node)
        else:
            result=asses.ChessComparisons(cMap[y2][x2],eneSta.findChess(x1,y1,posList),node)

        if result==0: # 实际的敌方胜
            if isEne:
                enemyChess=eneSta.findChess(x1,y1,posList)
                posList[enemyChess] = [y2,x2]
                cMap[y2][x2]=cMap[y1][x1]
                cMap[y1][x1]=0
            else:
                cMap[y1][x1]=0

        elif result==1: # 实际的我方胜
            if not isEne:
                enemyChess=eneSta.findChess(x2,y2,posList)
                eneSta.setDie(enemyChess,posList)
                cMap[y2][x2]=cMap[y1][x1]
                cMap[y1][x1]=0
            else: # 老位置是实际的敌方，前进失败
                enemyChess=eneSta.findChess(x1,y1,posList)
                eneSta.setDie(enemyChess,posList)
                cMap[y1][x1]=0

        elif result==2: # 对死
            if isEne:
                enemyChess=eneSta.findChess(x1,y1,posList)
            else:
                enemyChess=eneSta.findChess(x2,y2,posList)
            eneSta.setDie(enemyChess,posList)
            cMap[y2][x2]=0
            cMap[y1][x1]=0

        return cMap,False,posList