# FFR120 Homework 1
# Problem 1.6: Two-dimensional gas in a box
# Author: Jamie Santos
# Date: 11/7/21

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Initialize parameters and variables
nTimeSteps = 1000
nIndividuals = 100
numDims = 2
m0 = e0 = sig0 =  1
v0 = np.sqrt(2*e0/m0)
t0 = sig0 * np.sqrt(m0/(2*e0))
dt = 0.001*t0
l = 100 * sig0

plotVectors = False
plotEnergies = True

# Representation of a 2-D particle
class Particle:
	def __init__(self, x, y, vx, vy, m0):
		self.mass = m0
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
		rx = x2 - x1
		ry = y2 - y1
		r = self.get_distance(particle)
		term1 = 48 * e0 * sig0**12 * r**-13
		term2 = -24 * e0 * sig0**6 * r**-7
		force_total = term1 + term2
		force_x = force_total * rx/r
		force_y = force_total * ry/r
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
def init_particles(nIndividuals,boxLength,sig0,v0,m0):
	particles = []

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
particles = init_particles(nIndividuals,l,sig0,v0,m0)
x,y = get_all_positions(particles)
scat = plt.scatter(x, y, c="red", s=0.5)

if plotVectors == True:
	plotTimes = [1, 500, 900]
	iPlot = 1
	for i in range(1,1000):
		particles = new_step(particles,e0,sig0)
		x,y = get_all_positions(particles)
		if i in plotTimes:
			plt.subplot(1,3,iPlot)
			iPlot += 1
			plt.scatter(x, y, c="red", s=0.5)
			for j in range(1,nIndividuals):
				origin = (x[j], y[j])
				vx = particles[j].velocities[0]
				vy = particles[j].velocities[1]
				plt.quiver(*origin,vx,vy, color=['b'], scale=70, width = 0.002)
	plt.show()
elif plotEnergies == True:
	f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharey=False)
	kEList = []
	pEList = []
	totalEList = []
	for step in range(1,nTimeSteps):
		particles = new_step(particles,e0,sig0)
		x,y = get_all_positions(particles)
		if step % 100 == 0:
			kETotal = 0
			pETotal = 0
			energyTotal = 0
			for i in range(1,len(particles)):
				# Get kinetic energy of single particle
				vx,vy = particles[i].velocities
				velocity = np.sqrt(vx**2 + vy**2)
				kE = 0.5 * m0 * velocity**2
				#print(kE)
				# Get potential energy of single particle
				v = 0
				for j in range(1,len(particles)):
					if i != j:
						v += particles[i].get_lennard_jones(particles[j],e0,sig0)
				pE = 0.5 * v
				#print(pE)
				# Calculating the total energies of the system
				kETotal += kE
				pETotal += pE
				energyTotal += kE + pE
			kEList.append(kETotal)
			pEList.append(pETotal)
			totalEList.append(energyTotal)
	print(kETotal)
	times=np.arange(0)
	ax1.plot(kEList)
	ax1.set_ylim([390, 400])
	ax2.plot(pEList)
	ax2.set_ylim([-1, 1])
	ax3.plot(totalEList)
	ax3.set_ylim([390, 400])
	plt.pause(0.0001)
	plt.show(block=False)
	plt.show()
else:
	plt.show(block=False)
	plt.pause(0.0001)

	for i in range(1,nTimeSteps):
		particles = new_step(particles,e0,sig0)
		x,y = get_all_positions(particles)
		plt.clf()
		plt.scatter(x, y, c="red", s=1)
		plt.axis([0,l,0,l])
		plt.pause(0.0001)
		plt.show(block=False)
	plt.show()
