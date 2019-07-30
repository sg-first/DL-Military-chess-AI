import subprocess

def tableToStr(table):
    s = str(table)
    s = s[1:len(s)-1]
    s = s.replace('[','')
    s = s.replace(' ','')
    s = s.replace('],','\n')
    s = s.replace(']', '')
    return s

def writeLine(msg,p):
    p.stdin.write(msg+'\r\n'.encode())
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
        if line[0]=='G':
            oldPos = (int(line[3]),int(line[4]))
            newPos = (int(line[5]),int(line[6]))
            for i in node.childern:
                oldi, newi, _ = i.move
                if oldPos==oldi and newPos==newi:
                    p.terminate()
                    return i
            p.terminate()
            raise Exception("Can't find the desired child node")
