import value_net

model=value_net.PolicyValueNet('model0.pkl')
cmap = [[0 for _ in range(5)] for _ in range(12)]
probTable = [[0 for _ in range(12)] for _ in range(25)]
posList = [[0 for _ in range(2)] for _ in range(25)]
round=0
model.predict(cmap,probTable,)