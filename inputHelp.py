def inputMap(inmap:str, start=0, isFirst=True, splitToken='\n'):
    inmap = inmap.split(splitToken)
    end = start + 12
    temmap = [[0 for _ in range(5)] for _ in range(12)]
    for i in range(start,end):
        if(isFirst==True):
            temmap1 = inmap[i].split()
            temmap2 = ['0' if i == '\x00' else i for i in temmap1]
            temmap2 = [int(x) for x in temmap2]
            temmap[i] = temmap2
        else:
            temmap1 = inmap[i].split()
            temmap2 = ['0' if i == '\x00' else i for i in temmap1]
            temmap2 = [int(x) for x in temmap2]
            temmap[i-1] = temmap2
    return temmap

def inputProb(inprob:str, start=0, splitToken='\n'):
    inprob = inprob.split(splitToken)
    end = start + 25
    temProb = [[0 for _ in range(12)] for _ in range(25)]
    for i in range(start, end):
        temProb1 = inprob[i].split()
        temProb1 = [float(x) for x in temProb1]
        temProb[i - 1] = temProb1
    return temProb

def inputPos(inpos:str, start=0, splitToken='\n'):
    inpos = inpos.split(splitToken)
    end = start + 25
    temPos = [[0 for _ in range(2)] for _ in range(25)]
    for i in range(start, end):
        temPos1 = inpos[i].split()
        temPos1 = [int(x) for x in temPos1]
        temPos[i - 1] = temPos1
    return temPos

def inputRounds(temRounds:str):
    temmRounds = temRounds.split()
    return int(temmRounds[0])