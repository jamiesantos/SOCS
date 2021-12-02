# FFR120 Homework 4
# Problem 13.2: Patterns in evolutionary games
# Author: Jamie Santos
# Date: 12/2/21

import numpy as np
import random
from math import sqrt
from matplotlib import pyplot as plt
from prisoner import Prisoner

# Initialize parameters
N = 7			# Number of rounds
T = 0			# Sentence for single defector
R = 0.5			# Both cooperate 
P = 1			# Both defect
S = 1.5			# Sentence for single cooperator
m = 6			# Turns until accomplice becomes traitor
L = 10			# Lattice size
mu = 0			# Probability of mutation
timeSteps = 1

#nValues = np.arange(0,N+1,1)
nValues = [0,N]

# Play N set of rounds between two prisoners
def single_game(n, m):
	totalSentence = 0
 
	p1 = Prisoner()
	p2 = Prisoner()
   
	for rnd in range(N):
		# Prisoners make a choice based off n/m values
		p2.strategize(p1,rnd,m)
		p1.strategize(p2,rnd,n)
   
		# Track the last move each prisoner made
		p1.track_opponent(p2.strategy)
		p2.track_opponent(p1.strategy)

		totalSentence += p1.get_sentence(T,R,P,S,p2)

	return totalSentence

# Play a game against each von Neumann neighbor 
def play_neighbors(row,column,latticeStrats):
	totalScore = 0

	n = latticeStrats[row][column]

	# Up
	if row == 0:
		m = latticeStrats[-1][column]
	else:
		m = latticeStrats[row - 1][column]
	totalScore += single_game(n, m) 

	# Down
	if row == L - 1:
		m = latticeStrats[0][column]
	else:
		m = latticeStrats[row + 1][column]
	totalScore += single_game(n, m)

	# Left
	if column == 0:
		m = latticeStrats[row][-1]
	else:
		m = latticeStrats[row][column - 1]
	totalScore += single_game(n, m)

	# Right
	if column == L - 1:
		m = latticeStrats[row][0]
	else:
		m = latticeStrats[row][column + 1]
	totalScore += single_game(n, m)

	return totalScore

# Initialize a lattice of stategies
#latticeStrats = [[random.choice(nValues) for item in np.zeros(L)] for line in np.zeros(L)]

# Implant a single defector in the center
latticeStrats = [[random.choice(nValues) for item in np.zeros(L)] for line in np.zeros(L)]

# Initialize a lattice of scores
latticeScores = np.zeros((L,L))

# Run a simulation for number of timeSteps over an LxL lattice of prisoners
for t in range(timeSteps):

	#### COMPETE ####
	for row in range(L):
		for column in range(L):
			latticeScores[row][column] = play_neighbors(row,column,latticeStrats)

	#### REVISE ####
	

	#### MUTATE ####

# Plot the heatmap of total prison sentences per person
plt.figure()
plt.imshow(latticeScores,origin='lower', cmap='spring', interpolation='nearest')
plt.title('Years in Prison')
plt.colorbar()
plt.show()
