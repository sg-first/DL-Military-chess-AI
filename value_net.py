from keras.engine.topology import Input
from keras.engine.training import Model
from keras.layers.convolutional import Conv2D
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

        if model_file:
            net_params = pickle.load(open(model_file, 'rb'))
            self.model.set_weights(net_params)


    def create_net(self):
        board = Input((1, 12, 5))
        probTable = Input((1, 12+2, 25)) # 多出来那两个是对应的坐标（注意转置）
        otherFeature = Input((10,)) # 目前手数，我方棋子数，敌方棋子数，局面评估7项

        # conv layers
        network1 = Conv2D(filters=8, kernel_size=(3, 3), padding="same", data_format="channels_first",
                         activation="relu", kernel_regularizer=l2(self.l2_const))(board)
        network1 = Conv2D(filters=32, kernel_size=(3, 3), padding="same", data_format="channels_first",
                         activation="relu", kernel_regularizer=l2(self.l2_const))(network1)
        network2 = Conv2D(filters=8, kernel_size=(3, 3), padding="same", data_format="channels_first",
                          activation="relu", kernel_regularizer=l2(self.l2_const))(probTable)
        network2 = Conv2D(filters=32, kernel_size=(3, 3), padding="same", data_format="channels_first",
                          activation="relu", kernel_regularizer=l2(self.l2_const))(network2)
        # 后面的设置需要斟酌
        network1 = Conv2D(filters=4, kernel_size=(1, 1), data_format="channels_first", activation="relu",
                           kernel_regularizer=l2(self.l2_const))(network1)
        network1 = Conv2D(filters=2, kernel_size=(1, 1), data_format="channels_first", activation="relu",
                           kernel_regularizer=l2(self.l2_const))(network1)
        network2 = Conv2D(filters=4, kernel_size=(1, 1), data_format="channels_first", activation="relu",
                          kernel_regularizer=l2(self.l2_const))(network2)
        network2 = Conv2D(filters=2, kernel_size=(1, 1), data_format="channels_first", activation="relu",
                          kernel_regularizer=l2(self.l2_const))(network2)

        # state value layers
        network1 = Flatten()(network1)
        network2 = Flatten()(network2)
        value_net = Lambda(lambda x: K.concatenate([x[0], x[1]]), output_shape=(820,))([network1, network2])
        value_net = Lambda(lambda x: K.concatenate([x[0],x[1]]), output_shape=(830,))([value_net,otherFeature]) # 考虑其它特征
        value_net = Dense(32, activation='relu', kernel_regularizer=l2(self.l2_const))(value_net)
        value_net = Dense(16, activation='relu', kernel_regularizer=l2(self.l2_const))(value_net) # 这里原来是线性层，改成了relu
        self.value_net = Dense(1, activation="tanh", kernel_regularizer=l2(self.l2_const))(value_net)

        self.model = Model(inputs=[board,probTable,otherFeature], outputs=self.value_net)
        self.model.compile(optimizer=Adam(), loss='mean_squared_error')


    def train(self, board, probMap, otherFeature, isWin, epoch, batch_size):  # isWin与isFirstHand一样为bool列表，表示是否胜利
        # fix:目前所有胜利的局面值都为1，实际应当根据Q值更新公式给予远距离的局面一些折扣？
        self.model.fit([board, probMap, otherFeature], isWin, batch_size=batch_size, epochs=epoch)


    def test(self,board,probMap,otherFeature,isWin):
        result=self.model.predict([board, probMap, otherFeature])
        posRight=0
        negRight=0
        for i in range(len(isWin)):
            if result[i]>0.5 and isWin[i]==1:
                posRight+=1
            elif result[i]<0.5 and isWin[i]==0:
                negRight+=1
        return posRight, negRight


    def get_param(self):
        net_params = self.model.get_weights()
        return net_params


    def save_model(self, model_file):
        pickle.dump(self.model, open(model_file, 'wb'), protocol=2)
