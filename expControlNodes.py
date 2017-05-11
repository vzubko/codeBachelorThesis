import graphCreator
import chromaticNumber
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import dataset


dset = dataset.Dataset("resources/productionNetwork.txt")
graph = dset.getGraph(10)

clist = chromaticNumber.getCNumbersWithoutEachNode(graph)
# controlNodes = chromaticNumber.getControlNodes(len(graph.nodes()), graph.edges())

controlNodes = chromaticNumber.getControlDistr(len(graph.nodes()), graph.edges(), 1000)


controlling = controlNodes
print(controlling)

z = list(zip(controlling, clist))
changed = {}
notchanged = {}

for i in z: #change of CN
    value = i[0]
    cnum = i[1]
    value = int(value * 300)
    if cnum == max(clist)-1:
        if value not in changed:
            changed[value] = 1
        else:
            changed[value] += 1
print(changed)

for i in z: #no change of CN
    value = i[0]
    cnum = i[1]
    value = int(value * 300)
    if cnum == max(clist):
        if value not in notchanged:
            notchanged[value] = 1
        else:
            notchanged[value] += 1


countschanged = []
countsnotchanged = []

for i in range(20):
    if i in notchanged:
        countsnotchanged.append(notchanged[i])
    else:
        countsnotchanged.append(0)

    if i in changed:
        countschanged.append(changed[i])
    else:
        countschanged.append(0)


def myrange(upto, offset):
    c = offset
    l = []
    while c < upto:
        l.append(c)
        c += 1
    return l



plt.bar(myrange(len(countschanged)-0.5, -0.15), countschanged, width=0.2, color='green')
plt.bar(myrange(len(countsnotchanged)-0.5, 0.15), countsnotchanged, width=0.2, color='yellow')
green = mpatches.Patch(color='green', label='The chromatic number reduced')
yellow = mpatches.Patch(color='yellow', label='The chromatic number did not change')
plt.xlabel('Control nodes values')
plt.ylabel('Number of nodes (machines)')
plt.title('Correlation between number of important nodes (machines) and control nodes')
plt.show()