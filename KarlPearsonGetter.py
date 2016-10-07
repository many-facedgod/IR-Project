from scipy import sparse
import numpy as np
import pickle

###script takes the normalizedlogtf matrix and multiplies it with G###
f=open("C:/Python27/normlogtf.data", "rb")
x=pickle.load(f)
f.close()
f=open("C:/Python27/GKP0_6.data", "rb")
y=pickle.load(f)
f.close()
z=y*x
f=open("C:/Python27/KP2.data", "wb")
pickle.dump(z, f)
