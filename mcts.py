import math
import basic
import simulate
import playout
import asses

value_fn = None # 神经网络估值函数
epoch = 0
n_epoch = 10000 # 总训练轮次（超参数）
n_playout = 10000 # 模拟次数（超参数）

_n_qc = 1 # 快速走棋总次数，用于UCB公式计算（每手更新）

def ln(x):
    return math.log(x,math.e)

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
        cMapValue = asses.valueEstimation(cMap,self)
        # fix: 还需要其它参数
        self.nnQ = value_fn(self.cMap,self.probTable,cMapValue) # 神经网络胜率，构造时立即预测
        self.qcQ = 0 # 快速走棋胜率
        self.qcScore = 0 # 快速走棋得分

    def select(self):
        def s():
            if self.isEne:
                return min(self.children, lambda x: x.get_value())
            else:
                return max(self.children, lambda x: x.get_value())

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

    def get_value(self):
        """计算并返回此节点的加权Q值
        """
        nnPar = epoch/n_epoch
        weightingQcQ = self.qcQ + math.sqrt((2*ln(_n_qc)/self._n_visits)) # UCB选取
        return nnPar*self.nnQ + (1-nnPar)*weightingQcQ # 与神经网络Q加权

    def extend(self):
        for i in range(12):
            for j in range(5):
                if self.isEne:
                    condition = basic.IsEneChess(i,j,self.cMap)
                else:
                    condition = basic.IsMyChess(i,j,self.cMap)
                if condition:
                    allPos=basic.getAccessibility(i,j,self.isEne)
                    for newi,newj in allPos:
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
                playout._playout(self).playout()  # playout._playout(self)最后一步要把走法转换为self对应的子节点
            else:
                self.update_recursive(isWin) # 递归更新快速走棋评分
        else:
            playout._playout(self).playout()  # playout._playout(self)最后一步要把走法转换为self对应的子节点


lastUsNum = None # 上次使用MCTS时我方棋子数
lastEneNum = None # 对方棋子数

class MCTS:
    """An implementation of Monte Carlo Tree Search."""

    def __init__(self, handNum, cMap, probTable, posList):
        self.root = TreeNode(False, cMap, probTable, posList)
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
            basic.eneBeatHand = handNum - 1
        # 调整其它变量
        global _n_qc
        _n_qc = 1
        basic.handNum = handNum

    def simulation(self): # 调用一次是一次模拟，为了获取更好的快速走棋评分
        node = self.root
        while(node is not None):
            if node._n_visits == 1: # 没有进行过快速走棋（没有看过）
                if not (epoch>(n_epoch*3/4) and (node.nnQ>0.7 or node.nnQ<0.3)): # 不满足无快速走棋选择条件
                   node.playout() # 使用快速走棋走到结束
            node = node.select()

    def get_best_move(self):
        # 开始模拟
        for _ in range(n_playout):
            self.simulation()

        p1,p2,isMove = self.root.select().move
        if not isMove: # 如果是吃子，记录我方吃子手数
            basic.usBeatHand = basic.handNum

        return (p1,p2)

import configparser

if __name__=="__main__":
    cf = configparser.ConfigParser()
    cf.read('input.ini')
    handNum = int(cf.get('main', 'handNum'))
    cMap = int(cf.get('main', 'cMap'))
    probTable = int(cf.get('main', 'probTable'))
    posList = int(cf.get('main', 'posList'))

    # fix:将cMap probTable posList转换成二维数组

    mctsObj=MCTS(handNum,cMap,probTable,posList)
    result=mctsObj.get_best_move()
    i,j=result

    cf2 = configparser.ConfigParser()
    cf2.add_section('main')
    cf2.set('main', 'i', str(i))
    cf2.set('main', 'j', str(j))
    cf2.write(open('output.ini', 'w'))
    open('finish', 'w') # 工作完成，创建文件进行提示