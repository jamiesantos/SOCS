# FFR120 Homework 4
# Problem 13.1: Prisoner's dilemma with multiple rounds
# Author: Jamie Santos
# Date: 12/1/21


import numpy as np 
from math import sqrt
from matplotlib import pyplot as plt
from prisoner import Prisoner

# Initialize parameters
N = 10			# Number of rounds
T = 0			# Sentence for single defector
R = 0.5			# Both cooperate 
P = 1			# Both defect
S = 1.5			# Sentence for single cooperator
m = 6			# Turns until accomplice becomes traitor
nValues = np.arange(0,N+1,1)

# Play N number of rounds
def multiple_rounds(m, numRounds):
	yearsList1 = []
	yearsList2 = []

	for n in range(len(nValues)):
		totalSentence1 = 0
		totalSentence2 = 0
	
		p1 = Prisoner()
		p2 = Prisoner()
	
		for rnd in range(N):

			# Prisoners make a choice based off n/m values
			p2.strategize(p1,rnd,m)
			p1.strategize(p2,rnd,n)
	
			# Track the last move each prisoner made
			p1.track_opponent(p2.strategy)
			p2.track_opponent(p1.strategy)
	
			totalSentence1 += p1.get_sentence(T,R,P,S,p2)
			totalSentence2 += p2.get_sentence(T,R,P,S,p1)
	
			#print("Sentence1: " + str(totalSentence1))
			#print("Sentence2: " + str(totalSentence2))
		yearsList1.append(totalSentence1)
		yearsList2.append(totalSentence2)

	return yearsList1, yearsList2


# Plot for 1A
yearsList1,yearsList2 = multiple_rounds(m, N)

plt.figure()
plt.scatter(nValues,yearsList1,linewidth = 1, color="blue",label="p1")
plt.xticks(np.arange(min(nValues), max(nValues)+1, 1.0))
plt.ylabel('Years in prison')
plt.xlabel('n')

# Plot for 1B
mValues = nValues
heatMapData = []

for mVal in range(len(mValues)):
	m = mVal
	yearsList1,yearsList2 = multiple_rounds(m, N)
	heatMapData.append(yearsList1)

heatMapData = np.transpose(np.array(heatMapData))

plt.figure()
plt.imshow(heatMapData,origin='lower', cmap='summer', interpolation='nearest')
plt.title('Years in Prison')
plt.xlabel('m')
plt.ylabel('n')
plt.colorbar()
plt.show()
