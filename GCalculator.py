from scipy import stats
from scipy import sparse
import numpy as np
##This method reduces the expected time from 4 days (naive method) to 10 minutes by accessing raw data of the sparse matrices directly


def calculateG(original,rthresh):
    nrows=original.shape[0]
    flil=sparse.lil_matrix((nrows,nrows))
    m=[mean(row2(original,i)) for i in xrange(nrows)]#precomputing as much as possible (mean and sd of each term)
    sd=[np.sqrt(multiplymean(row2(original,i),row2(original,i))-np.square(m[i])) for i in xrange(nrows)]
    for i in xrange(nrows):
        print i
        for j in xrange(i+1,nrows):
            op=sparsecorrel(row2(original,i), row2(original,j), i, j,m,sd)
            if np.absolute(op)>=rthresh:
                flil[i,j]=op
                flil[j,i]=op
    for i in xrange(nrows):
        flil[i,i]=1
    return flil.tocsr()


def row2(t, i):#returns raw data to do away with the bottlenecking getrow() function and the slow csr_matrix() constructor
    return t.data[t.indptr[i]:t.indptr[i+1]],t.indices[t.indptr[i]:t.indptr[i+1]],t.shape[1]

def mean(ro):
    return ro[0].sum()/float(ro[2])
def multiplymean(ro1, ro2):
    acc=0
    size=ro1[2]
    arrsize=ro1[0].shape[0] if ro1[0].shape[0]<ro2[0].shape[0] else ro2[0].shape[0]
    z=(set(ro1[1])).intersection(set(ro2[1]))
    d1={a:b for (a,b) in zip(ro1[1],ro1[0])}
    d2={a:b for (a,b) in zip(ro2[1],ro2[0])}
    for i in z:
        acc=acc+d1[i]*d2[i]
    return acc/float(size)
    
def sparsecorrel(x,y,i,j, m, sd):
    z=multiplymean(x,y)
    den=sd[i]*sd[j]
    if den==0:
        return 0
    num=z-m[i]*m[j]
    return num/den

    
