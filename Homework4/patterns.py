# FFR120 Homework 4
# Problem 13.2: Patterns in evolutionary games
# Author: Jamie Santos
# Date: 12/2/21

import numpy as np
import random
from random import randrange
from math import sqrt
from matplotlib import pyplot as plt
from prisoner import Prisoner

# Initialize parameters
N = 7			# Number of rounds
T = 0			# Sentence for single defector
R = 0.82		# Both cooperate 
P = 1			# Both defect
S = 1.5			# Sentence for single cooperator
m = 6			# Turns until accomplice becomes traitor
L = 30			# Lattice size
mu = 0.01		# Probability of mutation
timeSteps = 200

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

# Check neighbors for lowest sentences and steal their strategy
def revise_strategy(row,column,latticeStrats,latticeScores):
	newScore = latticeScores[row][column]
	newStrategy = latticeStrats[row][column]	# Assign current strategy first
	tieRow = []
	tieColumn = []
	tieStrats = []

	# Up
	if row == 0:
		tieColumn,tieRow,newScore,newStrategy = track_scores(
			-1,column,newScore,newStrategy,latticeStrats,latticeScores,tieRow,tieColumn)
	else:
		tieColumn,tieRow,newScore,newStrategy = track_scores(
			row - 1,column,newScore,newStrategy,latticeStrats,latticeScores,tieRow,tieColumn)
	# Down
	if row == L - 1:
		tieColumn,tieRow,newScore,newStrategy = track_scores(
			0,column,newScore,newStrategy,latticeStrats,latticeScores,tieRow,tieColumn)
	else:
		tieColumn,tieRow,newScore,newStrategy = track_scores(
			row + 1,column,newScore,newStrategy,latticeStrats,latticeScores,tieRow,tieColumn)
	# Left
	if column == 0:
		tieColumn,tieRow,newScore,newStrategy = track_scores(
			row,-1,newScore,newStrategy,latticeStrats,latticeScores,tieRow,tieColumn)
	else:
		tieColumn,tieRow,newScore,newStrategy = track_scores(
			row,column - 1,newScore,newStrategy,latticeStrats,latticeScores,tieRow,tieColumn)

	# Right
	if column == L - 1:
		tieColumn,tieRow,newScore,newStrategy = track_scores(
			row,0,newScore,newStrategy,latticeStrats,latticeScores,tieRow,tieColumn)
	else:
		tieColumn,tieRow,newScore,newStrategy = track_scores(
			row,column + 1,newScore,newStrategy,latticeStrats,latticeScores,tieRow,tieColumn)

	# Check the ties
	if tieRow != []:
		randI = randrange(len(tieRow))
		newStrategy = latticeStrats[tieRow[randI]][tieColumn[randI]]

	return newStrategy

def track_scores(checkRow,checkColumn,newScore,newStrategy,latticeStrats,latticeScores,tieRow,tieColumn):
	otherScore = latticeScores[checkRow][checkColumn]

	if otherScore < newScore:
		newScore = otherScore
		newStrategy = latticeStrats[checkRow][checkColumn]
		tieRow = []
		tieColumn = []
	elif otherScore == newScore:
		tieRow.append(checkRow)
		tieColumn.append(checkColumn)

	return tieColumn,tieRow,newScore,newStrategy


#######################
# Initialize lattices #
#######################

#latticeStrats = [[random.choice(nValues) for item in np.zeros(L)] for line in np.zeros(L)]

latticeStrats = np.zeros((L,L))

#latticeiStrats[int(round(L/2))][int(round(L/2))] = 0 	# Implant a single defector in the center
cluster = np.arange(14,17,1) 		# Implant a cluster of defectors in the center
for i in range(len(cluster)):
	for j in range(len(cluster)):
		latticeStrats[cluster[i]][cluster[j]] = N

# Initialize a lattice of scores
latticeScores = np.zeros((L,L))


# Run a simulation for number of timeSteps over an LxL lattice of prisoners
for t in range(timeSteps):

	#### COMPETE ####
	for row in range(L):
		for column in range(L):
			latticeScores[row][column] = play_neighbors(row,column,latticeStrats)
		
	#### REVISE ####
	latticeStratsTemp = np.zeros((L,L))
	print(latticeStratsTemp)
	for row in range(L):
		for column in range(L):
			latticeStratsTemp[row][column] = revise_strategy(row,column,latticeStrats,latticeScores)	
	print(" ")
	print(latticeStratsTemp)
	print(" ")
	latticeStrats = latticeStratsTemp.copy()

	#### MUTATE ####
	for row in range(L):
		for column in range(L):
			if random.uniform(0,1) < mu:
				latticeStrats[row][column] = random.choice(nValues)
	
#	print(latticeScores)
#	print(latticeStrats)
#	print("  ")

# Plot the heatmap of total prison sentences per person
plt.figure()
#plt.imshow(latticeStrats,origin='lower', cmap='gist_rainbow', interpolation='nearest')
plt.imshow(latticeStrats,origin='lower', cmap='cool', interpolation='nearest')
plt.title('Strategies')
plt.colorbar()
plt.show()
