# FFR120 Homework 1
# Problem 1.1, 1.3: Harmonic oscillator simulated
#	with Euler and leapfrog algorithms
# Author: Jamie Santos
# Date: 11/6/21

import matplotlib.pyplot as plt
import numpy as np

# Parameters/initial conditions
n = 10000
k = 0.1
m = 1

freq = np.sqrt(k/m)/(2*np.pi)
deltaT = 0.01  # Compare with 0.1 and 0.05

xEuler = np.zeros(n)
vEuler = np.ones(n)
uEuler = np.zeros(n)
kEuler = np.zeros(n)
eEuler = np.zeros(n)

xLeap = np.zeros(n)
vLeap = np.ones(n)
uLeap = np.zeros(n)
kLeap = np.zeros(n)
eLeap = np.zeros(n)

# Get the inital simulated energies
uEuler[0] = uLeap[0] = 0.5 * k * xEuler[0]**2
kEuler[0] = kLeap[0] = 0.5 * m * vEuler[0]**2
eEuler[0] = eLeap[0] = uEuler[0] + kEuler[0]

# Simulate the particle motion with Euler's algorithm
for step in range(n - 1):
	xEuler[step + 1] = xEuler[step] + vEuler[step] * deltaT
	force = -k * xEuler[step]
	vEuler[step + 1] = vEuler[step] + (force / m) * deltaT
	uEuler[step + 1] = 0.5 * k * xEuler[step + 1]**2
	kEuler[step + 1] = 0.5 * m * vEuler[step + 1]**2
	eEuler[step + 1] = uEuler[step + 1] + kEuler[step + 1]
print("Euler: Simulated total energy at start: {:.4f}, end: {:.4f}".format(eEuler[0],eEuler[-1]))

# Simulate the particle motion with the leapfrog algorithm
for step in range(n - 1):
	xTemp = xLeap[step] + vLeap[step] * deltaT/2
	force = -k * xTemp
	vLeap[step + 1] = vLeap[step] + (force / m) * deltaT
	xLeap[step + 1] = xTemp + vLeap[step + 1] * deltaT/2
	uLeap[step + 1] = 0.5 * k * xLeap[step + 1]**2
	kLeap[step + 1] = 0.5 * m * vLeap[step + 1]**2
	eLeap[step + 1] = uLeap[step + 1] + kLeap[step + 1]
print("Leapfrog: Simulated total energy at start: {:.4f}, end: {:.4f}".format(eLeap[0],eLeap[-1]))
print(eLeap)

# Calculate the actual total amount of energy
r0 = xEuler[0]
v0 = vEuler[0]
time = deltaT * n   # Arbitrarily use the last time since the total energy doesn't change
w = np.sqrt(k/m)
a = np.sqrt(r0**2 + (v0 / w)**2)
phi = np.arccos(r0/a)

def totalEnergy(t):
	rActual = a * np.cos(w*t + phi)
	vActual = -w * a * np.sin(w*t + phi)
	uEActual = 0.5 * k * rActual ** 2
	kEActual = 0.5 * m * vActual ** 2
	return uEActual + kEActual

eActual = totalEnergy(time)
print("Analytical total energy: {:.4f}".format(eActual))

# Plot oscillations
times = np.arange(0, n, 1)
t = times * freq
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.plot(t,xEuler,'r',label="Euler")
ax1.plot(t,xLeap,'b',label="Leapfrog")
ax1.legend(loc="upper left")
ax1.set(xlabel='Time/T', ylabel='position',
       title='Position of Spring Over Time')
ax1.grid()

# Plot total energy ratios as a function of time/period
energyRatios1 = eEuler / eActual
energyRatios2 = eLeap / eActual
energyRatios3 = totalEnergy(times) / eActual  # Trivial since total energy doesn't change
ax2.plot(t,energyRatios1,'r',label="Euler")
ax2.plot(t,energyRatios2,'b',label="Leapfrog")
ax2.plot(t,energyRatios3,'g',label="Analytical")
ax2.legend(loc="upper left")
ax2.set(xlabel='Time/T', ylabel='E(t)/E_0',
	title='Energy Ratio Between Simulation and Analysis Over Time')
ax2.grid()
plt.show()   
