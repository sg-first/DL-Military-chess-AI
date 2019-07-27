def findChess(x,y,posList):
    sub = 0
    for xi,yi in posList:
        if x==xi and y==yi:
            return sub
        else:
            sub += 1

def simMove(node,x1,y1,x2,y2,isEne):
    pass