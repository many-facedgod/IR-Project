from scipy import sparse
import numpy as np
import pickle

###script normalizes the logtf matrix and gives 
f=open("C:/Python27/logtf.data", "rb")
x=pickle.load(f)
y=x.multiply(x)
s=np.sqrt(y.sum(0)).tolist()[0]
s=[i if i!=0 else 1 for i in s]
z=x.tolil()
for i in xrange(1400):
    for j in xrange(7838):
        if z[j,i]!=0:
            z[j,i]=z[j,i]/s[i]
x=z.tocsr()
f=open("C:/Python27/normlogtf.data","wb")
pickle.dump(x, f)

