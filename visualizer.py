import json
import networkx as nx
import matplotlib.pyplot as plt


def visualize():
    urlData = json.load(open("urls.txt",'r'))
    maxUrlSize = 100
    truncatedData = {} #truncate key:values so the urls aren't too long

    for k,v in urlData.items():
        kTrunc = k[:maxUrlSize]
        vTrunc = v[:maxUrlSize]
        truncatedData.update({kTrunc:vTrunc})

        
    data = [(k,v) for k,v in truncatedData.items()]





    Graph = nx.DiGraph()
    Graph.add_edges_from(data)
    pos = nx.spring_layout(Graph,k=12)
    nx.draw(Graph,with_labels= True,node_size=100,font_size=6,arrowsize = 3,alpha = .7,width = .4)

    plt.show()

