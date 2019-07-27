from keras.engine.topology import Input
from keras.engine.training import Model
from keras.layers.convolutional import Conv2D, Conv1D
from keras.layers.core import Activation, Dense, Flatten, Lambda
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2
from keras.optimizers import Adam
import keras.backend as K
import pickle


class PolicyValueNet():
    def __init__(self, model_file=None):
        self.l2_const = 1e-4  # coef of l2 penalty
        self.create_net()
        self.train_op()

        if model_file:
            net_params = pickle.load(open(model_file, 'rb'))
            self.model.set_weights(net_params)


    def create_net(self):
        board = Input((5, 12))
        probTable = Input((12,12+2)) # 多出来那两个是对应的坐标
        otherFeature = Input((3,)) # 目前手数，我方棋子数，敌方棋子数

        # conv layers
        network1 = Conv1D(filters=8, kernel_size=3, padding="same", data_format="channels_first",
                         activation="relu", kernel_regularizer=l2(self.l2_const))(board)
        network1 = Conv1D(filters=32, kernel_size=3, padding="same", data_format="channels_first",
                         activation="relu", kernel_regularizer=l2(self.l2_const))(network1)
        network2 = Conv1D(filters=8, kernel_size=3, padding="same", data_format="channels_first",
                          activation="relu", kernel_regularizer=l2(self.l2_const))(probTable)
        network2 = Conv1D(filters=32, kernel_size=3, padding="same", data_format="channels_first",
                          activation="relu", kernel_regularizer=l2(self.l2_const))(network2)

        network = Lambda(lambda x: K.concatenate([x[0],x[1]], axis=1+1))([network1,network2])

        # state value layers
        value_net = Conv1D(filters=4, kernel_size=1, data_format="channels_first", activation="relu",
                           kernel_regularizer=l2(self.l2_const))(network)
        value_net = Conv1D(filters=2, kernel_size=1, data_format="channels_first", activation="relu",
                           kernel_regularizer=l2(self.l2_const))(value_net)
        value_net = Flatten()(value_net)
        value_net = Lambda(lambda x: K.concatenate([x[0],x[1]]))([value_net,otherFeature]) # 考虑其它特征
        value_net = Dense(32, activation='relu', kernel_regularizer=l2(self.l2_const))(value_net)
        value_net = Dense(16, activation='relu', kernel_regularizer=l2(self.l2_const))(value_net) # 这里原来是线性层，改成了relu
        self.value_net = Dense(1, activation="tanh", kernel_regularizer=l2(self.l2_const))(value_net)

        self.model = Model(inputs=[board,probTable,otherFeature], outputs=self.value_net)


    def train_op(self):
        """
        Three loss terms：
        loss = (z - v)^2 + pi^T * log(p) + c||theta||^2
        """

        self.model.compile(optimizer=Adam(), loss='mean_squared_error')

        def train_step(board, probMap, isFirstHand, isWin, learning_rate): # isWin与isFirstHand一样为bool列表，表示是否胜利
            loss = self.model.evaluate([board,probMap,isFirstHand], isWin, batch_size=len(board),
                                       verbose=0)
            K.set_value(self.model.optimizer.lr, learning_rate)
            # fix:目前所有胜利的局面值都为1，实际应当根据Q值更新公式给予远距离的局面一些折扣？
            self.model.fit([board,probMap,isFirstHand], isWin, batch_size=len(board))
            return loss[0]

        self.train_step = train_step
        return train_step


    def get_param(self):
        net_params = self.model.get_weights()
        return net_params


    def save_model(self, model_file):
        pickle.dump(self.model, open(model_file, 'wb'), protocol=2)

PolicyValueNet()