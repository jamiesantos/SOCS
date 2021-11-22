# FFR120 Homework 3
# Problem 11.1: Simulation of the SIR model
# Author: Jamie Santos
# Date: 11/21/21


import numpy as np 
from math import sqrt
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize parameters/constants
AGENTS = 3
I_INIT = 1
R_INIT = 0
S_INIT = AGENTS - I_INIT - R_INIT
TILE_SIZE = 100		# tileSize x tileSize area	
GAMMA = 0.01		# Recovery rate
D = 0.8				# Diffusion rate
beta = 0.6 			# Infection rate (varying)

nRecovered = R_INIT
nInfected = INF_0
		
# Create a "patient" class
class Patient:
	def __init__(self, idNum, x, y, xNext, yNext, moveDir):
		self.id = idNum
		self.infectedTime = 0
		self.color = "gray"

		# SIR states
		self.susceptible = True
		self.infected = False
		self.recovered = False

		# Positions
		self.x = x
		self.y = y
		self.xNext = xNext
		self.yNext = yNext

	def infection(self):
		self.susceptible = False
        self.infected = True
        self.recovered = False

	def recovery(self):
		self.susceptible = False
        self.infected = False
        self.recovered = True

	def get_current_pos(self):
		return self.x,self.y

	def check_infection(self,neighbor):
		if self.susceptible == True && neighbor.infected == True
			self.infection()

	def update_square(self):
		# Make a move with probability d
		stepDecision = np.random.rand(AGENTS)
		if stepDecision < D:
			if stepDecision < D/2:
				xNext = x + np.sign(np.random.randn())
			else:
				yNext = y + np.sign(np.random.randn())

		# Check the boundaries
		if xNext < 0:
			xNext = 0
		elif yNext < 0:
			yNext = 0
		elif xNext > TILE_SIZE:
			xNEXT = TILE_SIZE
		elif yNext > TILE_SIZE:
			yNext = TILE_SIZE 

	def plot_color(self):
		if self.susceptible:
			self.color = "blue"
		elif self.infected:
			self.color = "orange"
		elif self.recovered:
			self.color = "green"

# Initialize positions of agents in lattice

# Run the simulation
# while nInfected != 0
	# perform random walk step
	# check if any agents within same cell as infected
	# update statuses
	# Plot S/I/R
