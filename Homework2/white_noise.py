# FFR120 Homework 2
# Problem 5.2: Discrete white noise
# Author: Jamie Santos
# Date: 11/13/21


import numpy as np 
from math import sqrt
from matplotlib import pyplot as plt 
nAgents = 50
nAgentsMSD = 1000
#nAgentsMSD = 7
time = 5
deltaTList = [0.01, 0.05, 0.1]
nTimeSteps = [int(time/i) for i in deltaTList]
#nTimeSteps = [3, 4, 5]

# Generate the list of choices for each method
def generateChoices(numTimeSteps, numAgents):
	whiteNoiseList = []
	for i in range(len(nTimeSteps)):
		whiteNoise = np.random.default_rng().normal(0, 1, size=(numTimeSteps[i],numAgents))
		whiteNoiseList.append(whiteNoise)
	return whiteNoiseList

# Setup plots
plotTitles = ["deltaT = 0.01", "deltaT = 0.05", "deltaT = 0.1"]
plotColors = ['r','g','b']
numCases = len(plotTitles)
plt.figure(figsize=(20,5))
#trajectories = []

# Generate and plot the trajectories
whiteNoiseList = generateChoices(nTimeSteps, nAgents)

for case in range(numCases):
	plt.subplot(1,3,case + 1)
	deltaT = deltaTList[case]
	t = [1, 2, 3, 4, 5]
	trajectory = np.cumsum(whiteNoiseList[case] * sqrt(deltaT),axis = 0)	#x_i+1 = x_i+w_i * sqrt(deltaT)
	plt.plot(trajectory[:,0:99],linewidth=0.2,color=plotColors[case]) # Plot first 100 steps 
	scale = 1 / deltaT
	xticks = [0, scale, 2*scale, 3*scale, 4*scale, 5*scale]
	ticklabels = ['0','1', '2', '3', '4', '5']
	plt.xticks(xticks, ticklabels)
	plt.ylim([-5, 5])
	plt.ylabel('x(t)')
	plt.xlabel('t(s)')
	plt.title(plotTitles[case])

plt.show(block=False)
plt.figure(figsize=(20,5))

# Generate 10^4 trajectories and calculate and plot the MSD's
whiteNoiseList = generateChoices(nTimeSteps, nAgentsMSD)
for case in range(numCases):
	plt.subplot(1,3,case + 1)
	deltaT = deltaTList[case]
	t = [1, 2, 3, 4, 5]
	trajectory = np.cumsum(whiteNoiseList[case] * sqrt(deltaT),axis = 0)	#x_i+1 = x_i+w_i * sqrt(deltaT)
	msdSum = 0
	msdList = []
	#for t in range(nTimeSteps[case] - 1):
	print("CASE##############" + str(t))
	for t in range(nTimeSteps[case] - 1):
		#print("trajectory next:" + str(trajectory[t+1,:]))
		#print("trajectory curr:" + str(trajectory[t,:]))
		distances = trajectory[t+1,:] - trajectory[0,:]
		squareDistances = np.square(distances)
		MSD = (1/nAgentsMSD) * sum(squareDistances)
		#print("msd:" + str(MSD))
		msdList.append(MSD)
	#print(msdList)
	plt.plot(msdList,linewidth = 0.2, color=plotColors[case])
	scale = 1 / deltaT
	xticks = [0, scale, 2*scale, 3*scale, 4*scale, 5*scale]
	ticklabels = ['0','1', '2', '3', '4', '5']
	plt.xticks(xticks, ticklabels)
	plt.ylim([0, 5])
	plt.ylabel('MSD')
	plt.xlabel('t(s)')
	plt.title(plotTitles[case])
plt.show()
