"""
motion.py

Copyright (C) 2022, 2023 Luuk Tijssen <info@luuktijssen.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import numpy as np
#from pycoaster.curve import Curve


class EqsMotion:
    """
    Equations of motion base class
    Default values and validation based on [1].
    
    [1] http://resolver.tudelft.nl/uuid:701f9c34-fc6b-46d2-8beb-c966041bc410
    """

    def __init__(self, ga, n, v=np.zeros(3), c=None):

        # TODO: more checks?
        assert n >= 1
        assert np.shape(v) == (3,)

        self.ga = ga # Curve object
        self.n  = n  # no. of coaches in a train
        self.v  = np.array(v) # m/s, wind speed (not used)
        self.c  = {  # physical constants (defaults)
        #   symbol value    unit  description
            "a"  : 3.0,   # m2    train frontal surface area
            "cd" : 0.8,   #       drag coeff.
            "crr": 0.01,  #       rolling resistance coeff.
            "ds" : 4.9,   # m     coach distance
            "f"  : 4.7e3, # N     wheel set spring load (not used)
            "g"  : 9.81,  # m/s2  gravitational accel.
            "m"  : 5.1e3, # kg    coach mass (empty)
            "rh" : 1.2,   # kg/m3 air mass density
        }
        if c is not None:
            self.c.update(c)

    # TODO: clean up or deprecate this function
    def si(self, s):
        ds = np.arange(self.n)*self.c["ds"]
        ds = ds - 0.5*ds[-1]
        return np.expand_dims(s, -1) + ds

    def ag(self, s, s1=None):
        # gravitational acceleration
        return np.resize([0.0, 0.0, self.c["g"]], (*np.shape(s), 3))

    def ac(self, s, s1):
        # centripetal acceleration
        ac = s1**2*self.ga.ka(s)
        return ac[..., np.newaxis]*self.ga.n(s)
        
    def an(self, s, s1):
        # normal acceleration
        a = self.ag(s, s1) + self.ac(s, s1)
        x = self.ga.x(s)
        return a - np.sum(a*x, axis=-1, keepdims=True)*x

    def ad(self, s, s1):
        # drag
        v  = s1 # assume self.v = 0
        fd = np.sign(v)*0.5*self.c["rh"]*v**2*self.c["cd"]*self.c["a"]
        ad = fd/self.c["m"]
        return ad[..., np.newaxis]*self.ga.x(s)

    def arr(self, s, s1):
        # rolling resistance
        an  = np.linalg.norm(self.an(s, s1), axis=-1)
        arr = np.sign(s1)*self.c["crr"]*an
        return arr[..., np.newaxis]*self.ga.x(s)
    
    def af(self, s, s1):
        # friction term
        return self.ad(s, s1) + self.arr(s, s1)

    def aa(self, s, s1):
        # total acceleration
        return self.ag(s, s1) + self.ac(s, s1) + self.af(s, s1)

    def ax(self, s, s1):
        # longitudinal acceleration
        si = self.si(s)
        s1 = s1[..., np.newaxis]
        ax = -np.sum(self.aa(si, s1)*self.ga.x(si), axis=-1)
        ax =  np.average(ax, axis=-1)
        return ax

    def ay(self, s, s1):
        # lateral/horizontal acceleration
        return np.sum(self.aa(s, s1)*self.ga.y(s), axis=-1)

    def az(self, s, s1):
        # vertical acceleration
        return np.sum(self.aa(s, s1)*self.ga.z(s), axis=-1)

    def fun(self, t, y):
        s, s1 = y
        s2 = self.ax(s, s1)
        return s1, s2
        
    def __call__(self, t, y):
        return self.fun(t, y)

