"""
:License:
    This file is part of cmmpy.

    cmmpy is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    cmmpy is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with cmmpy.  If not, see <https://www.gnu.org/licenses/>.

:This file:

    `cmm.py`

:Purpose:

    A library to support the solution of Inverse Problems (IPs) in
    hydrogeology using the Comparison Model Method (CMM).

    This implementation includes:
    - The possibility to use multiple data sets
    - Uses as Forward Problem (FP) solution engine Modflow6 through Flopy.
    - Usage of irregular domains.

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

.. future developments::

    - Extend to Parflow and Modflow6 (unstructured grids).
    
.. research directions::
    
    - Investigate what happens when the number of iteration increases.
    - Try with a as more tomographic as possible approach, where flow is 
      run along many direction, to check the limits of the methodology.
    - Check different initializations of the Tini.

"""

import numpy as np
import logging
import cmmpy.tools as tools

# create logger
module_logger = logging.getLogger('run_cmm.cmm')

def update_t(h_cm, h_ref, t_est, t_min, t_max, par, mask=None, mode="arithmetic"):
    """
    Update the T of the CMM.

    This is an updated version that allows to handle problems were
    grad(h_ref) is small.

    Parameters:
        h_cm: numpy array, 3D
            The heads computed at the step (k-1) for the
            Comparison Model
        h_ref: numpy array, 3D
            The reference head fields
        t_est: numpy array, 3D
            The t estimated at the step (k-1)
        t_min, t_max: floats
            The allowed range of variability of the
            transmissivity.
        c: float (default None)
            A parameter to "tune" the update step and to
            perform a more cautios updating when gradients are
            small.
            The general formula used to update T is formula (6),
            page 453 of Vassena et al. (2012).
            When the parameter `c` is set to 0.0, then it is like
            putting :math:`\Beta=1` in the aformentioned formula.

    Returns:
        An array containing the t estimated at the step k

    """
    diagn = {}
    # Get the 2D versions of the input variables
    h_cm = h_cm[0,:,:]
    h_ref = h_ref[0,:,:]
    t_est = t_est[0,:,:]
    
    # Compute |grad|
    mod_h_cm, h_cm_grad = tools.mod_grad(h_cm)
    diagn["mod_h_cm"] = mod_h_cm
#    print("mod_h_cm.shape", mod_h_cm.shape)
    mod_h_ref, h_ref_grad = tools.mod_grad(h_ref) # UNA SOLA VOLTA!
    diagn["mod_h_ref"] = mod_h_ref # UNA SOLA VOLTA!

    if mask is not None:
        t_est = np.ma.array(t_est, mask=mask)
        mod_h_cm = np.ma.array(mod_h_cm, mask=mask)
        mod_h_ref = np.ma.array(mod_h_ref, mask=mask) # UNA SOLA VOLTA!


    # QUESTO SI POTREBBE CALCOLARE ANCHE UNA SOLA VOLTA...
    # Correct too low values of the gradient for the CM
    mod_h_ref_OK = np.ma.where(mod_h_ref > par["eps_gradh"], mod_h_ref, par["eps_gradh"] ) # UNA SOLA VOLTA!
#    print(mod_h_ref_OK)
    beta = np.minimum(par["c"]*mod_h_ref_OK, np.ones(mod_h_ref_OK.shape))


    # Correct too low values of the gradient for the CM
    # (this is not as critical as for grad(h_ref))
    mod_h_cm_OK = np.ma.where(mod_h_cm > par["eps_gradh"], mod_h_cm, par["eps_gradh"])
    
    # Save the number of points where the correction is applied
#    diagn["beta_size"] = 100*np.sum(par["c"]*mod_h_ref_OK < np.ones(mod_h_ref_OK.shape))/np.sum(~mask)
    # Update T

    t_new = t_est*(1.0 + beta*(mod_h_cm_OK-mod_h_ref_OK)/mod_h_ref_OK)

    t_new = np.ma.where(t_new > t_max, t_max, t_new)
    t_new = np.ma.where(t_new < t_min, t_min, t_new)
#    if mask is not None:
#        t_new = np.ma.array(t_new, mask=mask)

#    print(type(t_new))

    return t_new.reshape(1, t_new.shape[0], t_new.shape[1]), h_cm_grad[0], h_cm_grad[1]



def beta_size(h_ref, par, mask):
    """
    Compute the % of grad(h_ref) values influenced by the parameter
    Beta (that in turns depends on the CMM parameter "c")

    Parameters:
        h_ref: numpy array, 3D
            The reference head fields
    Returns:
        The % of cells affected by the parameter Beta

    """

    # Get the 2D versions of the input variables
    h_ref = h_ref[0,:,:]

    mod_h_ref, h_ref_grad = tools.mod_grad(h_ref)

    mod_h_ref = np.ma.array(mod_h_ref, mask=mask)

    # Correct too low values of the gradient for the CM
    mod_h_ref_OK = np.ma.where(mod_h_ref > par["eps_gradh"], mod_h_ref, par["eps_gradh"])
    
    # Save the number of points where the correction is applied
    beta_size = 100*np.sum(par["c"]*mod_h_ref_OK < np.ones(mod_h_ref_OK.shape))/np.sum(~mask)

    return beta_size, h_ref_grad[0], h_ref_grad[1]

def beta_size2(gmod_ref, par):
    """
    Compute the % of grad(h_ref) values influenced by the parameter
    Beta (that in turns depends on the CMM parameter "c")

    Parameters:
        h_ref: numpy array, 3D
            The reference head fields
    Returns:
        The % of cells affected by the parameter Beta

    QUI SI POTREBBE FARE IN MODO DI AUTOMATIZZARE LA SCELTA DI C

    """


    # Correct too low values of the gradient for the CM
    gmod_ref_OK = np.ma.where(gmod_ref > par["eps_gradh"], gmod_ref, par["eps_gradh"])
    
    # Save the number of points where the correction is applied
    # "cprop" È LA PERCENTUALE DI PUNTI DOVE VORREMMO CORREGGERE IL GRADIENTE
    q = np.quantile(gmod_ref_OK, par["cprop"])
    c = 1.0/q
    beta_size = 100*np.sum(c*gmod_ref_OK < np.ones(gmod_ref_OK.shape))/gmod_ref_OK.size

    return beta_size, c
    


def update_t2(h_cm, gmod_cm, h_ref, gmod_ref, t_cm, t_minmax, par, ds=None):
    """
    Update the T of the CMM.

    This is an updated version that allows to handle problems were
    grad(h_ref) is small.

    Parameters:
        h_cm: numpy array, 3D
            The heads computed at the step (k-1) for the
            Comparison Model
        h_ref: numpy array, 3D
            The reference head fields
        t_est: numpy array, 3D
            The t estimated at the step (k-1)
        t_min, t_max: floats
            The allowed range of variability of the
            transmissivity.
        c: float (default None)
            A parameter to "tune" the update step and to
            perform a more cautios updating when gradients are
            small.
            The general formula used to update T is formula (6),
            page 453 of Vassena et al. (2012).
            When the parameter `c` is set to 0.0, then it is like
            putting :math:`\Beta=1` in the aformentioned formula.

    Returns:
        An array containing the t estimated at the step k

    """
    #  diagn = {}
    # Get the 2D versions of the input variables
    h_cm = h_cm[0,:,:]
    h_ref = h_ref[0,:,:]
    
    t_cm = t_cm[0,:,:]
    

    # QUESTO SI POTREBBE CALCOLARE ANCHE UNA SOLA VOLTA...
    # Correct too low values of the gradient for the CM
    gmod_ref_OK = np.where(gmod_ref > par["eps_gradh"], gmod_ref, par["eps_gradh"] ) # UNA SOLA VOLTA!
#    print(mod_h_ref_OK)
    beta = np.minimum(par["c"][ds]*gmod_ref_OK, np.ones(gmod_ref_OK.shape))


    # Correct too low values of the gradient for the CM
    # (this is not as critical as for grad(h_ref))
    gmod_cm_OK = np.where(gmod_cm > par["eps_gradh"], gmod_cm, par["eps_gradh"])
    
    # Save the number of points where the correction is applied
#    diagn["beta_size"] = 100*np.sum(par["c"]*mod_h_ref_OK < np.ones(mod_h_ref_OK.shape))/np.sum(~mask)
    # Update T

    t_new = t_cm*(1.0 + beta*(gmod_cm_OK-gmod_ref_OK)/gmod_ref_OK)

    t_new = np.where(t_new > t_minmax[1], t_minmax[1], t_new)
    t_new = np.where(t_new < t_minmax[0], t_minmax[0], t_new)
#    if mask is not None:
#        t_new = np.ma.array(t_new, mask=mask)

#    print(type(t_new))

    return t_new.reshape(1, t_new.shape[0], t_new.shape[1])#, h_cm_grad[0], h_cm_grad[1]
