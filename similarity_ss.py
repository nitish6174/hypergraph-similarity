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

def computeQualityPageRank(graph, scores):
	l = graph['n']

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

def computeQualityEdges(graph, quality, scores):
	length = len(graph['edges'])
	qualityEdges = [0]*length

	for i in range(len(graph['edges'])): 
		for j in range(len(graph['edges'][i])):
			qualityEdges[i]+= float(quality[graph['edges'][i][j]])/scores[graph['edges'][i][j]]

	return qualityEdges


def computeScore(quality1, quality2, n, m):
	return 0
	


if __name__ == '__main__':
	with open("data/generated_hypergraphs.json") as f:
		graphs = json.load(f)

	l = len(graphs)
	quality = [[0]]*l
	qualityEdges = [[0]]*l 

	for i in range(l):
		scores = computeQuality(graphs[i])
		quality[i] = computeQualityPageRank(graphs[i], scores)
		qualityEdges[i] = computeQualityEdges(graphs[i], quality[i], scores)

	print quality
	print qualityEdges


	for i in range(l):
		for j in range(i+1,l):
			print str(graphs[i]["label"]) + " " + str(graphs[j]["label"]) +" " + str(computeScore(quality[i], quality[j], len(graphs[i]['edges']), len(graphs[j]['edges'])))