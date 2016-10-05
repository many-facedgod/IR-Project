import sys
import pickle
import string
import datrie
import warnings
from collections import OrderedDict
warnings.filterwarnings("ignore")#ignoring warnings in lower versions of scipy



class wchandler:#Wrapper over datrie
    valchars=string.ascii_lowercase+'0123456789.-/\'\\'#all the characters in the non-normalized tokens
    def __init__(self):
        self.Pref_Trie=datrie.Trie(wchandler.valchars)
        self.Post_Trie=datrie.Trie(wchandler.valchars)#two tries for handling postfix and prefix
    
    def add(self, word):
        self.Pref_Trie[unicode(word)]=None#adding words in both the tries
        self.Post_Trie[unicode(word[::-1])]=None
    

    def pref(self, word):
        return set(map(lambda x: str(x), self.Pref_Trie.keys(unicode(word))))
    
    def post(self, word):
        return set(map(lambda x: str(x[::-1]),self.Post_Trie.keys(unicode(word[::-1]))))
    
    def mid(self, prefix, postfix):
        return self.pref(prefix)&self.post(postfix)#for * in the middle, take intersection



##*****************Loading the files to memory**************##
f=open('tokens.data','rb')
tlist=pickle.load(f)
f.close()
f=open("termlist.data", "rb")
termlist=pickle.load(f)
f.close()
tr=wchandler()
for x in tlist:
    tr.add(x)
f = open('idflist.data','rb')
idflist = pickle.load(f)
f.close()
f = open('normlogtf.data','rb')
nltf = pickle.load(f)
f.close()
f=open("GKP0_1.data", "rb")
g=pickle.load(f)
f.close()
kp2=g*nltf
##***********************Loading ends**********************##

def wcquery(query,x):#handles wildcard queries
    l=query.split(" ")
    k=""
    for i in l:
        if "*" in i:#handles the wildcard words separately
            k=i
            break
    y=k.split("*")
    for j,i in enumerate(y):
        if i=="":
	    del y[j] 
    threshold=40#number of queries allowed for a wildcard. Change as required
    z=set()
    if len(y)==2:
        z=tr.mid(y[0], y[1])
    elif len(y)==1:
        if k[0]=="*":
            z=tr.post(y[0])
        else:
            z=tr.pref(y[0])
    li=[]
    sc=[]
    lis=[]
    term=[]
    score=[]
    if len(z)<=threshold:
        for i,t in  enumerate (z):
            a,b=QueryHandle(query+" "+t, x)#simply adds the term, as the astrisk containing word won't affect
	    li.append(a)
	    sc.append(b)
        for i in xrange(len(li)):
            term=term+li[i]
            score=score+sc[i]
        final=sorted(zip(score,term))[::-1]#merging the list obtained by all the queries
	s=set([b for (a,b) in final])
	final=[b for (a,b) in final]
	final=list(OrderedDict.fromkeys(final))#merging can yield duplicates
        final=final if len(final)<=x else final[:x]
    else:#if greater than the threshold, add all terms to a single query to give a less accurate but calculatable result
        for i in z:
            query=query+" "+i
        final,_=QueryHandle(query,x)
    return final#returning the merged list. No need for scores.
            
        


##****************Query Handling************************##
import numpy as np
import pickle
import nltk
import string
import re
from nltk import PorterStemmer
from scipy import sparse

ps = PorterStemmer()

#Tokenizer function
def tok(s):
	tokens = nltk.word_tokenize(s)
	tokens = filter(lambda word: word not in string.punctuation, tokens) #To remove the tokens that are punctuation marks
	finalTok = {}
	for i in tokens:
		if i.endswith("'s"): #To remove trailing 's
			i = i[:len(i)-2]
		i = i.strip('/') #To remove any stray '/' around the words
		for p in string.punctuation: #To remove stray punctuation marks around the words
			i = i.strip(p)
		if len(i)==0:
			continue
		 #To handle hyphenated words
		Temp = i.split('-')
		if len(Temp)>1:
			for l in Temp:
				if l not in finalTok and l!='':
					finalTok[l] = 1
				elif l!='':
					finalTok[l] = finalTok[l]+1
			s = ""
			for l in Temp:
				s = s+l
			if s not in finalTok and s!='':
				finalTok[s] = 1
			elif s!='':
				finalTok[s] = finalTok[s]+1
		#To remove '.' in the tokens
		if len(Temp)==1:
			for temp in Temp:
				temp = temp.split('.')
				for l in temp:
					#To remove ',' between digits (For eg: 100,00)
					if re.match('[0-9]*,[0-9]*', l)!=None:
						x = l.split(",")
						l = ""
						for X in x:
							l = l + X
					if l not in finalTok and l!='':
						finalTok[l] = 1
					elif l!='':
						finalTok[l] = finalTok[l]+1
				if len(temp)>1:
					s = ""
					for l in temp:
						s = s+l
					if s not in finalTok and s!='':
						finalTok[s] = 1
					elif s!='':
						finalTok[s] = finalTok[s]+1
	return finalTok

#To return dictionary of normalized terms
def addToDict(x,dicti,m):
	if re.match('[a-z](.[a-z])*', x)!=None:
		s = x.split('.')
		x = ""
		for X in s:
			x = x + X
		
	stemm = str(ps.stem_word(x))
	if stemm not in dicti:
		dicti[stemm] = 0
	dicti[stemm] = dicti[stemm]+int(m)

#Normalization function
def Lemm(tokens):
	dicti = {}
	for line in tokens:
		if line!='':
			line = line.strip('.')
			if re.match('[0-9]*,[0-9]*', line)!=None:
				s = line.split(',')
				x = ""
				for X in s:
					x = x + X
				addToDict(x,dicti,tokens[line])
			elif re.match('o\'([1-9]|[a-z])*', line)!=None:
				addToDict(line,dicti,tokens[line])
			elif len(line.split(','))>1:
				s = line.split(",")
				for S in s:
					addToDict(S,dicti,tokens[line])
			elif line=="n't":
				addToDict("not", dicti, tokens[line])
			elif len(line.split("'"))>1:
				s = line.split("'")
				for S in s:
					addToDict(S,dicti,tokens[line])
			else:
				x = line
				addToDict(x,dicti,tokens[line])
	return dicti

#Function to return the documents in decreasing order of relevance, along with their relevance values
def sortV(res, indices):
	m = [b for (a,b) in sorted(zip(res,indices))][::-1]
	n = [a for (a,b) in sorted(zip(res,indices))][::-1]
	j = 0
	for i in range(len(n)):
		if n[i]==0:
			break
		j = j + 1
        m=m[:j]
        n=n[:j]
	return m,n
	

def multiplyQTD(qV, gM):
	res = qV*gM
	indices = []
	for i in range(1400):
		indices.append(i)
	res = res.toarray()
	res = res[0]
	return sortV(res,indices)
	
#To returns the list of documents with highest relevance w.r.t the query
def QueryHandle(query, count):
	arr = [0]*len(termlist)
	qterms = Lemm(tok(query))
	for i in range(len(termlist)):
		if termlist[i] in qterms:
			arr[i] = 1+np.log10(qterms[termlist[i]])
	
	y = sparse.csr_matrix(arr)
	arr2 = sparse.csr_matrix(idflist)
	res = y.multiply(arr2)
	square = res.multiply(res)
	leng = square.sum()
	leng = leng**(1/2.0)
	res = res*(1/leng)
	dc,rel = multiplyQTD(res,sparse.csr_matrix(kp2))
	return dc[:count],rel[:count]

#To print the specified document
def printf(l,id):
	index = l[id-1]
	f = open('yet_new_corpus1/'+str(index+1)+'.txt') 
	s = f.read()
	print s
    
##*************************Running the shell*********************##
f=open("FileList.txt","r")
flist=f.read().split("\n")
print("Enter number of results required")
nq=int(raw_input())
while True:
    print "Enter the query:"
    inp=raw_input().lower()
    if inp=='exit':
        sys.exit()
    ctr=inp.count('*')
    if ctr==0:
        dc,rel=QueryHandle(inp,nq)
        print dc
        for i, j in enumerate(dc):
            print "{}. {}".format(i+1, flist[dc[i]])
        print "Open document? Give number for yes, else give \"NO\""
        x=raw_input().lower()
        if x=="no":
            continue
        else:
            printf(dc, int(x))
        continue
    if ctr>1:
        print "Invalid Query"
        continue
    if ctr==1:
        dc= wcquery(inp,nq)
        for i, j in enumerate(dc):
            print "{}. {}".format(i+1, flist[dc[i]])
        print "Open document? Give number for yes, else give \"NO\""
        x=raw_input().lower()
        if x=="no":
            continue
        else:
            printf(dc, int(x))
##*************************************************************##
