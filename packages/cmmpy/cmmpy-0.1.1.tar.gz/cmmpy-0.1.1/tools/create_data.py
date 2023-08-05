#!/usr/bin/env python3
"""
:This file:

    `create_data.py`

:Purpose:

    Create a VTK file containing some input head data
    with linear BCs.

:Usage:

    Explain here how to use it.

:Parameters:

:Version:

    0.1 , YYYY-MM-DD :

        * First version

:Authors:

    Alessandro Comunian

.. notes::

.. warning::

.. limitations::



"""
import numpy as np
import sys
import matplotlib.pylab as pl
from mpl_toolkits.mplot3d import Axes3D

# This is the orientation in degrees
degN = float(sys.argv[1])
# This is h jump for 1 [m]
hj = float(sys.argv[2])

radN = degN*np.pi/180.0

print("    Rotation (degree, North):", degN)
nx = 57
ny = 40
dx = 25
dy = 25
ox = 0.0
oy = 0.0



nxy = np.max((nx, ny))

midx = 0.5*(ox + nx*dx)
midy = 0.5*(oy + ny*dy)
h_center = 100


point  = np.array([0., 0.0, 0.0])
#point  = np.array([midx, midy, h_center])
#normal = np.array([0,1,1])
normal = np.array([np.cos(radN),np.sin(radN),1/hj])


print("    Size of the squared domain:", nxy)

# a plane is a*x+b*y+c*z+d=0
# [a,b,c] is the normal. Thus, we have to calculate
# d and we're set
d = -point.dot(normal)





# create x,y
xx, yy = np.meshgrid(range(nxy), range(nxy))

# calculate corresponding z
z = (-normal[0] * xx - normal[1] * yy - d) * 1. /normal[2]

# Compute the gradient of z
gradx, grady = np.gradient(z)

print("gradx", gradx[0,0], "grady", grady[0,0])

# Shift according to the "h_center" variable
z = z+(h_center-np.mean(z))

print(np.mean(z))




# # Create the figure
# fig = pl.figure()

# # Add an axes
# ax = fig.add_subplot(111, projection='3d')

# # plot the surface
# ax.plot_surface(xx, yy, z1, alpha=0.2)
# ax.plot_surface(xx, yy, z2, alpha=0.2)
# ax.set_xlabel("x")
# ax.set_ylabel("y")

# # and plot the point 
# #ax.scatter(point2[0] , point2[1] , point2[2],  color='green')
# pl.show()


pl.imshow(z, origin="lower")
pl.xlabel("x")
pl.ylabel("y")
#pl.show()

# Save the VTK used as input file...


np.savetxt("ciccio.txt", np.ravel(z[:,9:-8], order="F"), fmt="%.6e")
