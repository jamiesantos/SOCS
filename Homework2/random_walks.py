# FFR120 Homework 2
# Problem 5.1: Universality of random walks
# Author: Jamie Santos
# Date: 11/13/21


import numpy as np 
from math import sqrt
from matplotlib import pyplot as plt 

nSteps = 1000
nAgents = 1000

# Generate the list of choices for each method
coinFlips = np.random.choice([1, -1], size = (nAgents,nSteps))
gaussian = np.random.default_rng().normal(0, 1, size=(nAgents,nSteps))
arbitrary = np.random.choice([-1, (1 - sqrt(3))/2, (1 + sqrt(3))/2], size=(nAgents,nSteps))
cases = [coinFlips, gaussian, arbitrary]

# Setup plots
plotTitles = ["Coin Flips", "Gaussian", "Arbitrary"]
plotColors = ['r','g','b']
numCases = len(plotTitles)
yRange = np.arange(0,nAgents)
plt.figure(figsize=(20,6))
trajectories = []

# Generate and plot the trajectories
for case in range(numCases):
	plt.subplot(1,3,case + 1)
	trajectory = np.cumsum(cases[case],axis = 0)	#x_i+1 = x_i+(next random selection)
	print(trajectory.shape)
	trajectories.append(trajectory)
	plt.plot(trajectory[:,0:99],yRange,linewidth=0.1,color=plotColors[case]) # Plot first 100 steps 
	plt.xlim([-50, 50])
	plt.xlabel('x(t)')
	plt.ylabel('t [steps]')
	plt.title(plotTitles[case])

plt.show(block=False)

plt.figure(figsize=(20,6))

# Plot the distributions
for case in range(numCases):
	plt.subplot(1,3,case + 1)
	plt.hist(trajectories[case][:,-1],color=plotColors[case]) # Plot last step of each agent
	plt.xlim([-50, 50])
	plt.xlabel('x(t)')
	plt.ylabel('t [steps]')
	plt.title(plotTitles[case])

plt.show()
