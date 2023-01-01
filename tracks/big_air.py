"""
Track definition for the Vekoma Big Air [1], based on [2].

[1] https://rcdb.com/8656.htm
[2] http://resolver.tudelft.nl/uuid:701f9c34-fc6b-46d2-8beb-c966041bc410
"""

import sys
sys.path.insert(0, "../")
import numpy as np
from numpy.polynomial import Polynomial as P
from pycoaster.curve import UpCurve

x = P([29.11, -174.80,  149.20, -31.67,   0.00])
y = P([48.48,   47.83, -154.60,  88.75, -14.12])

t = np.linspace(*x.deriv(1).roots())

xb, yb = x(t), y(t)

ya = np.linspace(53.25, yb[0], len(t))[:-1]
xa = np.resize(xb[0], ya.shape)

yc = np.flip(ya)
xc = np.resize(xb[-1], yc.shape)

x = np.hstack([xa, xb, xc])
y = np.hstack([ya, yb, yc])
z = np.zeros_like(x)

ga = UpCurve(np.transpose([x, z, y]))

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    ax = ga.plot()
    ax.view_init(elev=0.0, azim=-90.0)
    ax.set_proj_type("ortho")
    ax.set(xlabel="$x$ (m)", zlabel="$y$ (m)")
    plt.show()

