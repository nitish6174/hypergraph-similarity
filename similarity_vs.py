import json

def computeOutlinks(graph):
	n = graph['n']
	matrix = [[0]*n for i in range(n)]
	for edge in graph['edges']:
		for i in edge:
			for j in edge:
				matrix[i][j]+=1

	print matrix
	return matrix

def computeGamma(matrix):
	n = len(matrix)
	gamma = [[0.]*n for i in range(n)]
	for i in range(n):
		row_sum = sum(matrix[i])
		for j in range(n):
			gamma[i][j] = float(matrix[i][j])/row_sum

	print gamma
	return gamma

def computeSimilarity(gamma1, gamma2):
	n1 = len(gamma1)
	n2 = len(gamma2)
	n = max(n1,n2)
	value = 0
	for i in range(n):
		for j in range(0,i):
			if i >= len(gamma1) or i >= len(gamma2):
				value += 1
			elif gamma1[i][j] == 0 or gamma2[i][j] == 0:
				value += 1
			else: 
				value += abs(gamma1[i][j]-gamma2[i][j])/max(gamma1[i][j], gamma2[i][j])
	value /= n**2/2

	return 1-value		


if __name__ == '__main__':
	with open("data/generated_hypergraphs.json") as f:
		graphs = json.load(f)

	l = len(graphs)
	quality = []

	for i in range(l):
		quality.append(computeGamma(computeOutlinks(graphs[i])))

	for i in range(l):
		for j in range(i+1,l):
			print str(graphs[i]["label"]) + " " + str(graphs[j]["label"]) +" " + str(computeSimilarity(quality[i], quality[j]))