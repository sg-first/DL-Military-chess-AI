from keras.engine.topology import Input
from keras.engine.training import Model
from keras.layers.convolutional import Conv2D
from keras.layers.core import Dense, Flatten, Lambda
from keras.layers import MaxPooling2D
import keras.callbacks as callbacks
import LossHistory
from keras.regularizers import l2
from keras.optimizers import Adam
import keras.backend as K
import pickle
import numpy as np

def Recall(y_true, y_pred):
    """召回率"""
    tp = K.sum(K.round(K.clip(y_true * y_pred, 0, 1))) # true positives
    pp = K.sum(K.round(K.clip(y_true, 0, 1))) # possible positives
    recall = tp / (pp + K.epsilon())
    return recall

callback_list = [
        callbacks.EarlyStopping(monitor="val_loss", patience=70),
        # callbacks.ModelCheckpoint(filepath="model_1.h5", monitor="val_loss", save_best_only=True),
        callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.7, verbose=1, patience=5)
    ]

class PolicyValueNet():
    def __init__(self, model_file=None):
        self.l2_const = 1e-4  # coef of l2 penalty
        self.create_net()

        if model_file:
            self.model = pickle.load(open(model_file, 'rb'))
            # self.model.set_weights(net_params)


    def create_net(self):
        board = Input((1, 21, 21))
        otherFeature = Input((10,)) # 目前手数，我方棋子数，敌方棋子数，局面评估7项

        # conv layers
        network1 = Conv2D(filters=32, kernel_size=(3, 3), padding="same", data_format="channels_first",
                         activation="relu", kernel_regularizer=l2(self.l2_const))(board)
        # network1 = Conv2D(filters=64, kernel_size=(3, 3), padding="same", data_format="channels_first",
        #                  activation="relu", kernel_regularizer=l2(self.l2_const))(network1)
        # network1 = Conv2D(filters=128, kernel_size=(3, 3), padding="same", data_format="channels_first",
        #                   activation="relu", kernel_regularizer=l2(self.l2_const))(network1)
        network1 = MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid', data_format='channels_first')(network1)
        network1 = Conv2D(filters=16, kernel_size=(3, 3), padding="same", data_format="channels_first",
                          activation="relu", kernel_regularizer=l2(self.l2_const))(network1)
        network1 = Conv2D(filters=4, kernel_size=(3, 3), padding="same", data_format="channels_first",
                          activation="relu", kernel_regularizer=l2(self.l2_const))(network1)
        network1 = Conv2D(filters=1, kernel_size=(3, 3), padding="same", data_format="channels_first",
                          activation="relu", kernel_regularizer=l2(self.l2_const))(network1)
        network1 = MaxPooling2D(pool_size=(2, 2), strides=None, padding='valid', data_format='channels_first')(network1)

        # state value layers
        network1 = Flatten()(network1)
        value_net = Lambda(lambda x: K.concatenate([x[0], x[1]]), output_shape=(35,))([network1, otherFeature])
        value_net = Dense(16, activation='relu', kernel_regularizer=l2(self.l2_const))(value_net)
        value_net = Dense(8, activation='relu', kernel_regularizer=l2(self.l2_const))(value_net) # 这里原来是线性层，改成了relu
        self.value_net = Dense(1, activation="sigmoid", kernel_regularizer=l2(self.l2_const))(value_net)

        self.model = Model(inputs=[board,otherFeature], outputs=self.value_net)
        print(self.model.summary())
        self.model.compile(optimizer='Adam', loss="binary_crossentropy", metrics=["acc",Recall])


    def train(self, board, otherFeature, isWin, epoch, batch_size):  # isWin与isFirstHand一样为bool列表，表示是否胜利
        # fix:目前所有胜利的局面值都为1，实际应当根据Q值更新公式给予远距离的局面一些折扣？
        history = LossHistory.LossHistory()
        self.model.fit([board, otherFeature], isWin, batch_size=batch_size, epochs=epoch, callbacks=callback_list, validation_split=0.3)
        return history

    def predict(self, board, probMap, rounds, myChessNum, eneChessNum, estResult): # 预测的是一个
        otherFeature=[rounds,myChessNum,eneChessNum]+list(estResult)
        otherFeature=np.array([otherFeature])
        board=np.array([[board]])
        probMap=np.array(probMap).T # 先得到正确形式
        probMap=np.array([[probMap]]) # 后包两层
        return self.model.predict([board,probMap,otherFeature])[0]

    def test(self,board,otherFeature,isWin): # 应该直接在fit时用交叉验证，不用这个
        result=self.model.predict([board, otherFeature])
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
