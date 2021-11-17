# FFR120 Homework 2
# Problem 5.4: Optically trapped Brownian particle
# Author: Jamie Santos
# Date: 11/16/21


import numpy as np 
from math import sqrt
from matplotlib import pyplot as plt 

# Parameters and inital conditions
r = 1 * 10**-6					# micrometer
eta = 0.001						# N/s
gamma = 6 * np.pi * eta * r
temp = 300						# K
kB = 1.380649 * 10**-23			# J * K^-1
kX = 1	* 10**-6				# pN / meter
kY = 2.5 * 10**-6				# pN / meter
dT = 0.001
nSteps = 100000

# Generate the trajectories
trajX = np.zeros(nSteps)
trajY = np.zeros(nSteps)
wX = np.random.default_rng().normal(0, 1, size=(nSteps))
wY = np.random.default_rng().normal(0, 1, size=(nSteps))

#def generate_trajectories(kX,kY):
for i in range(nSteps - 1):
	termX2 = (-kX/gamma) * trajX[i] * dT
	termX3 = sqrt((2 * kB * temp * dT)/gamma) * wX[i+1]
	trajX[i + 1] = trajX[i] + termX2 + termX3

	termY2 = (-kY/gamma) * trajY[i] * dT
	termY3 = sqrt((2 * kB * temp * dT)/gamma) * wY[i+1]
	trajY[i + 1] = trajY[i] + termY2 + termY3
#	return trajX,trajY

#trajX,trajY = generate_trajectories(kX,kY)

# Plot the path of the particle
plt.figure(figsize=(10,10))
plt.scatter(trajX*10**9,trajY*10**9,s=0.1)
plt.axis('equal')
plt.xlabel('x [nm]')
plt.ylabel('y [nm]')

# Plot the distribution curves
plt.figure()
numBins = 100
pX, x = np.histogram(trajX, bins=numBins, density=True)  # sort data into histograms 
pY, y = np.histogram(trajY, bins=numBins, density=True)
x = x[:-1] + (x[1] - x[0])/2 				# center the bins
y = y[:-1] + (y[1] - y[0])/2
plt.plot(x, pX, color="red", label="x (experimental)")
plt.plot(y, pY, color="blue", label = "y (experimental)")
pXOld = pX
pYOld = pY

# Calculate the theoretical Boltzmann distributions
pX = np.zeros(len(x))
pY = np.zeros(len(y))
for i in range(len(x)):	
	# Get potential energies
	uX = 0.5 * kX * x[i]**2
	uY = 0.5 * kY * y[i]**2
	# Get Boltzmann probabilities
	pX[i] = np.exp(-uX / (kB * temp))
	pY[i] = np.exp(-uY / (kB * temp))
# Normalize scale
pX = [item * sum(pXOld) / sum(pX) for item in pX]
pY = [item * sum(pYOld) / sum(pY) for item in pY]

# Plot the theoretical Boltzmann distributions
plt.plot(x, pX, color="orange", label="x (theoretical)")
plt.plot(y, pY, color="cyan", label="y (theoretical)")
plt.yticks([])
plt.xlabel('x,y')
plt.ylabel('p(x), p(y)')
plt.legend(loc="upper left")

plt.figure()

# Calculate the experimental autocorrelations
cLength = 100
lags = np.arange(cLength) 	# tPrime - t values
meanX=np.mean(trajX)
meanY=np.mean(trajY)
trajX = trajX - meanX
trajY = trajY - meanY
var=np.var(trajX)			# Normalize by dividing by variance
var=np.var(trajY)
cXExp = np.zeros(cLength)
cYExp = np.zeros(cLength)

cXExp=[1. if l==0 else np.sum(trajX[l:]*trajX[:-l])/len(trajX)/var for l in lags]
cYExp=[1. if l==0 else np.sum(trajY[l:]*trajY[:-l])/len(trajY)/var for l in lags]
plt.plot(cXExp[1:],color="orange",label="C_x: experimental")
plt.plot(cYExp[1:],color="cyan",label="C_y: experimental")

# Calculate the theoretical autocorrelations
cXTheory = np.zeros(cLength)
cYTheory = np.zeros(cLength)

for t in range(cLength):
	cXTheory[t] = ((kB * temp)/kX) * np.exp(-kX * dT * t / gamma)
	cYTheory[t] = ((kB * temp)/kY) * np.exp(-kY * dT * t / gamma)

scaleX = np.average(cXExp)/np.average(cXTheory)
scaleY = np.average(cYExp)/np.average(cYTheory)

for i in range(len(cXTheory)):
	cXTheory[i] = cXTheory[i] * scaleX
	cYTheory[i] = cYTheory[i] * scaleY
#plt.plot(cXTheory,color="red",label="C_x: theoretical")
#plt.plot(cYTheory,color="blue",label="C_y: theoretical")

plt.yticks([])
xTicks = [0, 20, 40, 60, 80, 100] # dT = 0.001
tickLabels = ['0','0.2', '0.4', '0.6', '0.8', '1']
plt.xticks(xTicks, tickLabels)
plt.xlabel('Time [s]')
plt.ylabel('Cx, Cy')
plt.legend(loc="upper right")
plt.show(block=False)

# Simulate particle motion for range of stiffnesses
kList = [0.5*10**-6, 10**-6 , 2*10**-6, 5*10**-6, 10*10**-6]

#for i, kVal in enumarate(kList):
	

# Plot variance as function of stiffness




plt.show()
