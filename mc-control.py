#! /usr/bin/env python3

"""
Monte Carlo Control
"""

from env import Easy21
from pprint import pprint
import random
import tqdm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns


C_N0 = 100
C_N_EPISODES = 1_000_000

Q_sa = dict()

N_sa =  dict()
N_s = dict()

for e in tqdm.tqdm(range(C_N_EPISODES)):
    g = Easy21()
    state = g.reset()
    terminal = False

    trajectory = []

    while not terminal:
        N_s[state] = N_s.get(state, 0) + 1
        epsilon_t = C_N0 / (C_N0 + N_s[state])
        action = None

        if random.random() < epsilon_t:
            # Take random action.
            action = random.choice(g.get_actions())
        else:
            # Take optimal action.
            Q_sa[state] = Q_sa.get(state, {"stick": 0, "hit": 0})

            if Q_sa[state]["stick"] > Q_sa[state]["hit"]:
                action = "stick"
            else:
                action = "hit"

        N_sa[state] = N_sa.get(state, {"stick": 0, "hit": 0})
        N_sa[state][action] += 1

        next_state, reward, terminal = g.step(state, action)
        trajectory.append((state, action, reward))
        state = next_state



    G = sum(sar[-1] for sar in trajectory)

    for s, a, r in trajectory:
        Q_sa[s] = Q_sa.get(s, {"stick": 0, "hit": 0})
        alpha_t = 1 / N_sa[s][a]
        Q_sa[s][a] = Q_sa[s][a] + alpha_t * (G - Q_sa[s][a])

columns = ["Player Sum", "Dealer Showing", "Value"]
V_star = pd.DataFrame(columns=columns)

for i, (s, action_val) in enumerate(Q_sa.items()):
    p, d = s
    V_star.loc[i] = [p, d, max(Q_sa[s]["hit"], Q_sa[s]["stick"])]

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_trisurf(V_star['Dealer Showing'], V_star['Player Sum'], V_star['Value'],
                cmap=plt.cm.viridis,
                linewidth=0.2)

ax.view_init(25, 305)
ax.set_ylabel(columns[0])
ax.set_xlabel(columns[1])
ax.set_zlabel(columns[2])
plt.savefig("plots/mc-control.png", dpi=600, transparent=True)
# plt.show()
