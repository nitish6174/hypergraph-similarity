import json
import numpy as np
import copy

EPSILON = 0.0001
K = 2



def computeQuality(graph):
	scores = [0]*graph["n"]
	for edge in graph["edges"]:
		for vertex in edge:
			scores[vertex]+=1
	return scores

def makeVertexToEdgeMap(vertexToEdgeMap,graph,k):
	edges = graph['edges']

	for i in range(len(edges)):
		for vertex in edges[i]:
			if vertex in vertexToEdgeMap[k]:
				vertexToEdgeMap[k][vertex].append(i)
			else:
				vertexToEdgeMap[k][vertex] = [i]

	return vertexToEdgeMap

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

def makeSequence(graph, vertexToEdgeMap, quality):
	allList = [i for i in range(len(quality))]
	current = np.argmax(quality)
	visited = []
	qualitySorted = sorted(range(len(quality)), key=lambda k: quality[k])
	qualitySorted.reverse()

	while allList:
		visited.append(current)
		allList.remove(current)
		allVerticesAdjacentSet = set()
		for edge in vertexToEdgeMap[current]:
			for vertex in graph['edges'][edge]:
				allVerticesAdjacentSet.add(vertex)

		for i in range(len(qualitySorted)):
			if qualitySorted[i] not in visited:
				current = vertex
				break

		if current in visited:
			if allList:
				maxIndex = allList[0]
				for x in allList:
					if quality[x] > quality[maxIndex]:
						maxIndex = x
				current = maxIndex

	return visited


def computeScore(sequence1, sequence2):
	set1 = set()
	set2 = set()
	strSequence1 = ""
	strSequence2 = ""

	for i in range(len(sequence1)):
		strSequence1 +=str(sequence1[i])
		strSequence2 +=str(sequence2[i])

	for i in range(len(strSequence1) - K + 1):
		subString1 = strSequence1[i:i+K]
		subString2 = strSequence2[i:i+K]
		set1.add(subString1)
		set2.add(subString2)

	return float(len(set1 & set2))/ len(set1 | set2)

if __name__ == '__main__':
	with open("data/generated_hypergraphs.json") as f:
		graphs = json.load(f)

	l = len(graphs)
	vertexToEdgeMap = [dict() for x in range(l)]
	quality = [[0]]*l
	sequences = [[0]]*l

	for i in range(l):
		quality[i] = computeQualityPageRank(graphs[i])
		vertexToEdgeMap = makeVertexToEdgeMap(vertexToEdgeMap, graphs[i],i)
		sequences[i] = makeSequence(graphs[i], vertexToEdgeMap[i], quality[i])

	for i in range(l):
		for j in range(i+1,l):
			print str(graphs[i]["label"]) + " " + str(graphs[j]["label"]) +" " + str(computeScore(sequences[i], sequences[j]))