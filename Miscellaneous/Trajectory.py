#import numpy as np
import math
import matplotlib.pyplot as plt
import random

global G
G = 6.67e-11

class Body:
    # initialize the attributes
    def __init__(self, name: str, loc: tuple, radius: float, mass: float, initial_vel = 0):
        self.name = name
        self.loc = loc
        self.radius = radius
        self.mass = mass
        self.initial_vel = initial_vel

    def get_loc(self) -> tuple:
        return self.loc

    def get_radius(self) -> float:
        return self.radius

    def distance(self, loc: tuple) -> float:
        return math.sqrt((self.loc[0] - loc[0]) ** 2 + (self.loc[1] - loc[1]) ** 2)

    def acc_exerting(self, loc: tuple) -> tuple:
        d = self.distance(loc)
        theta = math.atan((loc[1] - self.loc[1]) / (loc[0] - self.loc[0]))
        if (loc[1] - self.loc[1] < 0 and loc[0] - self.loc[0] < 0) or (loc[1] - self.loc[1] > 0 and loc[0] - self.loc[0] < 0):
            theta += math.pi
        a = G * self.mass / d ** 2
        return -a * math.cos(theta), -a * math.sin(theta)


class Satellite:
    def __init__(self, loc: tuple, vel: tuple):
        self.loc = loc
        self.vel = vel

    def get_loc(self) -> tuple:
        return self.loc

    def get_vel(self) -> tuple:
        return self.vel

    def return_vel(self) -> float:
        return math.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2)

    def set_loc(self, new_p: tuple) -> None:
        self.loc = new_p

    def set_vel(self, new_v: tuple) -> None:
        self.vel = new_v

    def change_vel(self, acc: tuple, time=0.1) -> tuple:
        return self.vel[0] + time * acc[0], self.vel[1] + time * acc[1]

    def change_loc(self, vel: tuple, time=0.1) -> tuple:
        return self.loc[0] + time * vel[0], self.loc[1] + time * vel[1]

    def boost(self, theta, time=0.1) -> tuple:
        return 50 * time * math.cos(theta), 50 * time * math.sin(theta)


INTERVAL = 0.01
Sat = Satellite((0, 0), (5000 * math.cos(math.pi * 37/180), 5000 * math.sin(math.pi * 37/180)))
v0 = Sat.return_vel()
print("STARTING POSITION: " + str(Sat.get_loc()))
print("VELOCITY         : " + str(Sat.get_vel()))
print()

Earth = Body("Earth", (100000000, 100000000), 6.371e6, 5.972e24)
last_dict = {"Loc": Sat.get_loc(),
             "Vel Comp": Sat.get_vel(),
             "Vel": Sat.return_vel(),
             "Acc": Earth.acc_exerting(Sat.get_loc())}
X = [Sat.get_loc()[0]]
Y = [Sat.get_loc()[1]]
V = [Sat.return_vel()]
D = [Earth.distance(Sat.get_loc())]
A = [math.sqrt(Earth.acc_exerting(Sat.get_loc())[0] ** 2 + Earth.acc_exerting(Sat.get_loc())[1] ** 2)]

for i in range(5000000):
    acc = Earth.acc_exerting(Sat.get_loc())
    new_vel = Sat.change_vel(acc, INTERVAL)

    #rand = random.randint(0, 1000)
    #if rand == 0:
    #    new_vel2 = (new_vel[0] + Sat.boost(math.pi * 3/2, INTERVAL)[0], new_vel[1] + Sat.boost(math.pi * 3/2, INTERVAL)[1])
    #    new_vel = new_vel2

    new_loc = Sat.change_loc(new_vel, INTERVAL)

    Sat.set_vel(new_vel)
    Sat.set_loc(new_loc)

    #print("----------------------------------Time %f----------------------------------"%(INTERVAL * (i + 1)))
    #print("     Location:   %s"%(str(Sat.get_loc())))
    #print("     Velocity:   %f"%(Sat.return_vel()))
    #print("Velocity Comp:   %s"%(str(Sat.get_vel())))
    #print(" Acceleration:   %s"%(str(Earth.acc_exerting(Sat.get_loc()))))
    #print()

    X.append(Sat.get_loc()[0])
    Y.append(Sat.get_loc()[1])
    V.append(Sat.return_vel())
    D.append(Earth.distance(Sat.get_loc()))
    A.append(math.sqrt(Earth.acc_exerting(Sat.get_loc())[0] ** 2 + Earth.acc_exerting(Sat.get_loc())[1] ** 2))

    last_dict["Loc"] = Sat.get_loc()
    last_dict["Vel Comp"] = Sat.get_vel()
    last_dict["Vel"] = Sat.return_vel()
    last_dict["Acc"] = Earth.acc_exerting(Sat.get_loc())



    if Earth.distance(Sat.get_loc()) <= Earth.get_radius():
        print("CRASHED")
        break


circle1 = plt.Circle(Earth.get_loc(), Earth.get_radius(), color='b')
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
ax1.set_aspect(1)

ax1.add_patch(circle1)
#ax.set_xlim(left=0, right=100)
#ax.set_ylim(bottom=0, top=100)
ax1.plot(X, Y, 'k')
ax1.title.set_text("Trajectory")

ax4.plot(range(len(V)), V, 'k')
ax4.title.set_text("Velocity")
ax4.grid()

ax3.plot(range(len(A)), A, 'r')
ax3.title.set_text("Acceleration")
ax3.grid()

ax2.plot(range(len(D)), D, 'b')
ax2.title.set_text("Distance")
ax2.grid()
plt.show()