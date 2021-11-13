import numpy as np 
from matplotlib import pyplot as plt

N = 2000
dt = 0.05
k = 0.1
x = np.zeros(N)
V = np.ones(N)

for t in range(N-1):
    x[t+1] = x[t] + V[t]*dt                 # Harmonic oscillator position eqution, Euler
    V[t+1] = V[t] - k*x[t]*dt               # Harmonic oscillator velocity equation, Euler

plt.figure(figsize=(15,5))
plt.plot(x)


x = np.zeros(N)
V = np.ones(N)

for t in range(N-1): 
    x[t+1] = x[t] + V[t]*dt                 # Harmonic oscillator position eqution, Leap-Frog algorithm 
    V[t+1] = V[t] - k*(x[t]+x[t+1])/2*dt    # Harmonic oscillator velocity eqution, Leap-Frog algorithm 


plt.plot(x)
plt.legend(['Euler','Leap-frog'])
plt.ylabel('$x$')
plt.xlabel('$t$')
plt.title('Harmonic oscillator')
plt.rcParams.update({'font.size': 18})
plt.show()
