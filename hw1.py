
import pandas as pd
import time
import re
import math
start=time.clock()
import re
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords 
data = pd.read_csv("actual.data" , header=None, \
                    delimiter="\t", quoting=3)
data.shape

fp=open("actual.data")
sentencetest=[]
last=[]
for para in fp:
	last.append(para[:2])
	sentencetest.append(para)

def bagofwords(initial):
   	new = BeautifulSoup(initial,"html.parser").get_text() 
   	nopunc = re.sub("[^a-zA-Z]", " ", new)
	words = nopunc.lower().split() 
	sw = set(stopwords.words("english"))  
	imp = [w for w in words if not w in sw]  
	return( " ".join( imp ))  

no_of_reviews = data[1].size
finalreview = []
for i in xrange (0, no_of_reviews):
   if ( (i+1) % 1 == 0):
      finalreview.append(bagofwords(data[1][i]))
            
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(analyzer = "word",   
                             tokenizer = None,    
                             preprocessor = None, 
                             stop_words = None,
                             max_features = 5000) 
train_data_features = vectorizer.fit_transform(finalreview)
train_data_features = train_data_features.toarray()                           
print train_data_features.shape

vocab = vectorizer.get_feature_names()
print type(vocab)
print len(vocab)
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
def sentencesreview( review, tokenizer ):
    remove_stopwords=False
    raw_sentences = tokenizer.tokenize(review.strip())
    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            sentences.append( bagofwords( raw_sentence))
    return sentences
end=time.clock()

print "The TIME BEFORE SENTENCES"
print end-start
sentences = [0 for x in range(18506)]
i=0
print "Parsing sentences from unlabeled set"
print len(data[1])
i=0
max_num=0
count=0
for review in data[1]:
	'''print str(i)+review
	print "\n--------\n"
	print review_to_sentences(review, tokenizer)
	print "\n \n \n \n"'''
	sentences[i] = sentencesreview(review, tokenizer)
	count = len(re.findall(r'\w+', str(sentences[i])))
	#print count
	if max_num<count:
		max_num=count
	i+=1

end=time.clock()
print "The TIME BEFORE VEC"
print end-start
print "The max is"
print max_num

l=0
fw=open("vector.data","r+")
vec = [[0 for y in range(5001)] for x in range(18506)] 
vectest= [[0 for y in range(5000)] for x in range(18506)] 
indextrain=[[9000 for y in range(1084)] for x in range(18506)] 
indextest=[[8000 for y in range(1084)] for x in range(18506)] 
end=time.clock()
po=0
print "The TIME FOR VEC initialization"
print end-start
for x in range(len(vec)):
	strsent=str(sentences[x])
	po=0
	#print "POOOOOO"+str(x)
	for y in range(len(vec[0])):
		if y==5000:
			vec[x][y]=last[x]
		else:
			word=vocab[y]
			if word in strsent:
				vec[x][y]=strsent.count(word)
				indextrain[x][po]=y
				#print indextrain[x][po]
				po+=1
		
	
	
end=time.clock()
print "The TIME AFTER TRAIN"
print end-start
fw = open("format1.data","r+")

pot=0
	
for x in range(len(vectest)):
	strsent=str(sentencetest[x])
	pot=0
	#print "POTTTTTTTTT" +str(x)
	for y in range(len(vectest[0])):
		word=vocab[y]
		if word in strsent:
			vectest[x][y]=strsent.count(word)
			indextest[x][pot]=y
			#print indextest[x][pot]
			pot+=1
			#print "in count"
		#print vectest[x][y]
	

	

end=time.clock()
print "THE TIME AFTER VEC"
print end-start
fir=0
comm=[]
simvec = [[0 for y in range(18506)] for x in range(18506)] 
for i in range(len(vectest)):
	for  j in range(len(vec)-1):
		#print "i	"+str(i)+"	j	"+str(j)
		distance=0
		comm=list(set(indextest[i])&set(indextrain[j]))
		for l in range(len(comm)):
			k=comm[l]
			#print "Iiiiiiioioioioioioioioioioioioioioioioioioioioioioioioioio"
			#print str(l)+"of"+str(len(comm))
			distance += pow((vectest[i][k] - vec[j][k]), 2)
		simvec[i][j]=math.sqrt(distance)
		#print str(j)+"of"+str(len(vec))
		#print simvec[i][j]
	#maxsim=simvec[i].index(max(simvec[i]))
	
	
	
	
	ss=simvec[i]
	ss=map(int,ss)
	#print max(ss)
	finalinput= ss.index(max(ss))
	#ss.index(max(ss))
	#print "THE FINAL PREDICTION IS **************************"
	#print last[finalinput]
	fw.write(str(last[finalinput]))
	if fir==1:
		fw.write("\n")
	fir=1
	print i

end=time.clock()
print end-start



	
	
	
	
	