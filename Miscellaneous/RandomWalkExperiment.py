# File to test the hypothesis that the average distance from the starting point of a random walk of size n
# is roughly sqrt(n) using a Monte Carlo Simulation.

import numpy as np
import math
import matplotlib.pyplot as plt

def avg_distance(num: int) -> float:
    directions = ["North", "East", "South", "West"]
    x, y = (0, 0)
    for _ in range(num):
        idx = np.random.random_integers(0, 3)
        if directions[idx] == "North":
            y += 1
        elif directions[idx] == "East":
            x += 1
        elif directions[idx] == "South":
            y -= 1
        else:
            x -= 1
    return math.sqrt(x ** 2 + y ** 2)


X = []
Y = []
for i in range(100):
    intermediate = []
    for j in range(10000):
        intermediate.append(avg_distance(i))
    X.append(i)
    Y.append(np.mean(np.array(intermediate)))

plt.plot(X, Y, 'b')
plt.plot(X, [0.889 * math.sqrt(i) for i in X], 'r')
plt.show()