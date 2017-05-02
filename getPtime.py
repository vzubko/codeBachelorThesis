from dataset import Dataset
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class MachineStatistics(object):
    def __init__(self):
        self.data = {} # {2: [0.6575, 9.864986, 8.686]} meaning for this machine this is the list of timesItTakesUntilNextMAchine


    def addDifference(self, machine, difference):
        """
        adds differences to the dictionary
        :param machine: a machine
        :param difference: time it takes of an order to go to the next machine
        """
        if machine not in self.data:
            self.data[machine] = [difference]
        else:
            self.data[machine].append(difference)


    def plotStatistics(self, machine):
        """
        plots the processing times of all orders for one machine
        """
        seq = self.data[machine]
        grouped = {}    # keys are normalized differences, values are the number of these differences
        for i in seq:
            i = int(i) # i * 10 means we take 1/10 of a day
            if i not in grouped:
                grouped[i] = 1
            else:
                grouped[i] += 1
        counts = []     # the number of normalized differences for all the order for this machine (i.e number of orders with these differences)
        for k in range(20):
            if k not in grouped:
                count = 0
            else:
                count = grouped[k]
            counts.append(count)

        plt.plot(counts)



    def getPtimeOfAllMachines(self, machines):
        """
        returns list of processing times of all machines: method simple average
        """

        ptimes = []
        for machine in machines:
            if machine in self.data:
                ptime = sum(self.data[machine])/len(self.data[machine])
                ptimes.append(ptime)
            else:
                ptimes.append(0.0)
        return ptimes


    def getPtimeOfAllMachines2(self, machines):
        """
        returns list of processing times of all machines: method get median
        """
        ptimes = []
        for machine in machines:
            if machine in self.data:
                differences = sorted(self.data[machine])
                median = len(differences)//2
                ptime = differences[median]
                ptimes.append(ptime)
            else:
                ptimes.append(0.0)
        return ptimes


def getStatisticsOfDifferences(dataset):
    """
    calculates the differences using data from a dataset and returns it in a dictionary
    """
    mStats = MachineStatistics()
    for order in dataset.ordersDict.values():
        order.sortByTimes()
        for position in range(1, len(order.psteps)):
            delta = order.psteps[position].timestamp - order.psteps[position-1].timestamp
            mStats.addDifference(order.psteps[position-1].machine, delta)
    return mStats



dset = Dataset("resources/productionNetwork.txt")
stats = getStatisticsOfDifferences(dset)
# plotting = stats.plotStatistics(1)
# plotting = stats.plotStatistics(2)
# plotting = stats.plotStatistics(3)
# plotting = stats.plotStatistics(4)
# plotting = stats.plotStatistics(5)
#
# plt.xlabel("Processing time (in days)")
# plt.ylabel("Number of orders")
# plt.title("Processing times of all orders for five machines")
# plt.show()

# chromatic numbers after deletion of each node in a production network graph with parameter = 42
clist = [21, 21, 22, 22, 22, 21, 21, 22, 22, 22, 21, 21, 21, 21, 22, 21, 21, 21, 21, 21, 22, 21, 21, 21, 22, 22, 22, 22, 22, 21, 21, 21, 21, 22, 22, 22, 21, 22, 22, 22, 22, 22, 22, 22, 22, 21, 22, 22, 22, 22, 22]
ptimes = stats.getPtimeOfAllMachines(sorted(dset.listOfMachines))  # using either method 1 or 2
print(ptimes)

z = list(zip(ptimes, clist))
changed = {}    # keys are processing times, values are number of machines with this processing time, contains the machines with ptimes, that change CN
notchanged = {}

for i in z: # getting dictionary with normalized ptimes as keys and number of nodes that change CN as values
    ptime = i[0]
    cnum = i[1]
    ptime = int(ptime)
    if cnum == 21:
        if ptime not in changed:
            changed[ptime] = 1
        else:
            changed[ptime] += 1

for i in z: # getting dictionary with normalized ptimes as keys and number of nodes that don't change CN as values
    ptime = i[0]
    cnum = i[1]
    ptime = int(ptime)
    if cnum == 22:
        if ptime not in notchanged:
            notchanged[ptime] = 1
        else:
            notchanged[ptime] += 1


countschanged = []      # getting the list for plotting, of number of nodes that change CN
countsnotchanged = []   # getting the list for plotting, of number of nodes that do not change CN

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


# bar plotting the number of nodes that change/do not change CN against processing times of machines
plt.bar(myrange(len(countschanged)-0.5, -0.15), countschanged, width=0.2, color='green')
plt.bar(myrange(len(countsnotchanged)-0.5, 0.15), countsnotchanged, width=0.2, color='yellow')
green = mpatches.Patch(color='green', label='The chromatic number reduced')
yellow = mpatches.Patch(color='yellow', label='The chromatic number did not change')
plt.xlabel('Processing time (in days)')
plt.ylabel('Number of nodes (machines)')
plt.title('Correlation between number of important nodes (machines) and processing times for all machines (method 1: simple average)')
plt.show()

#!!!define nodes that change CN upon deletion as important nodes!!!