import graphCreator
import chromaticNumber
import networkx as nx

import matplotlib.pyplot as plt


graph = graphCreator.randomGraph(8, 25)

# bc = nx.betweenness_centrality(graph)
# print(bc)

def getListOfBCvalues(graph):
    bcList = []
    bcValues = nx.betweenness_centrality(graph)
    for bcValue in bcValues.values():
        bcList.append(bcValue)
    return bcList

def getNodesOfSameBC(graph, bcValue):
    bcList = getListOfBCvalues(graph)
    sameBcValueNodes = []
    for node in range(len(bcList)):
        if bcList[node] == int(bcValue):
            sameBcValueNodes.append(node)
    return sameBcValueNodes

def getCnumberBC(graph,listOfNodes):
    chromaticList = []
    for node in range(len(listOfNodes)):
        cNumber = chromaticNumber.getCNumberWithoutNodes(graph, [listOfNodes[node]])
        chromaticList.append(cNumber)
    return chromaticList

def sortChanges(graph, bcValue, originalChr):
    chromaticList = getCnumberBC(graph,getNodesOfSameBC(graph, bcValue))
    reduced = 0
    stayed = 0
    other = 0
    for cnumber in chromaticList:
        if cnumber == originalChr - 1:
            reduced += 1
        elif cnumber == originalChr:
            stayed += 1
        else:
            other += 1
    return reduced, stayed, other


def myrange(upto, offset):
    c = offset
    l = []
    while c < upto:
        l.append(c)
        c += 1
    return l


def bcStatistics(graph, maxBcValue):
    originalChr = chromaticNumber.getChromaticNumber(graph)
    reduced = []
    stayed = []
    other = []
    for degree in range(maxBcValue+1):
        a,b,c = sortChanges(graph,bcValue,originalChr)
        reduced.append(a)
        stayed.append(b)
        other.append(c)
    plt.bar(myrange(maxBcValue + 0.5, -0.2), reduced, width=0.2, color='green')
    plt.bar(myrange(maxBcValue + 0.5, 0), stayed, width=0.2, color='yellow')
    plt.bar(myrange(maxBcValue + 0.5, 0.2), other, width=0.2, color='red')
    plt.gca().set_xticks(range(maxBcValue + 1))
    plt.ylabel('Number of nodes')
    plt.xlabel('Betweenness Centrality')
    plt.title('Sort changes in chromatic number upon deletion of set of nodes of same betweenness centrality')
    plt.show()


print(bcStatistics(graph,1))