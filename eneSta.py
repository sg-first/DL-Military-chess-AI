def findChess(x,y,posList):
    sub = 0
    for yi,xi in posList:
        if x==xi and y==yi:
            return sub
        else:
            sub += 1

def setDie(sub,posList): # 仅该函数对posList产生副作用
    posList[sub] = [-1,-1]

def isDie(sub,posList):
    i,j=posList[sub]
    return i==-1 and j==-1