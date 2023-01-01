"""
curve.py

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

from scipy.interpolate import CubicSpline
import numpy as np
from numpy import linalg as LA


class Curve:
    """
    Curve base class
    Uses the Frenet frame [1] as local coordinate frame, with
        x = t; y = b; z = n
    
    Additionally defines methods to plot and save the curve.

    [1] https://en.wikipedia.org/wiki/Frenet-Serret_formulas
    """

    @classmethod
    def path_length(cls, ga):
        s = np.cumsum(np.sqrt(np.sum(np.diff(ga, axis=0)**2, axis=1)))
        return np.array([0.0, *s])

    def __init__(self, ga, ph=None):
        # ga = [x, y, z].T
        # TODO: implement custom bank angle (ph)
        # TODO: improve input flexibility
        # TODO: add support for bc_type=periodic
        cls = self.__class__
        s = cls.path_length(ga)
        self._ga = CubicSpline(s, ga)
        ## we can export the control points (kind of) using
        #ga = self._ga.c[-1]
        self.ph = ph # bank angle (not used)

    # TODO: add other methods from CubicSpline
    def __call__(self, *args, **kwargs): return self._ga(*args, **kwargs)

    @property
    def s(self):
        # curve length at control points
        return self._ga.x

    def t(self, s):
        # tangent vector
        ga1 = self(s, 1)
        return ga1/LA.norm(ga1, axis=-1, keepdims=True)

    def n(self, s):
        # normal vector
        ga1, ga2 = self(s, 1), self(s, 2)
        c = np.cross(ga2, ga1, axis=-1)
        return (np.cross(ga1, c, axis=-1)
                /(LA.norm(ga1, axis=-1, keepdims=True)
                 *LA.norm(  c, axis=-1, keepdims=True)))

    def b(self, s):
        # binormal vector
        ga1, ga2 = self(s, 1), self(s, 2)
        b = np.cross(ga1, ga2, axis=-1)
        return b/LA.norm(b, axis=-1, keepdims=True)

    def ka(self, s):
        # curvature
        ga1, ga2 = self(s, 1), self(s, 2)
        return (LA.norm(np.cross(ga1, ga2, axis=-1), axis=-1)
                *LA.norm(ga1, axis=-1)**-3)

    def ta(self, s):
        # torsion
        ga1, ga2, ga3 = self(s, 1), self(s, 2), self(s, 3)
        return (np.sum(ga1*np.cross(ga2, ga3, axis=-1), axis=-1)
                  *LA.norm(np.cross(ga1, ga2, axis=-1), axis=-1)**-2)

    def x(self, s): return self.t(s) # longitudinal

    def y(self, s): return self.b(s) # lateral/horizontal

    def z(self, s): return self.n(s) # vertical
    
    # TODO: add more representations (e.g., a realistic roller coaster spine)
    # TODO: pass kwargs to matplotlib
    def plot(self, **kwargs):
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection

        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_box_aspect((1, 1, 1))

        s  = np.linspace(0.0, self.s[-1], int(self.s[-1]))
        ga = self(s)
        ax.plot(*ga.T)

        y = self.y(s)
        g0, g1 = ga[:-1], ga[1:]
        y0, y1 =  y[:-1],  y[1:]
        # quadrilaterals
        #verts = np.array([g0 - 0.5*y0, g0 + 0.5*y0, g1 + 0.5*y1, g1 - 0.5*y1])
        # triangles
        verts = np.hstack(([g0 - 0.5*y0, g0 + 0.5*y0, g1 + 0.5*y1],
                           [g0 - 0.5*y0, g1 + 0.5*y1, g1 - 0.5*y1]))
        verts = np.transpose(verts, (1, 0, 2))
        ax.add_collection3d(Poly3DCollection(verts))

        lim = np.array([ax.get_xlim(), ax.get_ylim(), ax.get_zlim()]).T
        #clim = np.mean(lim, axis=0)
        clim = np.mean(ga, axis=0)
        dlim = 0.5*np.max(np.abs(np.diff(lim, axis=0)))
        lim = np.array([clim - dlim, clim + dlim])
        ax.set(xlim=lim[:, 0], ylim=lim[:, 1], zlim=lim[:, 2])

        return ax

    def save(self, fname, s=None,
             fmt="%.4f", delimiter="\t", header=None, comments="", **kwargs):
        # save in a format that can be read by NoLimitsCurve
        if s is None:
            s = self.s
        if header is None:
            header = delimiter.join(["No.",
                  "PosX",   "PosY",   "PosZ",
                "FrontX", "FrontY", "FrontZ",
                 "LeftX",  "LeftY",  "LeftZ",
                   "UpX",    "UpY",    "UpZ"])

        n = (np.arange(len(s)) + 1)[:, np.newaxis]
        p =  self  (s)[:, [1, 2, 0]]
        f =  self.x(s)[:, [1, 2, 0]]
        l =  self.y(s)[:, [1, 2, 0]]
        u = -self.z(s)[:, [1, 2, 0]]
        np.savetxt(fname, np.hstack([n, p, f, l, u]), 
                   fmt="%i" + 12*(delimiter + fmt),
                   header=header, comments=comments, **kwargs)


# TODO: up/down right/left vector frame
class UpCurve(Curve):
    """
    Uses the up-vector frame as local coordinate frame.
    In this frame, the vector with the highest z-component
    in the plane orthogonal to the x-vector is picked as the z-vector.

    In terms of the tangent vector t, it is roughly defined as
        x = t
        y = x cross ^z
        z = y cross  x
    where cross is the cross product and ^z = [0, 0, 1].
    
    Alternatively we can also use a right-vector frame
        x =  t
        y =  x cross z
        z = ^y cross x
    where ^y = [0, 1, 0].
    
    Down- and left variations are also possible
    by inverting the signs of y and z (TODO).
    """

    def y(self, s):
        ga1 = self(s, 1)
        y = np.array([ga1[..., 1], -ga1[..., 0], np.zeros_like(s)]).T
        y = np.reshape(y, ga1.shape)
        y = np.sign(ga1[..., 0, np.newaxis])*y # right-vector frame?
        return y/LA.norm(y, axis=-1, keepdims=True)

    def z(self, s):
        ga1 = self(s, 1)
        z = -ga1[..., 2, np.newaxis]*ga1
        z[..., 2] += LA.norm(ga1, axis=-1)**2
        z = np.sign(ga1[..., 0, np.newaxis])*z # right-vector
        return z/LA.norm(z, axis=-1, keepdims=True)


# TODO: generalize this class to be used with other finite methods
class NoLimitsCurve(Curve):
    """
    Uses a csv file exported from the NoLimits 2 game. Units are in meters.

    It is possible to export csv files from NoLimits 2 using either
    the Professional version of the game [1] or nolimits2-csv-exporter [2].
    I've only been able to test the class using the latter.

    nolimits2-csv-exporter has some funky behavior.
    Therefore, additional data processing is performed on the file.
    This ensures all vectors are of unit length and orthogonal at all times.

    This also means that the file contents may change when writing to disk.
    It is therefore not recommended to overwrite files directly.
    The track itself should remain unchanged when reading and writing.

    In terms of the vertical vector z' from the csv and the tangent vector,
        x = t
        y = x cross z'
        z = y cross x
    where cross is the cross product.

    [1] https://www.nolimitscoaster.com/
    [2] https://github.com/Buam/nolimits2-csv-exporter
    """
    
    def __init__(self, fname, skip_header=1, **kwargs):
        # clean up data using skip_header and skip_footer
        data = np.genfromtxt(fname, skip_header=skip_header, **kwargs)

        # TODO: compute distance and pick steps accordingly
        #if bc_type == "periodic" and not np.allclose(data[-1], data[0]):
        #    data = np.array([*data, *np.linspace(data[-1], data[0])[1:]])
        #    #data = np.array([*data, data[0]])
        
        ga =  data[:, [ 3,  1,  2]]
        # x is broken/not used
        # y is not used
        z  = -data[:, [12, 10, 11]]
        # clean up data (issue with scientific notation for small numbers)
        z[np.logical_or(np.abs(z) > 1.0, np.isnan(z))] = 0.0

        super().__init__(ga)
        self._z = CubicSpline(self.s, z)

    def y(self, s):
        ga1 = self(s, 1)
        z = self._z(s)
        y = np.cross(ga1, z, axis=-1)
        return y/LA.norm(y, axis=-1, keepdims=True)

    def z(self, s):
        ga1 = self(s, 1)
        z   = self._z(s)
        z  -= np.sum(ga1*z, axis=-1, keepdims=True)*ga1
        return z/LA.norm(z, axis=-1, keepdims=True)


# TODO: add different frames
    
