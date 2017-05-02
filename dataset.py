import networkx as nx

class ProcessingStep(object):
    """
    a 'container' for a processing step
    """
    def __init__(self, machine, timestamp, orderid):
        self.machine = machine
        self.timestamp = timestamp
        self.orderid = orderid



class Dataset(object):
    """
    contains funcitions for working with a dataset
    """
    def __init__(self, filename):
        self.filename = filename
        self.loadData()
        self.createOrders()


    def loadData(self):
        """
        loads data from a file and gets processing steps for each order
        """
        machineToNode = {}
        self.listOfMachines = []
        nextID = 0
        self.processingSteps = []
        with open(self.filename) as f:
            lines = f.read().splitlines()
            for line in lines:
                formatted = line.split("\t")
                order = int(formatted[0])
                machine = int(formatted[1])
                timestamp = float(formatted[2])
                if machine not in machineToNode:    # normalizing machines according to the nodes (1,2,3... instead of 1,34,2...)
                    machineToNode[machine] = nextID
                    nextID +=1
                    self.listOfMachines.append(machineToNode[machine])  # normalized list of all machines

                pstep = ProcessingStep(machineToNode[machine], timestamp, order)
                self.processingSteps.append(pstep)


    def getPairCounts(self):
        """
        :return: dictionary with counts of edges/ numbers of pairs (order goes from one machine to the next)
        """
        paircounts = {} # {(2,3) : 4}
        for order in self.ordersDict.values():
            for pstepA in order.psteps:
                for pstepB in order.psteps:
                    if pstepA.machine < pstepB.machine:  # and machineA != machineB, for just taking one pair, no repetitions
                        edge = (pstepA.machine, pstepB.machine)
                        if edge not in paircounts.keys():
                            paircounts[edge] = 1
                        else:
                            paircounts[edge] += 1
        return paircounts


    def getGraph(self, x):
        """
        :param x: the minimal number of orders in which two machines are both used, to get an edge between those machines
        :return: the graph of production network
        """
        graph = nx.Graph()
        edgeCounter = self.getPairCounts()

        for node in self.listOfMachines:
            graph.add_node(node)

        for edge in edgeCounter.keys():
            if edgeCounter[edge] >= x:
                graph.add_edge(edge[0], edge[1])
        return graph


    def createOrders(self):
        """
        creates a dictionary with orders as keys and list of processing steps for this order as values
        """
        self.ordersDict = {}
        for pstep in self.processingSteps:
            if pstep.orderid not in self.ordersDict:
                self.ordersDict[pstep.orderid] = Order()
            self.ordersDict[pstep.orderid].addProcessingStep(pstep)



class Order(object):
    """
    a 'container' for an order with processing steps
    """
    def __init__(self):
        self.psteps = [] #list of processing steps for this order

    def addProcessingStep(self, pstep):
        self.psteps.append(pstep)

    def sortByTimes(self):
        self.psteps.sort(key=lambda pstep : pstep.timestamp)
