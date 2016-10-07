from scipy import sparse
import numpy as np
import pickle
f=open("C:/Python27/logtf.data", "rb")
x=pickle.load(f)
f.close()
f=open("C:/Python27/idflist.data", "rb")
s=pickle.load(f)
z=x.tolil()
for i in xrange(7838):
    for j in xrange(1400):
        if z[i,j]!=0:
            z[i,j]=z[i,j]*s[i]
x=z.tocsr()
f=open("C:/Python27/idflogtf.data","wb")
pickle.dump(x, f)

