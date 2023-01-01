"""
Model validation based on [1].

[1] http://resolver.tudelft.nl/uuid:701f9c34-fc6b-46d2-8beb-c966041bc410
"""

import sys
sys.path.insert(0, "../")
from scipy.integrate import solve_ivp
import numpy as np
from pycoaster.curve import UpCurve
from pycoaster.motion import EqsMotion
from tracks.big_air import ga

s = ga.s
ga = ga(s) - ga.z(s)
ga = UpCurve(ga)
s = ga.s

rc = EqsMotion(ga, n=2, c={"cd": 1.6})

def event(t, y):
    s, s1 = y
    return s1 + 1e-8

event.terminal = True
event.direction = 1.0

sol = solve_ivp(rc, [0.0, 20.0], [0.0, 0.0], dense_output=True, events=event)
t = np.linspace(*sol.t[[0, -1]], 500)

y = sol.sol(t)
s, s1 = y

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    g = rc.c["g"]
    m = rc.n*rc.c["m"]
    h = 0.5*m*s1**2 + m*g*rc.ga(s)[..., 2]
    plt.plot(t, h*1e-6, label="PyCoaster")

    t = [0.0, 3.74, 7.48, 10.87, 14.25]
    t = np.array(t) + 1.87
    h = [g*53.25, 0.5*30.05**2, g*45.35, 0.5*27.68**2, g*38.65]
    h = m*np.array(h)
    plt.plot(t, h*1e-6, label="Vekoma")

    plt.xlabel("time $t$ (s)")
    plt.ylabel("total energy $H$ (MJ)")

    plt.grid()
    plt.legend()
    #plt.savefig("validation.png")
    plt.show()

