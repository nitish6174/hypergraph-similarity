import json
import numpy as np
import copy

EPSILON = 0.0001

def computeQuality(graph):
	scores = [0]*graph["n"]
	for edge in graph["edges"]:
		for vertex in edge:
			scores[vertex]+=1
	return scores

def getNorm(a,b):
	n = len(a)
	diff = 0
	for i in range(0,n):
		diff += abs(b[i] - a[i])
	return abs(diff)

def computeQualityPageRank(graph):
	l = graph['n']
	scores = computeQuality(graph)

	scoresnp = np.zeros(l)
	scoresnp = [float(scores[i])/sum(scores) for i in range(len(scores))]

	pageRankMatrix = np.zeros((l,l))

	for edge in graph["edges"]:
		for i in range(len(edge)):
			for j in range(i+1, len(edge)):
				pageRankMatrix[edge[i]][edge[j]]+=1
				pageRankMatrix[edge[j]][edge[i]]+=1


	scorestemp = np.zeros((l))
	graphT = np.transpose(pageRankMatrix)
	
	while True:
		rtemp = np.zeros((l))
		rtemp += np.matmul(graphT, scoresnp)
		rnorm = sum(rtemp)
		rtemp /= rnorm
		# print(r)
		# print(rtemp)
		if getNorm(scoresnp,rtemp) < EPSILON:
			break
		scoresnp = copy.deepcopy(rtemp)


	return rtemp


def computeScore(quality1, quality2, n, m):
	qualityIndices1 = sorted(range(len(quality1)), key=lambda k: quality1[k])
	qualityIndices2 = sorted(range(len(quality2)), key=lambda k: quality2[k])

	# print quality1
	# print quality2
	# print qualityIndices1
	# print qualityIndices2

	l = len(quality1)	
	value = 0.0
	for vertex in range(l):
		value +=(float((quality1[vertex]+quality2[vertex])) * (qualityIndices1[vertex]-qualityIndices2[vertex])**2/2)

	value = value*12/(float(l)*(l**2 -1))

	return 1 - value

if __name__ == '__main__':
	with open("data/generated_hypergraphs.json") as f:
		graphs = json.load(f)

	l = len(graphs)
	quality = [[0]]*l

	for i in range(l):
		quality[i] = computeQualityPageRank(graphs[i])


	for i in range(l):
		for j in range(i+1,l):
			print str(graphs[i]["label"]) + " " + str(graphs[j]["label"]) +" " + str(computeScore(quality[i], quality[j], len(graphs[i]['edges']), len(graphs[j]['edges'])))