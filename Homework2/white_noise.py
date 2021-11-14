# FFR120 Homework 2
# Problem 5.2: Discrete white noise
# Author: Jamie Santos
# Date: 11/13/21


import numpy as np 
from math import sqrt
from matplotlib import pyplot as plt 

#nSteps = 1000
nAgents = 50
time = 5
deltaTList = [0.01, 0.05, 0.1]
nTimeSteps = [int(time/i) for i in deltaTList]

# Generate the list of choices for each method
whiteNoiseList = []
for i in range(len(nTimeSteps)):
	whiteNoise = np.random.default_rng().normal(0, 1, size=(nTimeSteps[i],nAgents))
	whiteNoiseList.append(whiteNoise)

# Setup plots
plotTitles = ["deltaT = 0.01", "deltaT = 0.05", "deltaT = 0.1"]
plotColors = ['r','g','b']
numCases = len(plotTitles)
plt.figure(figsize=(20,5))
trajectories = []

# Generate and plot the trajectories
for case in range(numCases):
	plt.subplot(1,3,case + 1)
	deltaT = deltaTList[case]
	t = [1, 2, 3, 4, 5]
	trajectory = np.cumsum(whiteNoiseList[case] * sqrt(deltaT),axis = 0)	#x_i+1 = x_i+w_i * sqrt(deltaT)
	trajectories.append(trajectory)
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

# Plot the distributions
for case in range(numCases):
#	plt.subplot(1,3,case + 1)
#	plt.hist(trajectories[case][-1,:],color=plotColors[case]) # Plot last step of each agent
	plt.xlim([-150, 150])
	plt.xlabel('x(t)')
	plt.ylabel('t [steps]')
	plt.title(plotTitles[case])

plt.show()
