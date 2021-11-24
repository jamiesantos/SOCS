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
GAMMA = 0.01		# Recovery rate
D = 0.8				# Diffusion rate
timeSteps = 2000 	# Experimental value
beta = 0.6          # Infection rate (varying)
mu = 0.002			# Death rate

nRecovered = R_INIT
nInfected = I_INIT
nDead = D_INIT

population = []
currInfected = 0

#############################
# Initialize the population #
#############################

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

xInit = [p.x for p in population]
yInit = [p.y for p in population]

# Scatterplot showing mobility of patients
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
scatt=ax1.scatter(xInit,yInit,c='blue',s=10)
ax1.set_yticklabels([])
ax1.set_xticklabels([])
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set(xlim=(-.1, TILE_SIZE + 0.1), ylim=(-.1, TILE_SIZE + 0.1))

# Plot of SIR statuses over time
susceptible,=ax2.plot(AGENTS - currInfected,color="blue",label="Susceptible")
infected,=ax2.plot(currInfected,color="orange",label="Infected")
recovered,=ax2.plot(0,color="green",label="Recovered")
dead,=ax2.plot(0,color="gray",label="Dead")
ax2.axis([0,timeSteps,0,AGENTS])
ax2.legend(handles=[susceptible,infected,recovered,dead])
ax2.set_xlabel("Time")
ax2.set_ylabel("People")

# Set up plotting data
susList = []
infList = []
recList = []
deadList = []
times = []

######################### 
# Update a single frame #
#########################

def update(frame,susList,infList,recList,deadList,times):
	# Setting up arrays to pass to matplotlib animation
	times.append(frame)
	nSusceptible = 0
	nInfected = 0
	nRecovered = 0
	nDead = 0
	colors = []
	sizes = [10 for p in population]

	# If patients is infected, possibly infect neighbors
	# and/or recover. Also keep track of recovered patients.
	for p in population:		
		p.update_square(D,TILE_SIZE)
		if p.infected:
			nInfected += 1

			# "Expose" the others nearby
			for other in population:
				if p.id != other.id and np.random.rand() < beta:
					other.spread_infection(p)

			# Check if patient has recovered
			if np.random.rand() < GAMMA:
				p.recover()

			# Check if the patient isn't so lucky
			r1 = np.random.normal()
			r2 = np.random.random()
			#print(r2)
			if r2 < mu:
				p.die()


		# If the patient was already recovered
		elif p.recovered:
			nRecovered += 1

		# If the patient was already dead
		elif p.dead:
			nDead += 1

		colors.append(p.plot_color())

	# Add SIR numbers to lists for plotting 
	nSusceptible = AGENTS - nInfected - nRecovered - nDead
	susList.append(nSusceptible)
	infList.append(nInfected)
	recList.append(nRecovered)
	deadList.append(nDead)

	# Plot the scatterplot
	xPositions = [p.x for p in population]
	yPositions = [p.y for p in population]
	offsets=np.array([xPositions,yPositions])
	scatt.set_offsets(np.ndarray.transpose(offsets))
	scatt.set_color(colors)
	scatt.set_sizes(sizes)

	# Plot the line plots
	susceptible.set_data(times,susList)
	infected.set_data(times,infList)
	recovered.set_data(times,recList)
	dead.set_data(times,deadList)

	# Get the total number of dead patients
	if nInfected == 0:
		print(nDead)

	return scatt,susceptible,infected,recovered,dead

######################
# Run the simulation #
######################

animation = FuncAnimation(fig, update, interval=10,fargs=(susList,infList,recList,deadList,times),blit=False)
plt.show()
