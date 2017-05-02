from dataset import Dataset
import math
import matplotlib.pyplot as plt


dset = Dataset("resources/productionNetwork.txt")

pairCounter = dset.getPairCounts()  # counts of the number of pairs of machines (how often an order goes from one machine to the next)

all_machines = dset.listOfMachines  # list of all machines

for i in all_machines:
    for j in all_machines:
        if (i, j) not in pairCounter:   # if there is no such pair, add 0
            pairCounter[(i, j)] = 0


def getSumOut(pairscount, i):
    """
    returns the sum of all the pairs going from i to k (for outgoing probs)
    """
    count = 0
    for k in all_machines:
        count += pairscount[(i,k)]
    return count


def getSumIn(pairscount, j):
    """
    returns the sum of all pairs coming from i to k (incoming probs)
    """
    count = 0
    for k in all_machines:
        count += pairscount[(k,j)]
    return count


outgoingProbs = {}   # outgoing probabilities (p that j follows after i)
for i in all_machines:
    suma = getSumOut(pairCounter, i)
    for j in all_machines:
        if suma != 0:
            p = pairCounter[(i,j)]/suma
            outgoingProbs[(i, j)] = p
        else:
            outgoingProbs[(i, j)] = "none"   # no outgoing probability (always last machine)

incomingProbs = {}  # incoming probabilities (p that i precedes j)
for j in all_machines:
    suma = getSumIn(pairCounter, j)
    for i in all_machines:
        if suma != 0:
            p = pairCounter[(i, j)] / suma
            incomingProbs[(i, j)] = p
        else:
            incomingProbs[(i, j)] = "none"   # no incoming probability (always first machine)


outgoingEntropies = []
for i in all_machines:
    s = 0.0
    for j in all_machines:
        if outgoingProbs[(i, j)] != "none" and outgoingProbs[(i, j)] > 0:
            s -= outgoingProbs[(i, j)] * math.log(outgoingProbs[(i,j)])
    outgoingEntropies.append(s)

incomingEntropies = []
for j in all_machines:
    s = 0.0
    for i in all_machines:
        if incomingProbs[(i, j)] != "none" and incomingProbs[(i, j)] > 0:
            s -= incomingProbs[(i, j)] * math.log(incomingProbs[(i, j)])
    incomingEntropies.append(s)



# print(outgoingEntropies)
# print(incomingEntropies)



############################################ plotting the entropies (same as with ptimes)

clist = [21, 21, 22, 22, 22, 21, 21, 22, 22, 22, 21, 21, 21, 21, 22, 21, 21, 21, 21, 21, 22, 21, 21, 21, 22, 22, 22, 22, 22, 21, 21, 21, 21, 22, 22, 22, 21, 22, 22, 22, 22, 22, 22, 22, 22, 21, 22, 22, 22, 22, 22]
entropies = incomingEntropies
print(entropies)

z = list(zip(entropies, clist))
changed = {} #keys are entropies, values are number of machines with these entropies
notchanged = {}

for i in z: #change of CN
    entropy = i[0]
    cnum = i[1]
    entropy = int(entropy * 5)
    if cnum == 21:
        if entropy not in changed:
            changed[entropy] = 1
        else:
            changed[entropy] += 1
print(changed)

for i in z: #no change of CN
    entropy = i[0]
    cnum = i[1]
    entropy = int(entropy * 5)
    if cnum == 22:
        if entropy not in notchanged:
            notchanged[entropy] = 1
        else:
            notchanged[entropy] += 1


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
plt.ylabel('Number of nodes')
plt.xlabel('Entropies * 5')
plt.title('Correlation between number of important nodes (machines) and incoming entropies for all machines')
plt.show()