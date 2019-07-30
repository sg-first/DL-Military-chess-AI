import subprocess

def tableToStr(table):
    s = str(table)
    s = s[1:len(s)-1]
    s = s.replace('[','')
    s = s.replace(' ','')
    s = s.replace('],','\n')
    s = s.replace(']', '')
    return s

def _playout(node):
    p = subprocess.Popen('playout.exe', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    # 先发送局面和得到的信息
    p.stdin.write(str(node.isEne).encode())
    p.stdin.flush()
    p.stdin.write(tableToStr(node.cMap).encode())
    p.stdin.flush()
    p.stdin.write(tableToStr(node.probTable).encode())
    p.stdin.flush()
    p.stdin.write(tableToStr(node.posList).encode())
    p.stdin.flush()
    # 发送局面后接收结果即可
    while True:
        line = p.stdout.readline() # 返回的是GO 坐标坐标
        line = line.decode()
        if line[0]=='G':
            oldPos = (int(line[3]),int(line[4]))
            newPos = (int(line[5],int(line[6])))
            for i in node.childern:
                oldi, newi, _ = i.move
                if oldPos==oldi and newPos==newi:
                    return i
            raise Exception("Can't find the desired child node")
