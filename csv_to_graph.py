import csv
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def visualize(filename):
    df = pd.read_csv(f'{filename}.csv')
    Graphtype = nx.Graph()
    Graph = nx.from_pandas_edgelist(df, create_using=Graphtype)

    pos = nx.spring_layout(Graph,k=12)
    nx.draw(Graph,with_labels= True,node_size=100,font_size=6,alpha = .7,width = .4)

    plt.show()
