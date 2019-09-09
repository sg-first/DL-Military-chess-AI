import subprocess

def tableToStr(table):
    s = str(table)
    s = s[1:len(s)-1] # 外层[]截掉
    s = s.replace('[','')
    s = s.replace(' ','')
    s = s.replace('],','nr')
    s = s.replace(']', '')
    return s

def writeLine(msg,p):
    p.stdin.write((msg+'\r\n').encode())
    print(msg+'\r')
    p.stdin.flush()

def _playout(node):
    p = subprocess.Popen('playout.exe', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    # 先发送局面和得到的信息
    writeLine(str(node.isEne),p)
    writeLine(tableToStr(node.cMap),p)
    writeLine(tableToStr(node.probTable),p)
    writeLine(tableToStr(node.posList),p)
    # 发送局面后接收结果即可
    while True:
        line = p.stdout.readline() # 返回的是GO 坐标坐标
        line = line.decode()
        print('line',line)
        if line[0]=='G':
            line=line[1:len(line)-2] # 截掉前面G和后面换行符
            resultList=line.split(',')
            oldPos = (int(resultList[0]),int(resultList[1])) # 这里坐标都是ij形
            newPos = (int(resultList[2]),int(resultList[3]))
            for i in node.children:
                oldi, newi, _ = i.move
                if oldPos==oldi and newPos==newi:
                    p.terminate()
                    return i
            p.terminate()
            raise Exception("Can't find the desired child node")
