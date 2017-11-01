import json

def findNumCommonEdges(EdgeList1, EdgeList2):
	# return number of common edges between two edge lists
	count = 0
	# sort all edge lists
	for i in range(len(EdgeList1)):
		EdgeList1[i]=sorted(EdgeList1[i])

	for i in range(len(EdgeList2)):
		EdgeList2[i]=sorted(EdgeList2[i])

	# find common edges
	for edge1 in EdgeList1:
		for edge2 in EdgeList2:
			if edge1 == edge2:
				count = count + 1
				break

	return count

def findVertices(EdgeList):
	# return list of vertices in sorted order
	allVertices = []
	# concatenate all edge lists
	for edge in EdgeList:
		allVertices = allVertices + edge

	uniqueVertices = sorted(list(set(allVertices)))

	return uniqueVertices

def findNumCommonVertices(VertexList1, VertexList2):
	# returns number of common vertices in both vertex list
	count = 0
	for vertex1 in VertexList1:
		for vertex2 in VertexList2:
			if vertex1 == vertex2:
				count = count + 1
				break

	return count

def veoSimilarity(graph1,graph2):
	numEdges1 = len(graph1['edges'])
	numEdges2 = len(graph2['edges'])
	numCommonEdges = findNumCommonEdges(graph1['edges'],graph2['edges'])
	
	VertexList1= findVertices(graph1['edges'])
	VertexList2 = findVertices(graph2['edges'])
	numVertices1 = len(VertexList1)
	numVertices2 = len(VertexList2)
	numCommonVertices = findNumCommonVertices(VertexList1, VertexList2)

	veoScore = 2.0 * (numCommonVertices + numCommonEdges) / (numVertices1 + numVertices2 + numEdges1 + numEdges2)

	return [numEdges1, numEdges2, numCommonEdges, numVertices1, numVertices2, numCommonVertices, veoScore]


if __name__ == '__main__':
	with open("data/generated_hypergraphs.json") as f:
		graphs = json.load(f)

	print str("Graph1"+"\t"+"graph2"+"\t"+"Veo Score"+"\t"+"numEdges1"+"\t"+"numEdges2"+"\t"+"numCommonEdges"+"\t"+"numVertices1"+"\t"+"numVertices2"+"\t"+"numCommonVertices")

	for i in range(len(graphs)):
		for j in range(i+1,len(graphs)):
			numEdges1, numEdges2, numCommonEdges, numVertices1, numVertices2, numCommonVertices, veoScore = veoSimilarity(graphs[i],graphs[j])

			print str(str(graphs[i]['label'])+"\t"+str(graphs[j]['label'])+"\t"+str("{0:.2f}".format(veoScore))+"\t\t"+str(numEdges1)+"\t\t"+str(numEdges2)+"\t\t"+str(numCommonEdges)+"\t\t"+str(numVertices1)+"\t\t"+str(numVertices2)+"\t\t"+str(numCommonVertices))
