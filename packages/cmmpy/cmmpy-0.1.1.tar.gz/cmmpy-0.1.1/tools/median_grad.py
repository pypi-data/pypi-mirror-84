#!/usr/bin/env python3
"""
:This file:

    `script.py`

:Purpose:

    A sample script

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
import sys
import flopy
import numpy as np

file_in = sys.argv[1]

head = flopy.utils.HeadFile(file_in).get_data()


h = head[0][:,:]

h_min = np.floor(np.min(h))
h_max = np.floor(np.max(h))

gradx, grady = np.gradient(h)
grad = np.hypot(gradx, grady)

print("h_min", h_min)
print("h_max", h_max)

Mgrad = np.median(grad)


print("grad (median): {0:.2e}".format(Mgrad))
