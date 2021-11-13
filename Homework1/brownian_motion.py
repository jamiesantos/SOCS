# FFR120 Homework 1
# Problem 1.8: Brownian motion
# Author: Jamie Santos
# Date: 11/7/21

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

pathPlot = False
timePlot = True

# Initialize parameters and variables
nTimeSteps = 10000
nIndividuals = 100
numDims = 2
m0 = e0 = sig0 =  1
M = 40 * m0
rho = 10
v0 = np.sqrt(2*e0/m0)*40
t0 = sig0 * np.sqrt(m0/(2*e0))
dt = 0.00005*t0
l = 100 * sig0

plotVectors = True

# Representation of a 2-D particle
class Particle:
	def __init__(self, x, y, vx, vy, mass):
		self.mass = mass
		self.positions = np.array([x,y])
		self.velocities = np.array([vx,vy])

	def get_distance(self,particle):
		x1,y1 = self.positions
		x2,y2 = particle.positions
		distance = np.sqrt((x2-x1)**2 + (y2-y1)**2)
		return distance
	
	def check_min_distance(self,particle,sig0):
		distanceOkay = True
		if self.get_distance(particle) < sig0:
			distanceOkay = False
		return distanceOkay

	# Calculate force between two particles using the
	# negative gradient of the Lennard-Jones potential
	def get_force_vectors(self,particle,e0,sig0):
		x1,y1 = self.positions
		x2,y2 = particle.positions

		# Check if the interaction involves massive particle
		if self.mass == M or particle.mass == M:
			rx = abs(x2 - x1) - rho
			ry = abs(y2 - y1) - rho
			r = np.sqrt(rx**2 + ry**2)
		else:
			rx = x2 - x1
			ry = y2 - y1
			r = self.get_distance(particle)

		term1 = 48 * e0 * sig0**12 * r**-13
		term2 = -24 * e0 * sig0**6 * r**-7
		force_total = term1 + term2
		force_x = force_total * rx
		force_y = force_total * ry
		return force_x,force_y

	def get_position(self,dt):
		x,y = self.positions
		vx,vy = self.velocities
		x = x + vx * dt/2
		y = y + vy * dt/2
		return x,y

	def get_new_velocities(self,totalForces,m0,dt):
		vx,vy = self.velocities
		fx,fy = totalForces
		vx = vx + (fx/m0) * dt
		vy = vy + (fy/m0) * dt
		return vx,vy
		
# Initialize the locations of the particles
def init_particles(nIndividuals,boxLength,sig0,v0,m0,M):
	particles = []

    # Create a massive particle in the center
	x = y = int(round(l/2))
	vx = vy = 0
	newParticle = Particle(x,y,vx,vy,M)
	particles.append(newParticle)
	
	for i in range(nIndividuals):
		distanceOkay = False
		while(distanceOkay != True):
			distanceOkay = True
			x,y = (boxLength * np.random.rand(2)) - sig0
			vx = (random.randint(0,1)*2-1)*np.sqrt(2)*v0
			vy = (random.randint(0,1)*2-1)*np.sqrt(2)*v0
			newParticle = Particle(x,y,vx,vy,m0)

			# Check that the distance between two particles is greater than sigma
			for j in range(len(particles)):
				distance = newParticle.get_distance(particles[j])
				# Check that particle is not overlapping with massive particle
				if j == 0:
					if distance < rho:
						distanceOkay = False
						break
				# Check that the distance between two particles is greater than sigma
				else:
					if distance < sig0:
						distanceOkay = False
						break

		particles.append(newParticle)
	return particles

# Get the next positions and velocities of particles
# by implementing the leapfrog algorithm
def new_step(particles,e0,sig0):
	for i in range(len(particles)):
		# Retain old positions in case of boundary collision
		xOld,yOld = particles[i].positions
        # Get positions at half a time step
		xHalf,yHalf = particles[i].get_position(dt/2)
		particles[i].positions = xHalf,yHalf

		totalForces = [0,0]
        # Get total force in each direction
		for j in range(len(particles)):
			if i != j:
				totalForces += np.asarray(particles[i].get_force_vectors(particles[j],e0,sig0))
		totalForces = tuple(totalForces)

        # Get new velocities
		vx,vy = particles[i].get_new_velocities(totalForces,m0,dt)
		particles[i].velocities = vx,vy

        # Get new positions
		x,y = particles[i].get_position(dt/2)

		# Check for boundary collisions
		collision = False
		if x < 0:
			x = abs(x-xOld)
			vx = -vx
			collision = True
		elif x > l:
			x = l - abs(x-xOld)	
			vx = -vx
			collision = True
		elif y < 0:
			y = abs(y-yOld)
			vy = -vy
			collision = True
		elif y > l:
			y = l - abs(y-yOld)
			vy = -vy
			collision = True

		if collision == True:
			particles[i].velocities = vx,vy

		particles[i].positions = x,y		
	return particles

def get_all_positions(particles):
	positionsList=[list(p.positions) for p in particles]
	x = [item[0] for item in positionsList]
	y = [item[1] for item in positionsList]
	return x,y

plt.axis([0,l,0,l])
particles = init_particles(nIndividuals,l,sig0,v0,m0,M)
x,y = get_all_positions(particles)
scat = plt.scatter(x, y, c="red", s=0.5)
plt.show(block=False)
plt.pause(0.0001)

# Setup for plotting
bigParticleX = []
bigParticleY = []
s = [rho**2]
s.extend(np.ones(nIndividuals))

for i in range(1,nTimeSteps):
	plt.clf()
	particles = new_step(particles,e0,sig0)
	xOld = x
	yOld = y
	x,y = get_all_positions(particles)
	if x[0] > 0 and x[0] < l and y[0] > 0 and y[0] < l:
		bigParticleX.append(x[0])
		bigParticleY.append(y[0])
		plt.scatter(x, y, c="red", s=s)
		plt.axis([0,l,0,l])
		plt.pause(0.0001)
		plt.show(block=False)
	else:
		x = xOld
		y = yOld
		break

# Plot the final step and overall trajectory 
fig = plt.figure()
if pathPlot == True:
	ax1 = fig.add_subplot(111)
	ax1.scatter(x, y, s=s, c='r', marker="o")
	ax1.plot(bigParticleX,bigParticleY, color='blue')
	ax1.set_xlim([0, l])
	ax1.set_ylim([0, l])
# Plot the trajectory as a function of time
elif timePlot ==True:
	ax1 = fig.add_subplot(111)
	ax1.plot(bigParticleX, color='blue',label = 'X Positions')
	ax1.plot(bigParticleY, color='red',label = 'Y Positions')
	
	dispSum = 0
	print(nTimeSteps)
	print(len(bigParticleX))
	# Also calculate the mean square displacement
	for i in range(1,nTimeSteps - 2):
		xDiff = bigParticleX[i + 1] - bigParticleX[i]
		yDiff = bigParticleY[i + 1] - bigParticleY[i]
		dispSum += xDiff**2 + yDiff**2
	msd = (1/(nTimeSteps - 1)) * dispSum
	print("MSD: " + str(dispSum))
	tau = 1
	d = msd / (4 * tau)
	print("D: " + str(d))
plt.show()
