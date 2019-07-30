import subprocess

def tableToStr(table):
    return str(table[1:len(table)-1])

def _playout(node):
    p = subprocess.Popen('playout.exe', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    # 先发送局面和得到的信息
    p.stdin.writelines(str(node.isEne))
    p.stdin.writelines(tableToStr(node.cMap))
    p.stdin.writelines(tableToStr(node.probTable))
    p.stdin.writelines(tableToStr(node.posList))
    # 发送局面后接收结果即可
    while True:
        line = p.stdout.readline() # 返回的是GO 坐标坐标
        if line[0]=='G':
            oldPos = (int(line[3]),int(line[4]))
            newPos = (int(line[5],int(line[6])))
            for i in node.childern:
                oldi, newi, _ = i.move
                if oldPos==oldi and newPos==newi:
                    return i
            raise Exception("Can't find the desired child node")
        