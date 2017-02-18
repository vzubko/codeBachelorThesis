"""
The functions necessary for creating bar plots.
"""

import chromaticNumber


def getListofValues(dictionary):
    """
    Returns the list of values (e.g. list of clustering coefficient, degree, or betweenness centrality values).
    Requires dictionary as a parameter, which the algorithms from networkx library returns (e.g. {node:degree}).
    """
    listOfValues = []
    for value in dictionary.values():
        listOfValues.append(value)
    return listOfValues


def getNodesWithHighestValue(listOfValues):
    """
    Returns the list of nodes with the highest value (e.g. highest degree).
    """
    listOfNodesWithHighestValue = []
    maxValue = max(listOfValues)
    for node in range(len(listOfValues)):
        if listOfValues[node] == maxValue:
            listOfNodesWithHighestValue.append(node)
    return listOfNodesWithHighestValue


def getNodesWithSameValue(listOfValues, value):
    """
    Returns the list of nodes with the same value (e.g. same degree).
    """
    listOfNodesWithSameValue = []
    for node in range(len(listOfValues)):
        if listOfValues[node] == value:
            listOfNodesWithSameValue.append(node)
    return listOfNodesWithSameValue


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

