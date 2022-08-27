import numpy as np
import math
import matplotlib.pyplot as plt

'''
    This function is to see if a random walk of n steps will result in an average distance away from the
    starting point proportional to sqrt(n) using a Monte Carlo Simulation.
'''
def randomwalk():
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
        for j in range(1000):
            intermediate.append(avg_distance(i))
        X.append(i)
        Y.append(np.mean(np.array(intermediate)))

    plt.plot(X, Y, 'b')
    plt.plot(X, [0.889 * math.sqrt(i) for i in X], 'r')
    plt.show()


'''
    This function is to see if in a queue of cars and the speeds of each of the cars in this one-lane highway,
    how many "groups" of cars will form (aka how many times in the list will there be a speed that is the low-
    est speed up to that point from the front). The expected answer is that this would not change as the num-
    ber of cars increase which we will show by Monte Carlo Simulation.
'''
def carexample():
    def count_groups(car_speed_list: list) -> tuple:
        count = 1
        sizes = [0]
        curr_slow_val = car_speed_list[0]
        for idx, val in enumerate(car_speed_list):
            if curr_slow_val > val:
                curr_slow_val = val
                count += 1
                sizes.append(1)
            else:
                sizes[-1] += 1
        return count

    X = []
    Y = []
    for i in range(10, 1000):
        X.append(i)
        counts_list = []
        for _ in range(10000):
            list_of_car_speeds = [round(np.random.normal(65, 5)) for _ in range(100)]
            counts_list.append(count_groups(list_of_car_speeds))
        Y.append(np.mean(np.array(counts_list)))

    plt.plot(X, Y, 'b')
    plt.show()

if __name__ == "__main__":
    #randomwalk()
    carexample()
