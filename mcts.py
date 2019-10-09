import help
import basic
import simulate
import asses
import value_net
import train

model = value_net.PolicyValueNet('model0.pkl')
searchLayerNum=4

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


    def estimation(self,alpha,beta):
        if self.layer==searchLayerNum:
            # 不管是我方还是敌方，胜率都是以我方为标准，但是选择的时候敌方的层选min
            probMap = help.copy2DList(probTable)
            probMap = train.makeCompleteProbMap(probMap, posList)
            myChessNum, eneChessNum = basic.caluChessNum(self.cMap) # 我方、敌方棋子数
            estResult = asses.valueEstimation(self) # 局面评估七项
            self.nnQ = model.predict(self.cMap, probMap, basic.handNum+self.layer, myChessNum, eneChessNum,
                                estResult) # 神经网络胜率，构造时立即预测
            return -self.nnQ # 这里没有扩展，评估的就是当前层，所以得和在extend里的调用负负得正
        else:
            return self.extend(alpha,beta) # 传进来的时候已经倒完了，这里直接传即可


    def select(self,useUCB=True):
        if self.isEne:
            return min(self.children, key=lambda x: x.nnQ)
        else:
            return max(self.children, key=lambda x: x.nnQ)


    def extend(self,alpha,beta):
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
                        newNode=TreeNode(not self.isEne, cMap, self.probTable, posList, self.layer+1,
                                            ((i,j),(newi,newj),isMove), self)
                        self.children.append(newNode)
                        newNode.nnQ = -newNode.estimation(-beta, -alpha)  # 对该子节点评估
                        if newNode.nnQ > alpha:  # 更新最大值
                            alpha = newNode.nnQ
                        if alpha>=beta:
                            return alpha
        return alpha


    def is_leaf(self):
        return len(self.children) == 0


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

    def get_best_move(self):
        self.root.extend(-100000,100000)
        p1,p2,isMove = self.root.select(False).move
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