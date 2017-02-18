import graphCreator
import chromaticNumber

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


PARAMETERS = list(range(5, 100, 5))
NUMBER_OF_NODES = 51

colors = []
for parameter in PARAMETERS:
    graph = graphCreator.productionNetworkGraph(parameter)
    colors += chromaticNumber.getChangeColors(graph)

x = [[parameter] * NUMBER_OF_NODES for parameter in PARAMETERS]
y = list(range(NUMBER_OF_NODES)) * len(PARAMETERS)

plt.scatter(x, y, c=colors, s=30.0, edgecolors='face')

blue = mpatches.Patch(color='#5555ff', label='The chromatic number reduced')
orange = mpatches.Patch(color='#ff9a00', label='The chromatic number did not change')
red = mpatches.Patch(color='#ff0000', label='The chromatic number changed differently ')

plt.legend(handles=[blue, orange, red])
plt.ylabel('Node ID')
plt.xlabel('Parameter')
plt.show()
