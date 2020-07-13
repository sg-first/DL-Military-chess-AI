import value_net
import train

model=value_net.PolicyValueNet('model0.pkl')
model.model.summary()

cmap = [[13 for _ in range(5)] for _ in range(12)]
probTable = [[0.5 for _ in range(12)] for _ in range(25)]
posList = [[0 for _ in range(2)] for _ in range(25)]
probMap=train.makeCompleteProbMap(probTable,posList)

print(model.predict(cmap,probMap,20,49,1,(100,100,100,100,100,100,100)))
