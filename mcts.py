import help
import basic
import simulate
import playout
import asses
import value_net
import train
import math

model = value_net.PolicyValueNet('model0.pkl')
epoch = 1000 # 目前训练伦次
n_epoch = 2500 # 期待训练轮次（超参数）
n_playout = 10000 # 模拟次数（超参数）

openMCTS=False

_n_qc = 1 # 快速走棋总次数，用于UCB公式计算（每手更新）

class TreeNode:
    def __init__(self, isEne:bool, cMap:list, probTable:list, posList:list, layer = 0, move = None, parent = None):
        self.parent = parent
        self.move = move # 从哪移动到哪，注意，这个实际是上一手走的
        self.cMap = cMap
        self.probTable = probTable
        self.posList = posList
        self.isEne = isEne
        self.layer = layer # handNum+layer=上次走完的总手数

        self.children = []
        self._n_visits = 1  # 快速走棋次数

        # 不管是我方还是敌方，胜率都是以我方为标准，但是选择的时候敌方的层选min
        probMap = help.copy2DList(probTable)
        probMap = train.makeCompleteProbMap(probMap, posList)
        myChessNum, eneChessNum=basic.caluChessNum(self.cMap) # 我方、敌方棋子数
        estResult = asses.valueEstimation(cMap,self) # 局面评估七项
        self.nnQ = model.predict(self.cMap, probMap, basic.handNum+self.layer, myChessNum, eneChessNum,
                            estResult) # 神经网络胜率，构造时立即预测
        self.qcQ = 0 # 快速走棋胜率
        self.qcScore = 0 # 快速走棋得分

    def select(self,useUCB=True):
        def s():
            if self.isEne:
                return min(self.children, key=lambda x: x.getValue(useUCB))
            else:
                return max(self.children, key=lambda x: x.getValue(useUCB))

        if self.is_leaf():
            end, isWin = basic.game_end(self) # 检查游戏是否结束
            if not end:
                self.extend()
                return s()
            else:
                self.update_recursive(isWin) # 递归更新快速走棋评分
                return None
        else:
            return s()

    def update(self,isWin:int):
        """完成一次快速走棋之后更新本节点快速走棋评分
        """
        self._n_visits += 1
        self.qcScore += isWin
        self.qcQ += self.qcScore / (self._n_visits-1) # 取频率为概率

    def update_recursive(self, isWin:int):
        """更新所有父节点的快速走棋评分
        """
        if self.parent:
            self.parent.update_recursive(isWin)
        self.update(isWin)

    def getValue(self, useUCB=True):
        """计算并返回此节点的加权Q值，用于指导下一步扩展或直接给出最优落子
        """
        nnPar = epoch/n_epoch
        if useUCB:
            weightingQcQ = self.qcQ + math.sqrt((2*help.ln(_n_qc)/self._n_visits)) # UCB选取
        else:
            weightingQcQ = self.qcQ
        return nnPar*self.nnQ + (1-nnPar)*weightingQcQ # 与神经网络Q加权
        # （通过调参可实现只用MSTC不考虑神经网络，反之应当直接设openMCTS=False）

    def extend(self):
        print('extend:')
        import numpy as np
        print(np.array(self.cMap))

        for i in range(12):
            for j in range(5):
                if self.isEne:
                    condition = basic.IsEneChess(i,j,self.cMap)
                else:
                    condition = basic.IsMyChess(i,j,self.cMap)
                if condition:
                    allPos=basic.getAccessibility(i,j,self.isEne,self.posList,self.cMap,self.probTable)
                    print('layer:', self.layer)
                    for newi,newj in allPos:
                        print('move:',j,i,newj,newi)
                        print('棋子1:',self.cMap[i][j])
                        print('棋子2:',self.cMap[newi][newj])
                        cMap, isMove, posList = simulate.simMove(self,j,i,newj,newi,self.isEne)
                        # 扩展子节点
                        self.children.append(TreeNode(not self.isEne, cMap, self.probTable, posList, self.layer+1,
                                                      ((i,j),(newi,newj),isMove), self))

    def is_leaf(self):
        return len(self.children) == 0

    def playout(self):
        if self.is_leaf():
            end, isWin = basic.game_end(self) # 检查游戏是否结束
            if not end:
                self.extend()

                import numpy as np
                print(np.array(self.cMap))

                playout._playout(self).playout()  # playout._playout(self)最后一步要把走法转换为self对应的子节点（然后递归调用）
            else:
                self.update_recursive(isWin) # 递归更新快速走棋评分
        else:
            playout._playout(self).playout()  # playout._playout(self)最后一步要把走法转换为self对应的子节点


lastUsNum = None # 上次使用MCTS时我方棋子数
lastEneNum = None # 对方棋子数

class MCTS:
    """An implementation of Monte Carlo Tree Search."""

    def __init__(self, handNum, cMap, probTable, posList):
        # 统计双方棋子数
        usNum = 0
        eneNum = 0
        global lastUsNum
        global lastEneNum
        for i in range(12):
            for j in range(5):
                if basic.IsMyChess(i,j,cMap):
                    usNum += 1
                if basic.IsEneChess(i,j,cMap):
                    eneNum += 1
        # 第一次使用，初始化lastUsNum
        if handNum == 1 or handNum == 2:
            lastUsNum = usNum
            lastEneNum = eneNum
        # 棋子数有变，更新吃子记录
        if usNum != lastUsNum:
            lastUsNum = usNum
            basic.eneBeatHand = handNum - 1
        if eneNum != lastEneNum:
            lastEneNum = eneNum
            basic.usBeatHand = handNum - 1
        # 调整其它变量
        global _n_qc
        _n_qc = 1
        basic.handNum = handNum
        # 环境初始化完毕，创建根节点
        self.root = TreeNode(False, cMap, probTable, posList)

    def simulation(self): # 调用一次是一次模拟，为了获取更好的快速走棋评分
        node = self.root
        while(node is not None):
            if node._n_visits == 1: # 没有进行过快速走棋（没有看过）
                if not (epoch>(n_epoch*3/4) and (node.nnQ>0.7 or node.nnQ<0.3)): # 不满足无快速走棋选择条件
                   node.playout() # 使用快速走棋走到结束
            node = node.select() # 模拟走棋的扩展需开启UCB给探索提供更多可能性

    def get_best_move(self):
        if openMCTS:
            # 开始模拟
            for _ in range(n_playout):
                self.simulation() # 这里面会根据情况进行扩展
        else:
            self.root.extend() # 不模拟直接用神经网络评分，所以直接在这里给根节点扩展一次即可

        p1,p2,isMove = self.root.select(False).move # 最终求结果的扩展不开启UCB，得到目前信息下的最近似结果

        return (p1,p2)

import configparser

if __name__=="__main__":
    cf = configparser.ConfigParser()
    cf.read('input.ini')
    handNum = int(cf.get('main', 'handNum'))
    cMap = cf.get('main', 'cMap')
    probTable = cf.get('main', 'probTable')
    posList = cf.get('main', 'posList')

    import inputHelp
    cMap = inputHelp.inputMap(cMap, splitToken='-n')
    probTable = inputHelp.inputProb(probTable, splitToken='-n')
    posList = inputHelp.inputPos(posList, splitToken='-n')

    mctsObj=MCTS(handNum,cMap,probTable,posList)
    result=mctsObj.get_best_move()
    p1,p2=result
    oldi,oldj=p1
    newi,newj=p2

    cf2 = configparser.ConfigParser()
    cf2.add_section('main')
    cf2.set('main', 'oldi', str(oldi))
    cf2.set('main', 'oldj', str(oldj))
    cf2.set('main', 'newi', str(newi))
    cf2.set('main', 'newj', str(newj))
    cf2.write(open('output.ini', 'w'))
    open('finish', 'w') # 工作完成，创建文件进行提示