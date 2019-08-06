import subprocess

def tableToStr(table):
    s = str(table)
    s = s[1:len(s)-1]
    s = s.replace('[','')
    s = s.replace(' ','')
    s = s.replace('],','-n')
    s = s.replace(']', '')
    return s

def writeLine(msg,p):
    p.stdin.write((msg+'\r\n').encode())
    p.stdin.flush()

def _playout(node):
    p = subprocess.Popen('playout.exe', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    # 先发送局面和得到的信息
    writeLine(str(True),p)
    writeLine(tableToStr(node),p)
    writeLine(tableToStr(node), p)
    writeLine(tableToStr(node), p)
    # 发送局面后接收结果即可
    while True:
        line = p.stdout.readline() # 返回的是GO 坐标坐标
        line = line.decode()
        print(line)
        if line[0]=='G':
            oldPos = (int(line[3]),int(line[4]))
            newPos = (int(line[5]),int(line[6]))
            p.terminate()
            print(oldPos)
            print(newPos)
            p.terminate()
            break

import numpy as np
r = np.random.randint(0,100,(12,5))
r = r.tolist()
_playout(r)