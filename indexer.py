import numpy as np
from scipy import sparse
import pickle
f=open("C:/Python27/data.txt", "r")
t=7838#Number of terms
docs=1400#number of documents
tfmatlil=sparse.lil_matrix((t,docs))#lil matrices are easier to create
lis={}
idf={}
terms=[]
for i, r in enumerate(f):
    r=r[:len(r)-1]
    r=r.split(" ")
    print i
    terms.append(r[0])
    l=(len(r)/2)-1
    lis[r[0]]={}
    idf[r[0]]=0 if int(l)==0 else np.log10(docs/float(l))#calculating the idf
    for s,t in zip(r[2::2],r[3::2]):
        (lis[r[0]])[int(s)]=int(t)
        tfmatlil[int(i),int(s)]=int(t)
tf=tfmatlil.tocsr()#csr because it supports efficient multiplication
###Dumping the data###
f.close()
f=open("termlist.data", "wb")
pickle.dump(terms, f)
f.close()
f=open("idf.data", "wb")
pickle.dump(idf, f)
f.close()
f=open("tf.data", "wb")#required for SVD computation, did not work out
pickle.dump(tf, f)
f.close()
f=open("C:/Python27/invindex.data", "wb")
pickle.dump(lis, f)
f.close()
for i, x in enumerate(tf.data):
    tf.data[i]=0 if x==0 else 1+np.log10(x)
f=open("logtf.data", "wb")
pickle.dump(tf, f)
f.close()

