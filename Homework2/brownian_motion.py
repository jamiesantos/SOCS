# FFR120 Homework 2
# Problem 5.3: Brownian motion in inertial and viscous regimes
# Author: Jamie Santos
# Date: 11/14/21


import numpy as np 
from math import sqrt
from matplotlib import pyplot as plt 

# Parameters and initial conditions
r = 1 							# micrometer
m = 1.11 * 10 ** -14 			# kg
eta = 0.001 					# N/s
gamma = 6 * np.pi * eta * r
temp = 300						# K
tau = m / gamma
dT = 0.05 * tau					# set to less than 0.1 tau
kB = 1.380649 * 10**-23 		# J * K^-1
length = 100 * tau
nSteps = int(length / dT)

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
massPath = [0, 0] 	# Prime the paths with x_(i-2), x_(i-1)
masslessPath = [0, 0]
for step in range(nSteps):
	w = np.random.normal()
	massPath = nextStepMass(dT, gamma, m, kB, temp, w, massPath)
	masslessPath = nextStepSimple(dT, gamma, kB, temp, w, masslessPath)

# Make some nice plots
plt.figure(figsize=(20,6))
plt.plot(massPath,linewidth=0.1,color="red")
plt.plot(masslessPath,linewidth=0.1,color="blue")
		
plt.show()
