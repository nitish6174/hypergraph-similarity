import json
import networkx as nx
import matplotlib.pyplot as plt

def main():
	# import data
	with open('data/generated_hypergraphs.json') as data_file:
		data=json.load(data_file)

	for i in range(len(data)):
		visualize_hypergraph(data[i],i)

def visualize_hypergraph(hypergraph,instance):
	B = nx.Graph()
	node_list=range(hypergraph['n'])
	edge_list=range(len(hypergraph['edges']))
	for i in edge_list:
		edge_list[i] = -edge_list[i]-1

	# add nodes
	B.add_nodes_from(node_list, bipartite=0)
	B.add_nodes_from(edge_list, bipartite=1)

	# add edges
	for i in edge_list:
		for j in hypergraph['edges'][-i-1]:
			B.add_edges_from([(j,i)])

	# Separate by group
	l, r = nx.bipartite.sets(B)
	pos = {}

	# Update position for node from each group
	pos.update((node, (1, index)) for index, node in enumerate(l))
	pos.update((node, (2, index)) for index, node in enumerate(r))

	nx.draw(B, pos=pos)
	# plt.show()

	# save graph
	plt.savefig('graphs/n'+str(hypergraph['n'])+'i'+str(instance)+'.png',dpi=500)

if __name__ == '__main__':
    main()
