import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from patients import Patient

# Initialize parameters/constants

AGENTS = 1000
INF_RATE = 0.01
I_INIT = int(round(AGENTS * INF_RATE))
R_INIT = 0
S_INIT = AGENTS - I_INIT - R_INIT
TILE_SIZE = 100		# tileSize x tileSize area	
D = 0.8				# Diffusion rate
timeSteps = 2000 	# Experimental value
animationRate = 1
#gamma = 0.01		# Recovery rate (varying)
#beta = 1          	# Infection rate (varying)

nRecovered = R_INIT
nInfected = I_INIT

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
	
	########################
	#  Initialize graphics #
	########################
	
	#xInit = [p.x for p in population]
	#yInit = [p.y for p in population]
	
	# Scatterplot showing mobility of patients
	#fig, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
	#scatt=ax1.scatter(xInit,yInit,c='blue',s=10)
	#ax1.set_yticklabels([])
	#ax1.set_xticklabels([])
	#ax1.set_xticks([])
	#ax1.set_yticks([])
	#ax1.set(xlim=(-.1, TILE_SIZE + 0.1), ylim=(-.1, TILE_SIZE + 0.1))
	
	# Plot of SIR statuses over time
	#susceptible,=ax2.plot(AGENTS - currInfected,color="blue",label="Susceptible")
	#infected,=ax2.plot(currInfected,color="orange",label="Infected")
	#recovered,=ax2.plot(0,color="green",label="Recovered")
	#ax2.axis([0,timeSteps,0,AGENTS])
	#ax2.legend(handles=[susceptible,infected,recovered])
	#ax2.set_xlabel("Time")
	#ax2.set_ylabel("People")
	
	# Set up plotting data
	#susList = []
	#infList = []
	#recList = []
	#times = []

	return population
	#return population,susList,infList,recList,times
	
#gamma1List = []
#gamma2List = []

######################### 
# Update a single frame #
#########################
def update(beta,recInf,gamma,gammaList):
#def update(times,beta,recInf,gamma,gammaList):
	#scatt = 0
	#susceptible = []
	#infected = []
	#recovered = []

	# Setting up arrays to pass to matplotlib animation
	#times.append(frame)
	nSusceptible = 0
	nInfected = 0
	nRecovered = 0
	#colors = []
	#sizes = [10 for p in population]

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

		# If the patient was already recovered
		elif p.recovered:
			nRecovered += 1

		#colors.append(p.plot_color())

	# Add SIR numbers to lists for plotting 
	nSusceptible = AGENTS - nInfected - nRecovered
	#susList.append(nSusceptible)
	#infList.append(nInfected)
	#recList.append(nRecovered)

	if nInfected == 0:
		recInf = True
		gammaList.append(nRecovered)
		#print("APPENDING RECLIST: " + str(recList[-1]))

	#return scatt,susceptible,infected,recovered,recInf,gammaList
	return recInf,gammaList

######################
# Run the simulation #
######################
betas = np.arange(0,1,0.03)
#betas = [0.3]
gammas = [0.01,0.02]

#animation = FuncAnimation(fig, update, interval=animationRate,fargs=(susList,infList,recList,times),blit=False)
#plt.show(Block=False)

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
			recInf,gammaLists[g] = update(beta,recInf,gamma,gammaLists[g])
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

