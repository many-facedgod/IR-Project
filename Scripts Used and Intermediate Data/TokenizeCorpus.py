import re
import nltk
import string
from nltk import PorterStemmer

for k in range(1400):
	f = open('yet_new_corpus1/'+str(k+1)+'.txt', 'r')
	text = f.read()
	f.close()
	tokens = nltk.word_tokenize(text)
	#To remove the tokens that are punctuation marks
	tokens = filter(lambda word: word not in string.punctuation, tokens)
	f = open('Tokens/'+str(k)+'.txt', 'w')
	#dictionary of all the tokens with the frequency of their occurrence in the document
	finalTok = {}
	for i in tokens:
		#To remove trailing 's
		if i.endswith("'s"):
			i = i[:len(i)-2]
		#To remove any stray '/' around the words
		i = i.strip('/')
		#To remove stray punctuation marks around the words
		for p in string.punctuation:
			i = i.strip(p)
		if len(i)==0:
			continue
		#To handle hyphenated words (For eg: boundary-layer)
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
		#To remove '.' in the tokens (For eg: in abbreviations like m.i.t.)
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
	#To save the tokens of a document along with their frquency of occurrence in a text file
	for i in finalTok:
		f.write(i+" "+str(finalTok[i]))
		if i not in tok:
			tok.append(i)
		f.write('\n')
	f.close()


