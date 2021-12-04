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

question_4 = False
question_5 = True

# Initialize parameters
N = 7			# Number of rounds
T = 0			# Sentence for single defector
#R = 0.72		# Both cooperate
P = 1			# Both defect
#S = 3			# Sentence for single cooperator
m = 6			# Turns until accomplice becomes traitor
L = 30			# Lattice size
mu = 0.01		# Probability of mutation
timeSteps = 500

nValues = np.arange(0,N+1,1)
#nValues = [0,N]

#rList = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
#sList = [1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5, 2.7]
rList = [0.1, 0.2, 0.3]
sList = [1.1]

# Play N set of rounds between two prisoners
def single_game(n, m, R, S):
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
def play_neighbors(row,column,latticeStrats,R,S):
	totalScore = 0

	n = latticeStrats[row][column]

	# Up
	if row == 0:
		m = latticeStrats[-1][column]
	else:
		m = latticeStrats[row - 1][column]
	totalScore += single_game(n, m, R, S)

	# Down
	if row == L - 1:
		m = latticeStrats[0][column]
	else:
		m = latticeStrats[row + 1][column]
	totalScore += single_game(n, m, R, S)

	# Left
	if column == 0:
		m = latticeStrats[row][-1]
	else:
		m = latticeStrats[row][column - 1]
	totalScore += single_game(n, m, R, S)

	# Right
	if column == L - 1:
		m = latticeStrats[row][0]
	else:
		m = latticeStrats[row][column + 1]
	totalScore += single_game(n, m, R, S)

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

#Random start
latticeStrats = [[random.choice(nValues) for item in np.zeros(L)] for line in np.zeros(L)]

# Clustered start
#latticeStrats = np.zeros((L,L))

#latticeiStrats[int(round(L/2))][int(round(L/2))] = 0	# Implant a single defector in the center
#cluster = np.arange(14,17,1)		# Implant a cluster of defectors in the center
#for i in range(len(cluster)):
#	for j in range(len(cluster)):
#		latticeStrats[cluster[i]][cluster[j]] = N

# Initialize a lattice of scores
latticeScores = np.zeros((L,L))

# Initialize lists to track strategies at each time step
list0 = []
list1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
list7 = []

varSumMatrix = []
for rIndex in range(len(rList)):
	R = rList[rIndex]
	print("R: " + str(R))

	varSumRList = []

	for sIndex in range(len(sList)):
		S = sList[sIndex]
		print("S: " + str(S))
 
		# Run a simulation for number of timeSteps over an LxL lattice of prisoners
		for t in range(timeSteps):
		
			#### COMPETE ####
			for row in range(L):
				for column in range(L):
					latticeScores[row][column] = play_neighbors(row,column,latticeStrats,R,S)
				
			#### REVISE ####
			latticeStratsTemp = np.zeros((L,L))
			for row in range(L):
				for column in range(L):
					latticeStratsTemp[row][column] = revise_strategy(row,column,latticeStrats,latticeScores)	
			latticeStrats = latticeStratsTemp.copy()
		
			#### MUTATE ####
			for row in range(L):
				for column in range(L):
					if random.uniform(0,1) < mu:
						latticeStrats[row][column] = random.choice(nValues)
		
			if question_4 == True:
				### TRACK STRATEGIES ###
				list0.append(sum(list(x).count(0) for x in latticeStrats))
				list1.append(sum(list(x).count(1) for x in latticeStrats))
				list2.append(sum(list(x).count(2) for x in latticeStrats))
				list3.append(sum(list(x).count(3) for x in latticeStrats))
				list4.append(sum(list(x).count(4) for x in latticeStrats))
				list5.append(sum(list(x).count(5) for x in latticeStrats))
				list6.append(sum(list(x).count(6) for x in latticeStrats))
				list7.append(sum(list(x).count(7) for x in latticeStrats))
		
			if question_5 == True:
				if t >= 100:
					list0.append(sum(list(x).count(0) for x in latticeStrats))
					list1.append(sum(list(x).count(1) for x in latticeStrats))
					list2.append(sum(list(x).count(2) for x in latticeStrats))
					list3.append(sum(list(x).count(3) for x in latticeStrats))
					list4.append(sum(list(x).count(4) for x in latticeStrats))
					list5.append(sum(list(x).count(5) for x in latticeStrats))
					list6.append(sum(list(x).count(6) for x in latticeStrats))
					list7.append(sum(list(x).count(7) for x in latticeStrats))			

		if question_5 == True:
			var0 = np.var(list0) 
			var1 = np.var(list1)
			var2 = np.var(list2)
			var3 = np.var(list3)
			var4 = np.var(list4) 
			var5 = np.var(list5)
			var6 = np.var(list6)
			var7 = np.var(list7)

		varSum = var0 + var1 + var2 + var3 + var4 + var5 + var6 + var7
		varSumRList.append(varSum)
	varSumMatrix.append(varSumRList)
	print("Var matrix: " + str(varSumMatrix))

#	print(list0)
#	print(" ")
#	print(list7)
#	print("Var0: " + str(var0))
#	print("Var1: " + str(var1))
#	print("Var2: " + str(var2))
#	print("Var3: " + str(var3))
#	print("Var4: " + str(var4))
#	print("Var5: " + str(var5))
#	print("Var6: " + str(var6))
#	print("Var7: " + str(var7))

# Plot the heatmap of total prison sentences per person
#plt.figure()
#plt.imshow(latticeStrats,origin='lower', cmap='gist_rainbow', interpolation='nearest')
#plt.imshow(latticeStrats,origin='lower', cmap='cool', interpolation='nearest')
#plt.title('Strategies')
#plt.colorbar()

if question_4 == True:
	# Plot the strategies over time
	plt.figure()
	plt.plot(list0,color="red",label="0")
	plt.plot(list1,color="orange",label="1")
	plt.plot(list2,color="yellow",label="2")
	plt.plot(list3,color="lime",label="3")
	plt.plot(list4,color="green",label="4")
	plt.plot(list5,color="cyan",label="5")
	plt.plot(list6,color="blue",label="6")
	plt.plot(list7,color="purple",label="7")
	plt.legend(loc="upper right")
	plt.xlabel('Time')
	plt.ylabel('Population Fraction')

if question_5 == True:
	# Plot the heatmap of variances
	plt.figure()
	plt.imshow(varSumMatrix,origin='lower', cmap='gist_rainbow', interpolation='nearest')
	plt.title('Variances')
	plt.colorbar()

plt.show()
