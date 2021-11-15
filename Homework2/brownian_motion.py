# FFR120 Homework 2
# Problem 5.3: Brownian motion in inertial and viscous regimes
# Author: Jamie Santos
# Date: 11/14/21


import numpy as np 
from math import sqrt
from matplotlib import pyplot as plt 

# Parameters and initial conditions
r = 1 * 10**-6					# micrometer
m = 1.11 * 10 ** -14			# kg
eta = 0.001						# N/s
gamma = 6 * np.pi * eta * r
temp = 300						# K
tau = m / gamma
dT = 0.05 * tau					# set to less than 0.1 tau
kB = 1.380649 * 10**-23			# J * K^-1
length = 100 * tau
#nSteps = int(length / dT)
#nAgents = 100					# Number of realizations
nSteps = 10
nAgents = 7

# Get the next step (with mass):
def nextStepMass(dT, gamma, m, kB, temp, w, xList):
	denom = (1 + dT * (gamma/m))
	term1 = (2 + dT * (gamma/m))/denom * xList[-1]
	term2 = (-1 / denom) * xList[-2]
	term3 = (sqrt(2 * kB * temp * gamma) / (m * denom))*(dT**(3/2))*w
	xNew = term1 + term2 + term3
	xList.append(xNew)
	return xList

# Get the next step (without mass):
def nextStepSimple(dT, gamma, kB, temp, w, xList):
	xNew = xList[-1] + sqrt((2 * kB * temp * dT)/gamma) * w
	xList.append(xNew)
	return xList

# Generate the trajectories
def generateTrajectories():
	massPath = [0, 0]	# Prime the paths with x_(i-2), x_(i-1)
	masslessPath = [0, 0]
	for step in range(nSteps):
		w = np.random.normal()
		massPath = nextStepMass(dT, gamma, m, kB, temp, w, massPath)
		masslessPath = nextStepSimple(dT, gamma, kB, temp, w, masslessPath)
	return massPath,masslessPath

# Get trajectories for inital two plots
massPath,masslessPath = generateTrajectories()

# Make some nice plots
plt.figure(figsize=(20,6))

# Plot for time duration = 1 tau
plt.subplot(1,3,1)
plt.plot(massPath[0:20],linewidth=0.3,color="red")
plt.plot(masslessPath[0:20],linewidth=0.3,color="blue")
xTicks1 = [0, 10, 20]  # dT = 0.05 * tau 
tickLabels1 = ['0','0.5', '1']
plt.xticks(xTicks1, tickLabels1)
plt.ylabel('x(t)')
plt.xlabel('t / tau')

# Plot for time duration = 100 tau
plt.subplot(1,3,2)
plt.plot(massPath,linewidth=0.3,color="red")
plt.plot(masslessPath,linewidth=0.3,color="blue")
xTicks2 = np.multiply(xTicks1,100)
tickLabels2 = ['0','50','100']
plt.xticks(xTicks2, tickLabels2)
plt.ylabel('x(t)')
plt.xlabel('t / tau')

# Compute MSDs for several realizations
msdMassList = []
msdMasslessList = []

# Generate many realizations of paths
massPaths = []
masslessPaths = []
for agent in range(nAgents):	
	massPath,masslessPath = generateTrajectories()	  
	massPaths.append(massPath)
	masslessPaths.append(masslessPath)

for t in range(nSteps - 1):
	squareDistances1 = [np.square(item[t]) for item in massPaths] # Starting position is 0
	squareDistances2 = [np.square(item[t]) for item in masslessPaths]
	msdMass = (1/nAgents) * sum(squareDistances1)
	msdMassList.append(msdMass)
	msdMassless = (1/nAgents) * sum(squareDistances2)
	msdMasslessList.append(msdMassless)

# Plot the MSDs
plt.subplot(1,3,3)
plt.plot(msdMassList,linewidth = 0.5, color="red",label="With mass")
plt.plot(msdMasslessList,linewidth = 0.5, color="blue",label="Without mass")
plt.legend(loc="upper left")
plt.yscale('log')
plt.xscale('log')
plt.xlim(2,2000)
xTicks1 = [20, 2000]  # dT = 0.05 * tau 
tickLabels1 = ['10^0', '10^2']
plt.xticks(xTicks1, tickLabels1)
plt.ylabel('MSD')
plt.xlabel('t / tau')
plt.show(block=False)

# Calculate eMSD
print("eMSD, with mass: " + str(np.average(msdMassList)))
print("eMSD, without mass: " + str(np.average(msdMasslessList)))

# Calculate tMSD
massPath,masslessPath = generateTrajectories() # Generate a single path
squareDistances1 = [np.square(item) for item in massPaths] # Starting position is 0
squareDistances2 = [np.square(item) for item in masslessPaths]
msdMass = (1/nAgents) * sum(squareDistances1)
msdMassless = (1/nAgents) * sum(squareDistances2)


print("tMSD, with mass: " + str(np.average(msdMass)))
print("tMSD, without mass: " + str(np.average(msdMassless)))
