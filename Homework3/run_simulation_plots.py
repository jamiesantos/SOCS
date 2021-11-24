import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from patients import Patient

# Initialize parameters/constants

AGENTS = 1000
INF_RATE = 0.01
I_INIT = int(round(AGENTS * INF_RATE))
R_INIT = 0
D_INIT = 0
S_INIT = AGENTS - I_INIT - R_INIT - D_INIT
TILE_SIZE = 100		# tileSize x tileSize area	
D = 0.8				# Diffusion rate
timeSteps = 2000	# Experimental value
animationRate = 1
#gamma = 0.01		# Recovery rate (varying)
#beta = 1			# Infection rate (varying)
#mu = 0.01			# Death rate

nRecovered = R_INIT
nInfected = I_INIT
nDead = D_INIT

question_2 = False
question_3 = True

def initializeSimulation(beta,gamma):
	#############################
	# Initialize the population #
	#############################

	population = []
	currInfected = 0
	
	for i in range(AGENTS):
		# Generate positions
		x = int(round(np.random.random()*TILE_SIZE))
		y = int(round(np.random.random()*TILE_SIZE))
		patient = Patient(i, x, y)
	
		# Perhaps infect the person
		if np.random.random() < INF_RATE: # May need to include if no one is infected 
			patient.infect()
			currInfected += 1
		population.append(patient)
	
	return population
	

######################### 
# Update a single frame #
#########################
def update(beta,recInf,gamma,gammaList,deadInf,mu,muList):
	nSusceptible = 0
	nInfected = 0
	nRecovered = 0
	nDead = 0

	# If patient is infected, possibly infect neighbors
	# and/or recover. Also keep track of recovered patients.
	for p in population:		
		p.update_square(D,TILE_SIZE)
		if p.infected:
			nInfected += 1

			# "Expose" the others nearby
			for other in population:
				if other.x == p.x and other.y == p.y:
					if p.id != other.id and np.random.rand() < beta:
						other.spread_infection(p)

			# Check if patient has recovered
			if np.random.rand() < gamma:
				p.recover()

			# Check if the patient isn't so lucky
			r1 = np.random.rand()
			r2 = np.random.normal()
			r3 = np.random.random()
			if r3 < mu:
				#print("r2: " + str(r2) + "," + "mu: " + str(mu))
				p.die()

		# If the patient was already recovered
		elif p.recovered:
			nRecovered += 1

		# If the patient was already dead
		elif p.dead:
			nDead += 1

	# Add SIR numbers to lists for plotting 
	nSusceptible = AGENTS - nInfected - nRecovered - nDead

	if nInfected == 0:
		recInf = True
		gammaList.append(nRecovered)

		deadInf = True
		muList.append(nDead)

	#return scatt,susceptible,infected,recovered,recInf,gammaList
	return recInf,gammaList,deadInf,muList

######################
# Run the simulation #
######################

if question_2:
	mu = 0
	muList = []
	betas = np.arange(0,1,0.03)
	gammas = [0.01,0.02]
	
	gamma1List = []
	gamma2List = []
	gammaLists = [gamma1List,gamma2List]
	
	for g in range(len(gammas)):
		gamma = gammas[g]
		print("gamma: " + str(gamma))
		for b in range(len(betas)):
			print("beta: " + str(betas[b]))
			beta = betas[b]
			recInf = False
			population = initializeSimulation(beta,gamma)
			frame = 0
			while recInf == False:
				recInf,gammaLists[g],deadInf,muList = update(beta,recInf,gamma,gammaLists[g],mu,muList)
			frame += 1
	print("Gamma = 0.01: " + str(gamma1List))
	print("Gamma = 0.02: " + str(gamma2List))
	print("Betas: " + str(betas))

	# Plot final number recovered as function of beta
	plt.figure()
	plt.scatter(betas,gamma1List,color = "blue",label="gamma = 0.01")
	plt.scatter(betas,gamma2List,color="green",label="gamma = 0.02")
	plt.legend(loc="upper left")
	plt.xlabel('Beta')
	plt.ylabel('R_infinity')
	plt.show()

elif question_3:
	beta = 1
	gamma = 0.001
	gammaList = []
	recInf = False
	mus = np.arange(0.0,0.1,0.001)
	#mus = np.arange(0.95,1,0.0001)
	#mus = np.arange(0,1,0.001)
	muList = []

	for m in range(len(mus)):
		mu = mus[m]
		deadInf = False
		population = initializeSimulation(beta,gamma)
		frame = 0
		while deadInf == False:
			recInf,gammaList,deadInf,muList = update(beta,recInf,gamma,gammaList,deadInf,mu,muList)
			if len(muList) > 0:
				print(muList[-1])
		frame += 1

	# Plot final number dead as a function of mu
	plt.figure()
	plt.scatter(mus,muList,color = "red")
	plt.xlabel('Mu')
	plt.ylabel('D_infinity')
#	plt.ylim(0, 200)
	plt.show()

