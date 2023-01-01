
import sys
sys.path.insert(0, "../")
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from examples.validate import *

fps = 30 # 1/s
frames = np.linspace(*sol.t[[0, -1]], int(sol.t[-1]*fps))
interval = int(1e3/fps) # ms

def update(t):
    s, s1 = sol.sol(t)
    si = rc.si(s)
    ga = rc.ga(si)
    a = 2.5
    x = a*rc.ga.x(si)
    y = a*rc.ga.y(si)
    z = a*rc.ga.z(si)
    gx = np.reshape([ga, ga + x, ga], (-1, 3), order="F")
    lnx.set_data(gx[..., 0:2].T)
    lnx.set_3d_properties(gx[..., 2])
    gy = np.reshape([ga, ga + y, ga], (-1, 3), order="F")
    lny.set_data(gy[..., 0:2].T)
    lny.set_3d_properties(gy[..., 2])
    gz = np.reshape([ga, ga + z, ga], (-1, 3), order="F")
    lnz.set_data(gz[..., 0:2].T)
    lnz.set_3d_properties(gz[..., 2])
    return lnx, lny, lnz

ax = ga.plot()
fig = ax.get_figure()
lnx, = ax.plot([], [], [], c="r", zorder=10)
lny, = ax.plot([], [], [], c="g")
lnz, = ax.plot([], [], [], c="b")

ax.set(xlabel="$x$ (m)", ylabel="$y$ (m)", zlabel="$z$ (m)")

ani = FuncAnimation(fig, update, frames=frames, interval=interval, blit=True)

plt.show()

#ani.save("animation.gif", fps=fps)

