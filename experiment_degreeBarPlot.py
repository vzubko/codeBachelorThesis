import chromaticNumber
import barPlots
import graphCreator
import matplotlib.pyplot as plt

graph = graphCreator.randomGraph(10,30)
dictionary = graph.degree()

def sortChanges(graph, degree, originalChr):
    """
    Returns three lists that contain the number of nodes, which influenced the change in chromatic number:
    reduced it, left it unchanged, or increased it (in case of error, as the algorithm is not exact).
    """
    chromaticList = barPlots.getCNumberWithoutNodesOfSameValue(graph, barPlots.getNodesWithSameValue(barPlots.getListofValues(dictionary), degree))
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

def myrange(upto, offset):
    c = offset
    l = []
    while c < upto:
        l.append(c)
        c += 1
    return l

def getDegreeStatistics(graph, maxDegree):
    """
    Plots the three bars for each degree, which show the number of nodes of this degree,
    which either influenced the decrease, staying, or increase in chrimatic number
    (all the nodes upon deletion of a particular degree for each degree).
    """
    originalChr = chromaticNumber.getChromaticNumber(len(graph.nodes()),graph.edges())
    reduced = []
    stayed = []
    other = []
    for degree in range(maxDegree+1):
        a,b,c = sortChanges(graph, degree, originalChr)
        reduced.append(a)
        stayed.append(b)
        other.append(c)
    plt.bar(myrange(maxDegree+0.5, -0.2), reduced, width=0.2, color='green')
    plt.bar(myrange(maxDegree+0.5, 0), stayed, width=0.2, color='yellow')
    plt.bar(myrange(maxDegree+0.5, 0.2), other, width=0.2, color='red')
    plt.gca().set_xticks(range(maxDegree + 1))
    plt.ylabel('Number of nodes')
    plt.xlabel('Degree')
    plt.title('Change in chromatic number upon deletion of all the nodes of each degree')
    plt.show()

print("experiment running")
print(getDegreeStatistics(graph,10))
