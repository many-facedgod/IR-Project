from nltk import PorterStemmer
import re

ps = PorterStemmer()

#To add the normalized terms and their posting lists to the dictionary
def addToDict(k,x,dicti,m):
	if re.match('[a-z](.[a-z])*', x)!=None:
		s = x.split('.')
		x = ""
		for X in s:
			x = x + X
	stemm = str(ps.stem_word(x))
	if stemm not in dicti:
		dicti[stemm] = [0]*1400
	dicti[stemm][k] = dicti[stemm][k]+int(m)

#Dictionary of all the normalized terms and their respective posting lists
dicti = {}
for k in range(0, 1400):
	print k
	f = open('Tokens/'+str(k)+'.txt', 'r')
	lines = f.read().split('\n')
	f.close()
	for line in lines:
		if line !='': 
			line = line.split()
			line[0] = line[0].strip('.') #To remove stray '.' around the words
			if re.match('[0-9]*,[0-9]*', line[0])!=None: #To remove ',' between digits (For eg: 100,00)
				s = line[0].split(',')
				x = ""
				for X in s:
					x = x + X
				addToDict(k,x,dicti,line[1])
			elif re.match('o\'([1-9]|[a-z])*', line[0])!=None: #To handle words like "o'brian"
				addToDict(k,line[0],dicti,line[1])
				s = line[0].split("'")
				x = s[0]+s[1]
				addToDict(k,x,dicti,line[1])
			elif len(line[0].split(','))>1: #To split any words with ','s
				s = line[0].split(",")
				for S in s:
					addToDict(k,S,dicti,line[1])
			elif line[0]=="n't": #To convert "n't" to "not"
				addToDict(k,"not", dicti, line[1])
			elif len(line[0].split("'"))>1:
				s = line[0].split("'")
				for S in s:
					addToDict(k,S,dicti,line[1])
			else:
				x = line[0]
				addToDict(k,x,dicti,line[1])
#To store all the terms with their posting lists in a file
f = open('terms2.txt', 'w')
keys = []
for key in dicti:
	keys.append(key)
keys.sort()

for word in keys:
	f.write(word+" ")
	sumi = 0
	for doc in dicti[word]:
		sumi = sumi + doc
	f.write(str(sumi)+" ")
	for i in range(0,1400):
		if dicti[word][i]>0:		
			f.write(str(i)+" "+str(dicti[word][i])+ " ")
	f.write('\n')
f.close()	
