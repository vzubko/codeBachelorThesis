import matplotlib.pyplot as plt
import graphCreator
import chromaticNumber
import networkx as nx
import matplotlib.patches as mpatches
import random

def getClusteringList(graph):
    clusterList = []
    for node in range(len(graph.nodes())):
        cluster = nx.clustering(graph,node)
        clusterList.append(cluster)
    return clusterList

def getDegreeList(graph):
    degrees = graph.degree()
    degreeList = []
    for node in range(len(graph.nodes())):
        degreeList.append(degrees[node])
    return degreeList



x = []
y = []
c = []
for i in range(1):
    print("graph", i)
    g = graphCreator.clusterGraph(100, 10, 0.3)
    x += getDegreeList(g)
    y += getClusteringList(g)
    c += chromaticNumber.getChangeColors(g)


moved_x = [v - 0.2 + 0.4 * random.random() for v in x]

plt.scatter(moved_x, y, c=c, s=30.0,edgecolors='face', alpha = 0.6)
blue = mpatches.Patch(color='#5555ff', label='The chromatic number reduced')
orange = mpatches.Patch(color='#ff9a00', label='The chromatic number did not change')
red = mpatches.Patch(color='#ff0000', label='The chromatic number changed differently ')
plt.legend(handles=[blue,orange,red])
plt.title('Correlation between change in chromatic number and clustering coefficient and degree')
plt.ylabel('Clustering coefficient')
plt.xlabel('Degree')
plt.show()
