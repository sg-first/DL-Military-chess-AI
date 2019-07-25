import numpy as np
import keras.backend as K

m1=np.random.randint(0,2,(2,1,))
m2=np.random.randint(0,100,(2,2*(5+12)*12))

print(m1)
print(m2)

a = K.variable(m1)
b = K.variable(m2)
c1 = K.concatenate([a,b])

print(K.eval(c1))