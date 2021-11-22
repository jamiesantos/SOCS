import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from patients import Patient

# Initialize parameters/constants
AGENTS = 70
INF_RATE = 0.4
I_INIT = int(round(AGENTS * INF_RATE))
R_INIT = 0
S_INIT = AGENTS - I_INIT - R_INIT
TILE_SIZE = 100		# tileSize x tileSize area	
GAMMA = 0.01		# Recovery rate
D = 0.8				# Diffusion rate
beta = 0.6			# Infection rate (varying)

nRecovered = R_INIT
nInfected = I_INIT

population = []
currInfected = 0

# Initialize the population
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

# Initialize graphics
xInit = [p.x for p in population]
yInit = [p.y for p in population]
print(xInit)

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=False)
scatt=ax1.scatter(xInit,yInit,c='blue',s=10)
#ax1.set_yticklabels([])
#ax1.set_xticklabels([])
#ax1.set_xticks([])
#ax1.set_yticks([])
ax1.set(xlim=(-.1, TILE_SIZE + 0.1), ylim=(-.1, TILE_SIZE + 0.1))

susceptible,=ax2.plot(AGENTS - currInfected,color="blue",label="Susceptible")
infected,=ax2.plot(currInfected,color="orange",label="Infected")
recovered,=ax2.plot(0,color="green",label="Recovered")
ax2.axis([0,1000,0,AGENTS])
ax2.legend(handles=[susceptible,infected,recovered])
ax2.set_xlabel("Time")
ax2.set_ylabel("People")

# Set up plotting data
susList = []
infList = []
recList = []
times = []

# Update a single frame
def update(frame,susList,infList,recList,times):
	times.append(frame)
	nSusceptible = 0
	nInfected = 0
	nRecovered = 0
	colors = []
	sizes = [10 for p in population]

	for p in population:		
		p.update_square(D,TILE_SIZE)
		if p.infected:
			nInfected += 1

			# Infect the others nearby
			for other in population:
				if p.id != other.id and np.random.rand() < beta:
					other.spread_infection(p)

			# Check if patient has recovered
			#if np.random.rand() < GAMMA:
			#	p.recover()
		#elif p.recovered:
		#	nRecovered += 1

		colors.append(p.plot_color())

	nSusceptible = AGENTS - nInfected - nRecovered
	#print("infected: " + str(nInfected))
	#print("recovered: " + str(nRecovered))
	susList.append(nSusceptible)
	infList.append(nInfected)
	recList.append(nRecovered)

	xPositions = [p.x for p in population]
	yPositions = [p.y for p in population]
	offsets=np.array([[p.x for p in population],
					 [p.y for p in population]])
	scatt.set_offsets(np.ndarray.transpose(offsets))
	scatt.set_color(colors)
	scatt.set_sizes(sizes)
	susceptible.set_data(times,susList)
	infected.set_data(times,infList)
	recovered.set_data(times,recList)
	return scatt,susceptible,infected,recovered

animation = FuncAnimation(fig, update, interval=10,fargs=(susList,infList,recList,times),blit=False)
plt.show()
#for p in population:
#	print("s: " + str(p.susceptible))
#	print("i: " + str(p.infected))
#	print("r: " + str(p.recovered))
