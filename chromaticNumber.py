"""
My module for calculating chromatic numbers (and changes in the chromatic number)
"""

import networkx as nx
import subprocess

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
    return chromaticList


def getCNumberWithoutNodesOfSameValue(graph, listOfNodes):
    """
    The function does the following:
    1. It computes chromatic number after deletion of all the nodes of the same value.
    2. It does it for each node.
    3. It appends chromatic numbers upon deletion to a list.
    4. Returns the list.
    """
    chromaticList = []
    for node in range(len(listOfNodes)):
        cNumber = chromaticNumber.getCNumberWithoutNodes(graph, [listOfNodes[node]])
        chromaticList.append(cNumber)
    return chromaticList


def sortChanges(graph, value, originalChr):
    """
    Returns three lists that contain the number of nodes, which influenced the change in chromatic number:
    reduced it, left it unchanged, or increased it (in case of error, as the algorithm is not exact).
    """
    chromaticList = getCNumberWithoutNodesOfSameValue(graph, getNodesWithSameValue(getListofValues(dic),value))
    reduced = 0
    stayed = 0
    other = 0
    for cnumber in chromaticList:
        if cnumber == originalChr-1:
            reduced += 1
        elif cnumber == originalChr:
            stayed += 1
        else:
            other += 1
    return reduced, stayed, other


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
    originalChr = getChromaticNumber(len(graph.nodes()),graph.edges())
    colors = [chromaticChangeToColor(originalChr, x) for x in getCNumbersWithoutEachNode(graph)]
    return colors

