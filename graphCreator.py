"""
My module for creating graphs
"""

import networkx as nx

def randomGraph(nodes, edges):
    """
    Creates and returns a graph by randomly connecting nodes.
    nodes is the number of nodes and edges is the number of edges.
    """
    g = nx.gnm_random_graph(nodes, edges)
    return g


def prefAttachmentGraph(nodes,edges):
    """Creates and returns a random graph using Barabási-Albert preferential attachment model.
    edges = number of edges to attach from a new node to existing nodes"""
    g = nx.barabasi_albert_graph(nodes,edges)
    return g


def clusterGraph(nodes,edges,p):
    """Holme and Kim algorithm for growing graphs with powerlaw degree distribution and approximate average clustering.
    p is a ptobability of adding a triangle after adding a random edge.
    edges = number of random edges to add for each new node
    https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.generators.random_graphs.powerlaw_cluster_graph.html#networkx.generators.random_graphs.powerlaw_cluster_graph
    """
    g = nx.powerlaw_cluster_graph(nodes,edges,p)
    return g


def karateClubGraph():
    """Returns the karate club graph."""
    g = nx.karate_club_graph()
    return g


def productionNetworkGraph(x):    # where x is the minimal number of orders in which two machines are both used, to get an edge between those machines
    GRAPH_FILE_PATH = "resources/productionNetwork.txt"

    machineToNode = {}
    orderWithMachines = {}
    nextID = 0

    edgeCounter = {}
    with open(GRAPH_FILE_PATH) as f:
        lines = f.read().splitlines()
        for line in lines:
            formated = line.split("\t")
            order = int(formated[0])
            machine = int(formated[1])

            if machine not in machineToNode.keys():
                machineToNode[machine] = nextID
                nextID += 1

            if order not in orderWithMachines.keys():
                orderWithMachines[order] = []

            orderWithMachines[order].append(machine)

    graph = nx.Graph()

    for node in machineToNode.values():
        graph.add_node(node)

    for order in orderWithMachines.keys():
        for machineA in orderWithMachines[order]:
            for machineB in orderWithMachines[order]:
                if machineA < machineB:  # and machineA != machineB
                    edge = (machineToNode[machineA], machineToNode[machineB])
                    if edge not in edgeCounter.keys():
                        edgeCounter[edge] = 1
                    else:
                        edgeCounter[edge] += 1

    for edge in edgeCounter.keys():
        if edgeCounter[edge] >= x:
            graph.add_edge(edge[0], edge[1])

    return graph
