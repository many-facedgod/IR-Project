import nltk
import pickle
from scipy import sparse

dicti = {}
for k in range(1400):
	print k
	f = open('Tokens2/'+str(k)+'.txt', 'r')
	listd = f.read()
	lines = listd.split('\n')
	for line in lines:
		if line != '':
			term = line.split(' ')
			if term[0] not in dicti:
				dicti[term[0]] = 0
			dicti[term[0]] = dicti[term[0]] + int(term[1])
	f.close()
	
f = open('tokens.data', 'wb')
pickle.dump(dicti, f)
f.close()
f = open('tokens.data', 'rb')
dicti = pickle.load(f)
print dicti
