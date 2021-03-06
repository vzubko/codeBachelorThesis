"""
My module for calculating chromatic numbers (and changes in the chromatic number)
"""

import networkx as nx
import subprocess
import random

GRAPH_FILE_PATH = "/tmp/graph.txt"
BASE_PATH = "/tmp/"
SOLUTION_PATH = BASE_PATH + "solution.txt"


def greedy(graph,strategy):
    """
    Returns the coloring of a graph using a greedy strategy.
    see https://networkx.github.io/documentation/development/reference/generated/networkx.algorithms.coloring.greedy_color.html
    for possible strategies.
    """
    greedy = nx.greedy_color(graph,strategy)
    return greedy


def chromaticNumberFromColoring(coloring):
    """
    Returns the chromatic number of a coloring.
    coloring should be a list of colors of the nodes, starting with 0.
    """
    return max(coloring) + 1


def getColoringHEA(numberOfNodes, listOfEdges):
    """
    Uses the HEA for coloring.
    numberOfNodes should be the number of nodes in the graph, and listOfEdges should be a list of the edges.
    The nodes are in the range 0, ..., numberOfNodes - 1.
    Returns the coloring of the graph as a list of integers.
    """

    # write graph to file
    with open(GRAPH_FILE_PATH, "w") as f:
        f.write("p edge " + str(numberOfNodes) + " " + str(len(listOfEdges)) + "\n")
        for edge in listOfEdges:
            f.write("e " + str(edge[0]+1) + " " + str(edge[1]+1) + "\n")

    # run algorithm on graph
    subprocess.run(["./HybridEA", GRAPH_FILE_PATH, "-o", BASE_PATH])

    # read coloring
    with open(SOLUTION_PATH, "r") as f:
        numberOfNodes = int(f.readline())
        coloring = []
        for line in f:
            coloring.append(int(line))
        assert len(coloring) == numberOfNodes
        return coloring


def getChromaticNumber(numberOfNodes, listOfEdges):
    """
    returns the chromatic number of a graph using HEA
    """
    coloring = getColoringHEA(numberOfNodes, listOfEdges)
    c = chromaticNumberFromColoring(coloring)
    return c


def getCNumberWithoutOneNode(graph,node):
    """
    returns the chromatic number of a graph with one node removed
    """
    edgeList = graph.edges()
    nodesList = graph.nodes()
    keepEdges = []
    for edge in range(len(edgeList)):
        if node not in edgeList[edge]:
            keepEdges.append(edgeList[edge])
    c = getColoringHEA(len(nodesList), keepEdges)
    return chromaticNumberFromColoring(c)


def getCNumberWithoutNodes(graph, listOfNodes):
    """
    returns the chromatic number of a graph with the nodes in listOfNodes removed
    """
    edgeList = graph.edges()
    keepEdges = []
    for edge in edgeList:
         if edge[0] not in listOfNodes and edge[1] not in listOfNodes:
            keepEdges.append(edge)
    c = getChromaticNumber(len(graph.nodes()), keepEdges)
    return c


def getCNumbersWithoutEachNode(graph):
    """
    returns list of chromatic numbers after removal of each one node
    """
    chromaticList = []
    nodesList = graph.nodes()
    for node in range(len(nodesList)):
        cNumber = getCNumberWithoutOneNode(graph, node)
        chromaticList.append(cNumber)
    print(chromaticList)
    return chromaticList


def chromaticChangeToColor(originalCN, newCN):
    """
    returns the color depending on how the chromatic number changed
    """
    if newCN == originalCN - 1:
        return '#5555ff'
    elif newCN == originalCN:
        return '#ff9a00'
    else:
        return '#ff0000'


def getChangeColors(graph):
    """
    returns the list of colors of nodes, which change chromatic number upon deletion
    """
    originalChr = getChromaticNumber(len(graph.nodes()),graph.edges())
    print(originalChr)
    colors = [chromaticChangeToColor(originalChr, x) for x in getCNumbersWithoutEachNode(graph)]
    return colors


def getControlNodes(numberOfNodes, listOfEdges):
    """
    Uses the HEA for coloring.
    numberOfNodes should be the number of nodes in the graph, and listOfEdges should be a list of the edges.
    The nodes are in the range 0, ..., numberOfNodes - 1.
    Returns the coloring of the graph as a list of integers.
    """

    # write graph to file
    with open(GRAPH_FILE_PATH, "w") as f:
        for edge in listOfEdges:
            f.write(str(edge[0]) + " " + str(edge[1]) + "\n")
            f.write(str(edge[1]) + " " + str(edge[0]) + "\n")

    # run algorithm on graph
    subprocess.run(["./netctrl-wrapper.sh"])

    with open(SOLUTION_PATH, "r") as f:
        driverNodes = []
        for line in f:
            driverNodes.append(int(line))
        return driverNodes


def getControlDistr(numberOfNodes, listOfEdges, rep):
    prob = [0] * numberOfNodes
    for i in range(rep):
        perm = list(range(numberOfNodes))
        random.shuffle(perm)
        ep = [(perm[a], perm[b]) for (a, b) in listOfEdges]

        dp = getControlNodes(numberOfNodes, ep)
        for e in dp:
            prob[perm.index(e)] += 1/float(rep)
    return prob

































