import numpy as np
import copy
import math
import basic

value_fn = None # 神经网络估值函数
playout_fn = None # 快速走棋函数
epoch = 0
n_epoch = 10000 # 总训练轮次（超参数）
n_playout = 10000 # 模拟次数（超参数）

_n_qc = 1 # 快速走棋总次数，用于UCB公式计算

def ln(x):
    return math.log(x,math.e)

class TreeNode:
    def __init__(self, isEne, cMap, probTable, move = None, parent = None):
        self._parent = parent
        self.move = move
        self.cMap = cMap
        self.probTable = probTable
        self.isEne = isEne
        self.children = []
        self._n_visits = 1  # 快速走棋次数

        # 不管是我方还是敌方，胜率都是以我方为标准，但是选择的时候敌方的层选min
        self.nnQ = value_fn(self.cMap,self.probTable) # 神经网络胜率，构造时立即预测
        self.qcQ = 0 # 快速走棋胜率
        self.qcScore = 0 # 快速走棋得分

    def select(self):
        def s():
            if self.isEne:
                return min(self.children, lambda x: x.get_value())
            else:
                return max(self.children, lambda x: x.get_value())

        if self.is_leaf():
            end, isWin = basic.game_end() # 检查游戏是否结束
            if not end:
                self.extend()
                return s()
            else:
                self.update_recursive(isWin) # 递归更新快速走棋评分
                return None
        else:
            return s()

    def update(self,isWin):
        """完成一次快速走棋之后更新本节点快速走棋评分
        """
        self._n_visits += 1
        self.qcScore += isWin
        self.qcQ += self.qcScore / (self._n_visits-1) # 取频率为概率

    def update_recursive(self, isWin):
        """更新所有父节点的快速走棋评分
        """
        if self._parent:
            self._parent.update_recursive(isWin)
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
                    condition = self.cMap[i][j]==13
                else:
                    condition = self.cMap[i][j]>=1 and self.cMap[i][j]<=12
                if condition:
                    allPos=basic.getNearPos(i,j)
                    for newi,newj in allPos:
                        newCMap = self.cMap[:]
                        chess = self.cMap[i][j]
                        newCMap[newi][newj]=chess
                        newCMap[i][j] = 0
                        # 扩展子节点
                        self.children.append(TreeNode(not self.isEne, self.cMap, self.probTable, ((i,j),(newi,newj), self)))

    def is_leaf(self):
        return len(self.children) == 0

    def playout(self):
        if self.is_leaf():
            end, isWin = basic.game_end() # 检查游戏是否结束
            if not end:
                self.extend()
                playout_fn(self).playout()  # playout_fn最后一步要把走法转换为self对应的子节点
            else:
                self.update_recursive(isWin) # 递归更新快速走棋评分
        else:
            playout_fn(self).playout()  # playout_fn最后一步要把走法转换为self对应的子节点


class MCTS:
    """An implementation of Monte Carlo Tree Search."""

    def __init__(self, cMap, probTable):
        self.root = TreeNode(False, cMap, probTable)

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
        return self.root.select().move
