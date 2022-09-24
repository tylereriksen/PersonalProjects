import numpy as np
import random
from gym import Env
from gym.spaces import Discrete, Box
import matplotlib.pyplot as plt

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

    def set_loc(self, new_loc: tuple) -> None:
        self.loc = new_loc

    def distance(self, loc: tuple) -> float:
        return np.sqrt((self.loc[0] - loc[0]) ** 2 + (self.loc[1] - loc[1]) ** 2)

    def acc_exerting(self, loc: tuple) -> tuple:
        d = self.distance(loc)
        theta = np.arctan((loc[1] - self.loc[1]) / (loc[0] - self.loc[0]))
        if (loc[1] - self.loc[1] < 0 and loc[0] - self.loc[0] < 0) or (loc[1] - self.loc[1] > 0 and loc[0] - self.loc[0] < 0):
            theta += np.pi
        a = G * self.mass / d ** 2
        return -a * np.cos(theta), -a * np.sin(theta)


class Satellite:
    def __init__(self, loc: tuple, vel: tuple):
        self.loc = loc
        self.vel = vel
        self.heading = np.arctan(vel[1] / vel[0])

    def get_loc(self) -> tuple:
        return self.loc

    def get_heading(self) -> float:
        return self.heading

    def get_vel(self) -> tuple:
        return self.vel

    def return_vel(self) -> float:
        return np.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2)

    def set_loc(self, new_p: tuple) -> None:
        self.loc = new_p

    def set_vel(self, new_v: tuple) -> None:
        self.vel = new_v
        self.heading = np.arctan(new_v[1] / new_v[0])

    def change_vel(self, acc: tuple, time=0.1) -> tuple:
        return self.vel[0] + time * acc[0], self.vel[1] + time * acc[1]

    def change_loc(self, vel: tuple, time=0.1) -> tuple:
        return self.loc[0] + time * vel[0], self.loc[1] + time * vel[1]

    def boost(self, theta, time=0.1) -> tuple:
        return 50 * time * np.cos(theta), 50 * time * np.sin(theta)


global Earth
Earth = Body("Earth", (200000000, 250000000), 6.371e6, 5.972e24)

global Target
Target = Body("Planet1", (450000000, 700000000), 8.149e6, 1.954e25)

class SpaceshipMove(Env):
    def __init__(self):
        # either turn left, keep going straight, or turn right
        self.action_space = Discrete(16)

        # Box of x coordinate and y coordinate with the velocity and heading
        self.observation_space = Box(low=np.array([0, 0, 0, 0]), high=np.array([1000000000, 1000000000, 500000, 360]))
        self._target = Target.get_loc()

        # starts at origin and is pointed 35-45 degrees above the x-axis
        self.state = np.array([0, 0, np.random.randint(5000, 10000), np.random.randint(35, 55)])
        self.satellite = Satellite((0, 0), (self.state[2] * np.cos(np.pi * self.state[3] / 180),
                                            self.state[2] * np.sin(np.pi * self.state[3] / 180)))

        # coordinate values
        self.x = 0
        self.y = 0
        self.episode_len = 0

        # for plotting purposes (see the trajectory of spacecraft
        self.plot = [tuple([self.x, self.y])]

    def _action_cat(self, action: int) -> tuple:
        if action == 0:
            return 0, 0
        elif action == 1:
            return np.cos(self.satellite.get_heading() - (np.pi / 4)) * 0.3, \
                   np.sin(self.satellite.get_heading() - (np.pi / 4)) * 0.3
        elif action == 2:
            return np.cos(self.satellite.get_heading() - (3 * np.pi / 4)) * 0.3, \
                   np.sin(self.satellite.get_heading() - (3 * np.pi / 4)) * 0.3
        elif action == 3:
            return np.cos(self.satellite.get_heading() + (3 * np.pi / 4)) * 0.3, \
                   np.sin(self.satellite.get_heading() + (3 * np.pi / 4)) * 0.3
        elif action == 4:
            return np.cos(self.satellite.get_heading() + (np.pi / 4)) * 0.3, \
                   np.sin(self.satellite.get_heading() + (np.pi / 4)) * 0.3
        elif action == 5:
            return np.cos(self.satellite.get_heading() - (np.pi / 4)) * 0.3 + \
                   np.cos(self.satellite.get_heading() - (3 * np.pi / 4)) * 0.3, \
                   np.sin(self.satellite.get_heading() - (np.pi / 4)) * 0.3 + \
                   np.sin(self.satellite.get_heading() - (3 * np.pi / 4)) * 0.3
        elif action == 6:
            return np.cos(self.satellite.get_heading() - (np.pi / 4)) * 0.3 + \
                   np.cos(self.satellite.get_heading() + (3 * np.pi / 4)) * 0.3, \
                   np.sin(self.satellite.get_heading() - (np.pi / 4)) * 0.3 + \
                   np.sin(self.satellite.get_heading() + (3 * np.pi / 4)) * 0.3
        elif action == 7:
            return np.cos(self.satellite.get_heading() - (np.pi / 4)) * 0.3 + \
                   np.cos(self.satellite.get_heading() + (np.pi / 4)) * 0.3, \
                   np.sin(self.satellite.get_heading() - (np.pi / 4)) * 0.3 + \
                   np.sin(self.satellite.get_heading() + (np.pi / 4)) * 0.3
        elif action == 8:
            return np.cos(self.satellite.get_heading() - (3 * np.pi / 4)) * 0.3 + \
                   np.cos(self.satellite.get_heading() + (3 * np.pi / 4)) * 0.3, \
                   np.sin(self.satellite.get_heading() - (3 * np.pi / 4)) * 0.3 + \
                   np.sin(self.satellite.get_heading() + (3 * np.pi / 4)) * 0.3
        elif action == 9:
            return np.cos(self.satellite.get_heading() - (3 * np.pi / 4)) * 0.3 + \
                   np.cos(self.satellite.get_heading() + (np.pi / 4)) * 0.3, \
                   np.sin(self.satellite.get_heading() - (3 * np.pi / 4)) * 0.3 + \
                   np.sin(self.satellite.get_heading() + (np.pi / 4)) * 0.3
        elif action == 10:
            return np.cos(self.satellite.get_heading() + (3 * np.pi / 4)) * 0.3 + \
                   np.cos(self.satellite.get_heading() + (np.pi / 4)) * 0.3, \
                   np.sin(self.satellite.get_heading() + (3 * np.pi / 4)) * 0.3 + \
                   np.sin(self.satellite.get_heading() + (np.pi / 4)) * 0.3
        elif action == 11:
            return np.cos(self.satellite.get_heading() - (np.pi / 4)) * 0.3 + \
                   np.cos(self.satellite.get_heading() - (3 * np.pi / 4)) * 0.3 + \
                   np.cos(self.satellite.get_heading() + (3 * np.pi / 4)) * 0.3, \
                   np.sin(self.satellite.get_heading() - (np.pi / 4)) * 0.3 + \
                   np.sin(self.satellite.get_heading() - (3 * np.pi / 4)) * 0.3 + \
                   np.sin(self.satellite.get_heading() + (3 * np.pi / 4)) * 0.3
        elif action == 12:
            return np.cos(self.satellite.get_heading() - (np.pi / 4)) * 0.3 + \
                   np.cos(self.satellite.get_heading() - (3 * np.pi / 4)) * 0.3 + \
                   np.cos(self.satellite.get_heading() + (np.pi / 4)) * 0.3, \
                   np.sin(self.satellite.get_heading() - (np.pi / 4)) * 0.3 + \
                   np.sin(self.satellite.get_heading() - (3 * np.pi / 4)) * 0.3 + \
                   np.sin(self.satellite.get_heading() + (np.pi / 4)) * 0.3
        elif action == 13:
            return np.cos(self.satellite.get_heading() - (np.pi / 4)) * 0.3 + \
                   np.cos(self.satellite.get_heading() + (3 * np.pi / 4)) * 0.3 + \
                   np.cos(self.satellite.get_heading() + (np.pi / 4)) * 0.3, \
                   np.sin(self.satellite.get_heading() - (np.pi / 4)) * 0.3 + \
                   np.sin(self.satellite.get_heading() + (3 * np.pi / 4)) * 0.3 + \
                   np.sin(self.satellite.get_heading() + (np.pi / 4)) * 0.3
        elif action == 14:
            return np.cos(self.satellite.get_heading() - (3 * np.pi / 4)) * 0.3 + \
                   np.cos(self.satellite.get_heading() + (3 * np.pi / 4)) * 0.3 + \
                   np.cos(self.satellite.get_heading() + (np.pi / 4)) * 0.3, \
                   np.sin(self.satellite.get_heading() - (3 * np.pi / 4)) * 0.3 + \
                   np.sin(self.satellite.get_heading() + (3 * np.pi / 4)) * 0.3 + \
                   np.sin(self.satellite.get_heading() + (np.pi / 4)) * 0.3
        elif action == 15:
            return np.cos(self.satellite.get_heading() - (np.pi / 4)) * 0.3 + \
                   np.cos(self.satellite.get_heading() - (3 * np.pi / 4)) * 0.3 + \
                   np.cos(self.satellite.get_heading() + (3 * np.pi / 4)) * 0.3 + \
                   np.cos(self.satellite.get_heading() + (np.pi / 4)) * 0.3, \
                   np.sin(self.satellite.get_heading() - (np.pi / 4)) * 0.3 + \
                   np.sin(self.satellite.get_heading() - (3 * np.pi / 4)) * 0.3 + \
                   np.sin(self.satellite.get_heading() + (3 * np.pi / 4)) * 0.3 + \
                   np.sin(self.satellite.get_heading() + (np.pi / 4)) * 0.3

    def end_goal(self) -> bool:
        if (self._target[0] - self.x) ** 2 + (self._target[1] - self.y) ** 2 <= 1e14 and \
                self.satellite.return_vel() < 9000:
            return True
        return False

    def step(self, action, time=0.01) -> tuple:
        # new velocity
        boost = self._action_cat(action)
        body1_a = Earth.acc_exerting(self.satellite.get_loc())
        body2_a = Target.acc_exerting(self.satellite.get_loc())
        total_a = body1_a[0] + body2_a[0], body1_a[1] + body2_a[1]
        new_vel = self.satellite.change_vel(total_a, time)
        self.satellite.set_vel((new_vel[0] + boost[0], new_vel[1] + boost[1]))
        self.satellite.set_loc(self.satellite.change_loc(self.satellite.get_vel(), time))

        self.state = np.array([self.satellite.get_loc()[0], self.satellite.get_loc()[1],
                               self.satellite.return_vel(), 180 * self.satellite.get_heading() / np.pi % 360])
        self.x = self.state[0]
        self.y = self.state[1]
        self.plot.append(tuple([self.x, self.y]))

        reward = -1
        if self.end_goal():
            reward = 0
        done = False

        self.episode_len += 1

        # if spaceship goes out of bounds or reaches the target within acceptable margin of error
        # episode is finished
        if reward == 0 or \
                Earth.distance(self.satellite.get_loc()) <= Earth.get_radius() or \
                self.episode_len > 15000000 or self.x > 1000000000 or self.y > 1000000000:
            done = True

        info = {}
        return self.state, reward, done, info

    def render(self) -> None:
        circle1 = plt.Circle(Earth.get_loc(), Earth.get_radius(), color='b')
        target = plt.Circle(self._target, 1e7, color='r')
        fig, ax = plt.subplots()
        ax.set_aspect(1)
        ax.add_patch(circle1)
        ax.add_patch(target)
        ax.plot([a[0] for a in self.plot], [a[1] for a in self.plot], 'k')
        plt.show()

    def reset(self) -> np.array:
        self.state = np.array([0, 0, np.random.randint(5000, 10000), np.random.randint(30, 44)])
        self.satellite = Satellite((0, 0), (self.state[2] * np.cos(np.pi * self.state[3] / 180),
                                            self.state[2] * np.sin(np.pi * self.state[3] / 180)))
        self.x = 0
        self.y = 0
        self.episode_len = 0
        self.plot = [tuple([self.x, self.y])]
        return self.state

def main():
    env = SpaceshipMove()
    env.reset()

    LEARNING_RATE = 0.1
    DISCOUNT = 0.95
    EPISODES = 25000

    SHOW_EVERY = 2

    # make the discrete values table: 25 values for x and y coordinates and 15 values for the heading
    DISCRETE_OS_SIZE = [100, 100, 1000, 72]
    discrete_os_win_size = (env.observation_space.high - env.observation_space.low) / DISCRETE_OS_SIZE

    EPSILON = 0.5
    START_EPSILON_DECAYING = 1
    END_EPSILON_DECAYING = EPISODES // 2
    EPSILON_DECAY_VALUE = EPSILON / (END_EPSILON_DECAYING - START_EPSILON_DECAYING)

    # form the q-table using numpy
    q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_OS_SIZE + [env.action_space.n]))

    def get_discrete_state(state: np.array, num_states: list) -> tuple:
        discrete_state = (state - env.observation_space.low) / discrete_os_win_size
        returnTuple = tuple(discrete_state.astype(np.int))
        for idx, val in enumerate(num_states):
            if returnTuple[idx] == val:
                returnTuple[idx] == val - 1
        return tuple(returnTuple)

    for episode in range(EPISODES):
        render = True if episode % SHOW_EVERY == 0 else False
        discrete_state = get_discrete_state(env.reset(), DISCRETE_OS_SIZE)
        print(env.reset(), discrete_state)
        done = False
        while not done:
            if np.random.random() > EPSILON:
                action = np.argmax(q_table[discrete_state])
            else:
                action = np.random.randint(0, env.action_space.n)
            new_state, reward, done, info = env.step(action)
            new_discrete_state = get_discrete_state(new_state, DISCRETE_OS_SIZE)
            if not done:
                max_future_q = np.max(q_table[new_discrete_state])
                current_q = q_table[discrete_state + (action, )]

                new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
                q_table[discrete_state + (action, )] = new_q

            elif env.end_goal():
                q_table[discrete_state][action] = 0

            discrete_state = new_discrete_state
        env.render() if render else None
        if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
            EPSILON -= EPSILON_DECAY_VALUE
    env.close()

if __name__ == '__main__':
    main()