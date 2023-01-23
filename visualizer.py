import json
import networkx as nx
import matplotlib.pyplot as plt

urlData = json.load(open("urls.txt",'r'))
data = [(k,v) for k,v in urlData.items()]

Graph = nx.DiGraph()
Graph.add_edges_from(data)
nx.draw(Graph,with_labels = True)

plt.show()

