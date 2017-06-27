
import csv
import os
import numpy as np
from sklearn.feature_extraction import DictVectorizer
#from sklearn.metrics.cluster import v_measure_score
from scipy.spatial import distance
from collections import Counter
d={}
final=[[0 for p in range(150)] for q in range(8580)]
with open('1475544942_8895261_input.mat', 'rb') as file:
	for i, line in enumerate(file):
		c = line.split()
		x=0
		while x<(len(c)):
			if (x%2==0):
				if c[x] in d:
					d[c[x]] = d[c[x]]+float(c[x+1])
				else:
					d[c[x]]=float(c[x+1])
				#print("bye")
			x+=1
		
	values=[]
	top= Counter (d)
	for k,v in top.most_common(150):
		values.append(k)
	#print(values)
	
with open('1475544942_8895261_input.mat', 'rb') as f:			
	for z in range(len(values)):
		#print("enter")
		for i, line in enumerate(f):
			c = line.split()
			x=0
			#print len(c)
			while x<(len(c)):
				#print type((c[x]))
				#print type((values[z]))
				#print("in while")
				if (x%2==0):
					if c[x]==values[z]:
						final[i][z]=float(c[x+1])
						#print("end")
				x+=1

	#print(final)					
def kmeans(data, k):
	check=True
	centroids = []
	centroids = getRandomCentroids(data, centroids, k)  
	print("Random centroids done")
	old_centroids = [[] for i in range(k)]
	iterations = 0
	while check:
    #while not shouldStop(oldCentroids, centroids, iterations):
		print("in while")
		old_centroids = centroids
		iterations += 1
		clusters = [[] for i in range(k)]
		calDist(centroids,data,clusters)
		index = 0
		for cluster in clusters:
			old_centroids[index] = centroids[index]
			centroids[index] = np.mean(cluster, axis=0).tolist()
			index += 1
		check=not shouldStop(old_centroids, centroids, iterations)
	#print("done")
	fw=open("out.data","w+")
	for y in range (len(data)):
		if data[y] in clusters[0]:
			fw.write("1")
			fw.write("\n")
		if data[y] in clusters[1]:
			fw.write("2")
			fw.write("\n")
		if data[y] in clusters[2]:
			fw.write("3")
			fw.write("\n")
		if data[y] in clusters[3]:
			fw.write("4")
			fw.write("\n")
		if data[y] in clusters[4]:
			fw.write("5")
			fw.write("\n")	
 		if data[y] in clusters[5]:
			fw.write("6")
			fw.write("\n")
		if data[y] in clusters[6]:
			fw.write("7")
			fw.write("\n")

         
def getRandomCentroids(data, centroids, k):
	
    for cluster in range(0, k):
        centroids.append(data[np.random.randint(0, len(data), size=1)])
    return centroids

def shouldStop(centroids, old_centroids, iterations):
	MAX_ITERATIONS = 1000
	if iterations > MAX_ITERATIONS:
		return True
	return old_centroids == centroids

def calDist(centroids,data,clusters):
	for i in range(len(data)):
		dist=[0 for k in range(7)]
		
		for j in range(len(centroids)):
			
			dist[j]=(distance.euclidean(centroids[j],data[i]))	
		#print(dist)	
		mini=dist.index(min(dist))
			#minclus=j
		clusters[mini].append(data[i])		
			
kmeans(final,7)

#print(v_measure_score(final,))

           


			
