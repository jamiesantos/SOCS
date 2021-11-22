# FFR120 Homework 3
# Problem 11.1: Simulation of the SIR model
# Author: Jamie Santos
# Date: 11/21/21


import numpy as np 
from math import sqrt
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize parameters/constants
#AGENTS = 3
#I_INIT = 1
#R_INIT = 0
#S_INIT = AGENTS - I_INIT - R_INIT
#TILE_SIZE = 100		# tileSize x tileSize area	
#GAMMA = 0.01		# Recovery rate
#D = 0.8				# Diffusion rate
#beta = 0.6			# Infection rate (varying)

#nRecovered = R_INIT
#nInfected = I_INIT
		
# Create a "patient" class
class Patient:
	def __init__(self, idNum, x, y):
		self.id = idNum
		self.infectedTime = 0

		# SIR states
		self.susceptible = True
		self.infected = False
		self.recovered = False

		# Positions
		self.x = x
		self.y = y

	def infect(self):
		self.susceptible = False
		self.infected = True
		self.recovered = False

	def recover(self):
		self.susceptible = False
		self.infected = False
		self.recovered = True

	def get_current_pos(self):
		return self.x,self.y

	def spread_infection(self,neighbor):
		neighborInfected = neighbor.infected
		susceptible = self.susceptible
		sameXPos = (self.x == neighbor.x)
		sameYPos = (self.y == neighbor.y)

		if neighborInfected and susceptible and sameXPos and sameYPos:
			self.infect()

	def update_square(self,d,tileSize):
		# Make a move with probability d
		stepDecision = np.random.rand()
		if stepDecision < d:
			if stepDecision < d/2:
				self.x += np.sign(np.random.randn())
			else:
				self.y +=  np.sign(np.random.randn())

		# Check the boundaries
		if self.x < 0:
			self.x = 0
		elif self.y < 0:
			self.y = 0
		elif self.x > tileSize:
			self.x = tileSize
		elif self.y > tileSize:
			self.y = tileSize 		

	def plot_color(self):
		if self.susceptible:
			return "blue"
		elif self.infected:
			return "orange"
		elif self.recovered:
			return "green"

