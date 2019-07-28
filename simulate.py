def findChess(x,y,posList):
    sub = 0
    for xi,yi in posList:
        if x==xi and y==yi:
            return sub
        else:
            sub += 1

def setDie(sub,posList):
    posList[sub] = (-1,-1)

def isDie(sub,posList):
    x,y = posList[sub]
    return x==-1 and y==-1

def simMove(node,x1,y1,x2,y2,isEne):
    pass