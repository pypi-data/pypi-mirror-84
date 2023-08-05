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

    `tools.py`

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
import os
import matplotlib.pylab as pl
import matplotlib 
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm
import scipy.stats as ss
import logging
import flopy

# This is to generate the heterogeneous K
import gstools as gs


# create logger
module_logger = logging.getLogger('cmmpy.tools')

# Default resolution for raster images output
DPI = 400

# Order of the numpy.gradient approximation for the edges
edge_order = 2

# This is for fixed imshow representations of T
fixed_odg_T = 2

# Some settins useful for the fonts
matplotlib.rcParams['mathtext.fontset'] = 'custom'
matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
matplotlib.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
matplotlib.rcParams['mathtext.bf'] = 'Bitstream Vera Sans:bold'
pl.rc('text', usetex=True)
pl.rc('text.latex', preamble=r'\usepackage{siunitx}')

def plot_h(h, modelname, out_dir="out", mode="ref", extent=None, ptype="imshow", mask=None):
    """
    A function to plot the hydraulic head fields
    """
    h = np.transpose(h[0,:,:])
    if mask is not None:
        mask=np.transpose(mask)
        h = np.ma.array(h, mask=mask)
        
    mode_opt = {}
    name_opt = {}
    mode_opt["ref"] = "$h^\mathrm{(ref)}$ ($\si{m}$)"
    mode_opt["BCs"] = "Fixed $h$ BCs ($\si{m}$)"
    name_opt["ref"] = "ref"
    name_opt["fwd"] = "fwd"
    name_opt["BCs"] = "BCs"    
    
    h_min = np.floor(np.min(h))
    h_max = np.floor(np.max(h))   
    
    ax = pl.subplot(111, aspect="equal")
    ax.set_title(mode_opt[mode])
    divider = make_axes_locatable(ax)
    if ptype=="imshow":
        im = ax.imshow(h, origin="lower", interpolation="none")
        cax = divider.append_axes("right", size="5%", pad=0.05)
        ax.set_xlabel("cells along $x$")
        ax.set_ylabel("cells along $y$")
        pl.colorbar(im, cax=cax)
        file_name = os.path.join(out_dir, '{0}_h_{1}.png'.format(modelname, name_opt[mode]))
        module_logger.info('Writing h_{0} into file "{1}" (imshow)'.format(mode, file_name))
        pl.savefig(file_name, dpi=DPI)
        
    elif ptype=="contour":
        levels = np.linspace(h_min, h_max, int((h_max-h_min)*4)+1)
        cs = ax.contour(np.flipud(h), levels=levels, extent=extent)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        ax.clabel(cs, fmt="%.2f")
        ax.set_xlabel("$x$ ($\si{m}$)")
        ax.set_ylabel("$y$ ($\si{m}$)")
        cax.remove()
        #        pl.colorbar(cs, cax=cax)
        file_name = os.path.join(out_dir, '{0}_h_{1}-contour.png'.format(modelname, name_opt[mode]))
        module_logger.info('Writing h_{0} into file "{1}" (contour)'.format(mode, file_name))
        pl.savefig(file_name, dpi=400)
    else:
        module_logger.warning("WARNING: Wrong option in 'plot_h'")
    pl.close()

    
def plot_h_mds(h, modelname, out_dir="out", mode="ref", extent=None, ptype="imshow", mask=None):
    """
    Version to be used for a multiple data set
    """
    for i, hh in enumerate(h):
        plot_h(hh, modelname, "{0}_ds{1}".format(out_dir, i), mode=mode, ptype=ptype, mask=mask)




    
def plot_t(t, modelname, out_dir="out", mode="ref", it=0, minmax=None, mask=None):
    """
    A function to plot the T fields
    """


    
    mode_opt = {}
    mode_opt["ref"] = "$T^\mathrm{(ref)}$ ($\si{m^2/s}$)"
    mode_opt["iter"] = "$T^\mathrm{{{0}}}$ ($\si{{m^2/s}}$)".format(it)
    name_opt = {}
    name_opt["ref"] = "ref"
    name_opt["iter"] = "iter{0:03d}".format(it)

    t = np.transpose(t[0,:,:])
    mask = np.transpose(mask)

    if mask is not None:
        t = np.ma.array(t, mask=mask)

    if minmax is None:
        t_min = np.min(t)
        t_max = np.max(t)
    else:
        t_min = minmax[0]
        t_max = minmax[1]
        
    ax = pl.subplot(111)
    ax.set_title(mode_opt[mode])
    im = ax.imshow(t, origin="lower",
                   norm=LogNorm(vmin=t_min, vmax=t_max),
                   interpolation="none")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    ax.set_xlabel("cells along $x$")
    ax.set_ylabel("cells along $y$")
    pl.colorbar(im, cax=cax)
    pl.savefig(os.path.join(out_dir, '{0}_T_{1}.png'.format(modelname, name_opt[mode])), dpi=DPI)
    pl.close()

def plot_t_mds(t, nb_ds, modelname, out_dir="out", mode="ref", it=0, minmax=None, mask=None):
    """
    Plot T fields when multiple data are available.
    """
    if mode=="ref":
        for i in range(nb_ds):
            plot_t(t, modelname, os.path.join(out_dir, "ds{0:03d}".format( i)), mode, it, minmax, mask)
    else:
        for i, tt in enumerate(t):
            plot_t(tt, modelname,  os.path.join(out_dir, "ds{0:03d}".format( i)), mode, it, minmax, mask)
        

def plot_A(A, out_dir="out", it=0):
    """
    A function to plot the Anomaly (h_ref - h_cm[i])
    """

    A_max = np.max(np.abs(A))
    
    ax = pl.subplot(111)
    ax.set_title("$A^{{{0}}}$ ($\si{{m}}$)".format(it))
    
    im = ax.imshow(A[0,:,:], interpolation="none", vmin=-A_max, vmax=A_max, cmap="PiYG")
    
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    ax.set_xlabel("cells along $x$")
    ax.set_ylabel("cells along $y$")
    pl.colorbar(im, cax=cax)
    pl.savefig(os.path.join("out", out_dir, 'A.png'), dpi=DPI)
    pl.close()    
    

def log_quickstat(x, title, mask=None):
    """
    Print out a quick statistic summary about one input matrix.
    """
    if mask is not None:
        x = np.ma.array(x, mask=mask)
    module_logger.info("*** {0} ***".format(title))
    module_logger.info("min    : {0:.2e}".format(np.min(x)))
    module_logger.info("max    : {0:.2e}".format(np.max(x)))
    module_logger.info("mean   : {0:.2e}".format(np.mean(x)))
    module_logger.info("median : {0:.2e}".format(np.ma.median(x)))


def mod_grad(data):
    """
    Compute the absolute value of the gradient of a 2D
    variable.
    
    Parameters:
        data: 2D numpy array
            Array containing the variable
    Returns:
        A 2D numpy array containing the result.

    ATTENZIONE: CONTROLLARE CHE VENGA TENUTO CONTO ANCHE DELLA DISCRETIZZAZIONE!
    """
    # Compute the gradient
    data_grad = np.gradient(data,2, edge_order=edge_order) # ATTENZIONE, VERIFICARE!
    # SE SI VEDE LA DOCUMENTAZIONE DI GRAD, È POSSIBILE ANCHE SPECIFICARE IL DX E IL DY... QUINDI IL 2 NON È DETTO CHE SIA L'ASSE
    # PERCHÈ AVEVO MESSO 2?
    # Compute the absolute value
    out = np.ma.sqrt(data_grad[0]**2+data_grad[1]**2)
    
    return out, data_grad

def mod_grad2(gcol, grow):
    """
    Compute the absolute value of the gradient of a 2D
    variable.
    
    Parameters:
        data: 2D numpy array
            Array containing the variable
    Returns:
        A 2D numpy array containing the result.
    """
    # Compute the absolute value
    out = np.hypot(gcol, grow)
    
    return out


def plot_diagn(diagn, out_dir="out"):
    """
    Draw some diagnostic plots...
    """
    it = np.arange(1, diagn["lmbd"].size+1)
    fig, ax = pl.subplots(2,2, sharex=True)#, figsize=(8.0, 4.0))
    #  # Anomaly
    # ax[0].plot(it, diagn["anomaly"], "-o")
    # ax[0].set_xlabel("iteration")
    # ax[0].set_title("$\sum_{i,j} A_{i,j}$")
    # x0, x1 = ax[0].get_xlim()
    # y0, y1 = ax[0].get_ylim()
    # ax[0].set_aspect((x1-x0)/(y1-y0))

    
    ax[0,0].plot(it, diagn["lmbd"], "-o")
 #   ax[0,0].set_xlabel("iteration")
    ax[0,0].set_title("a) $\lambda$")
    x0, x1 = ax[0,0].get_xlim()
    y0, y1 = ax[0,0].get_ylim()
    ax[0,0].set_aspect((x1-x0)/(y1-y0))

    
    ax[0,1].plot(it, diagn["lmbd_abs"], "-o")
#    ax[0,1].set_xlabel("iteration")
    ax[0,1].set_title("b) $|\lambda|$")
    x0, x1 = ax[0,1].get_xlim()
    y0, y1 = ax[0,1].get_ylim()
    ax[0,1].set_aspect((x1-x0)/(y1-y0))
    
    ax[1,0].plot(it, diagn["lmbd2"], "-o")
    ax[1,0].set_xlabel("iteration")
    ax[1,0].set_title("d) $\lambda^2$")
    x0, x1 = ax[1,0].get_xlim()
    y0, y1 = ax[1,0].get_ylim()
    ax[1,0].set_aspect((x1-x0)/(y1-y0))


    nb_ds = len(diagn.keys())-3
    for i in range(nb_ds):
        ax[1,1].plot(it, diagn["a{0}".format(i)], "-o", label="data set {0}".format(i+1))
    ax[1,1].set_xlabel("iteration")
    ax[1,1].set_title("d) anomaly")
    x0, x1 = ax[1,1].get_xlim()
    y0, y1 = ax[1,1].get_ylim()
    ax[1,1].set_aspect((x1-x0)/(y1-y0))
    ax[1,1].legend()

    pl.xticks(it, it)

    file_out = os.path.join(out_dir, "diagnostic.png")
    module_logger.info('Writing diagnostic file "{0}"'.format(file_out))
    pl.tight_layout()
    pl.savefig(file_out, dpi=DPI)
    pl.close()


def fill_ma(mat):
    """
    Fill a matrix with some missing data.  Actually, the missing
    values are filled using a nearest neighborhood interpolation
    algorithm.
    
    This is made to solve some problem when gradients are computed on 
    masked arrays...

    """
    from scipy import interpolate

    
    x = np.arange(0, mat.shape[1])
    y = np.arange(0, mat.shape[0])
    #mask invalid values
    xx, yy = np.meshgrid(x, y)
    #get only the valid values
    x1 = xx[~mat.mask]
    y1 = yy[~mat.mask]
    newarr = mat[~mat.mask]
    
    GD1 = interpolate.griddata((x1, y1), newarr.ravel(),
                               (xx, yy),
                               method='nearest')
    return GD1


def plot_domain(data, out_dir, par, ds=None):
    """
    Plot a map of the domain.
    """

    lx = par["fwd"]["nx"]*par["fwd"]["dx"]
    ly = par["fwd"]["ny"]*par["fwd"]["dy"]
    dx = par["fwd"]["dx"]
    dy = par["fwd"]["dy"]    

    ax = pl.subplot(111, aspect="equal")
    ax.set_title("Domain geometry")
    ax.set_xlabel("$x$ (m)")
    ax.set_ylabel("$y$ (m)")
    cmap = pl.cm.get_cmap('Accent', 3)
    im = ax.imshow(np.transpose(data), cmap=cmap, vmin=1, vmax=3, extent=(0.0,lx,0.0,ly ))
    if ds is not None:
        # Plot domain is used to plot data for a specific data set,
        # therefore well locations should be included
        for i, well in enumerate(par["fwd"]["data_sets"][ds]["wells_ID"]):
            y, x = par["fwd"]["data_sets"][ds]["wells_loc"][i][1:]
            ax.scatter(x*dx,ly-y*dy, marker="x", c="yellow")
            ax.text(x*dx,ly-y*dy, par["fwd"]["data_sets"][ds]["wells_ID"][i], c="yellow")

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = pl.colorbar(im, cax=cax)
    cbar = pl.colorbar(im, cax=cax, ticks=[1.33, 2, 2.66])    
    cbar.ax.set_yticklabels(['E', 'D', 'I'])
#    module_logger.info('Plotted domain shape into file "domain_shape.png".')
#    pl.show()
    pl.savefig(os.path.join(out_dir, "domain_shape.png"), dpi=DPI)
    pl.savefig(os.path.join(out_dir, "domain_shape.pdf"))    
    pl.close()


def plot_domain_sol(data, out_dir):
    """
    Plot the area of the grid where the CMM is applied.
    """
    ax = pl.subplot(111, aspect="equal")
    ax.set_title("Solution domain")
    ax.set_xlabel("cells along $x$")
    ax.set_ylabel("cells along $y$")
    cmap = pl.cm.get_cmap('Accent', 2)
    ax.imshow(np.transpose(data), origin="lower", cmap=cmap)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cax.remove()
    module_logger.info('Plotted domain where to solve FP into file "domain_solution.png".')    
    pl.savefig(os.path.join(out_dir, "domain_solution.png"), dpi=DPI)
    pl.close()

def plot_grad(gr, modelname, out_dir="out", mode="cm",  it=0, mask=None):
    """
    A function to plot the gradients
    """
    mode_opt = {}
    mode_opt["ref"] = "|grad(h\_ref)|"
    mode_opt["cm"] = "grad h CM, iter{0:03d}".format(it)
    name_opt = {}
    name_opt["ref"] = "h_ref"
    name_opt["cm"] = "h_cm-iter{0:03d}".format(it)
    

    gr = np.transpose(gr)
    mask = np.transpose(mask)

    if mask is not None:
        gr = np.ma.array(gr, mask=mask)
        
    ax = pl.subplot(111)
    ax.set_title(mode_opt[mode])
    im = ax.imshow(gr, origin="lower", interpolation="none")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    ax.set_xlabel("cells along $x$")
    ax.set_ylabel("cells along $y$")
    pl.colorbar(im, cax=cax)
    pl.savefig(os.path.join(out_dir, '{0}_grad_{1}.png'.format(modelname, name_opt[mode])), dpi=DPI)
    pl.close()
    


def plot_t_err(t_ref, t_cm, modelname, out_dir="out", it=0, mask=None):
    """
    A function to plot the error on T fields (log10(T_ref)-log10(T_CM))
    """

    t_ref = np.transpose(t_ref[0,:,:])
    t_cm = np.transpose(t_cm[0,:,:])
    mask = np.transpose(mask)

    if mask is not None:
        t_ref = np.ma.array(t_ref, mask=mask)
        t_cm = np.ma.array(t_cm, mask=mask)


    err = np.log10(t_ref)-np.log10(t_cm)
    err_abs = np.abs(err)
    ax = pl.subplot(111)
    ax.set_title("$\log(T^\mathrm{{(ref)}})-\log(T^\mathrm{{{0}}})$".format(it))
    im = ax.imshow(err, origin="lower", vmin=-np.max(err_abs),
                   vmax=np.max(err_abs), interpolation="none",
                   cmap="Spectral")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    ax.set_xlabel("cells along $x$")
    ax.set_ylabel("cells along $y$")
    pl.colorbar(im, cax=cax)
    pl.savefig(os.path.join(out_dir, '{0}_Terr_iter{1:03d}.png'.format(modelname, it)), dpi=DPI)
    pl.close()


def plot_t_err2(t_ref, t_cm, modelname, out_dir="out", it=0, mask=None, scale="fixed"):
    """
    A function to plot the error on T fields (log10(T_ref)-log10(T_CM))
    """

    t_ref = t_ref[0,:,:]
    t_cm = t_cm[0,:,:]
    # mask = np.transpose(mask)

    # if mask is not None:
    #     t_ref = np.ma.array(t_ref, mask=mask)
    #     t_cm = np.ma.array(t_cm, mask=mask)

    if scale == "fixed":
        vmin  = -fixed_odg_T
        vmax  = fixed_odg_T
    elif scale == "symmetric":
        vmax = np.max(err_abs)
        vmin = -vmax



    err = np.log10(t_ref)-np.log10(t_cm)
    err_abs = np.abs(err)
    ax = pl.subplot(111)
    ax.set_title("$\log(T^\mathrm{{(ref)}})-\log(T^\mathrm{{{0}}})$".format(it))
    im = ax.imshow(err, vmin=vmin, vmax=vmax, interpolation="none",
                   cmap="Spectral")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    ax.set_xlabel("cells along $x$")
    ax.set_ylabel("cells along $y$")
    pl.colorbar(im, cax=cax)


    pl.savefig(os.path.join(out_dir, '{0}_Terr_iter{1:03d}.png'.format(modelname, it)), dpi=DPI)
    pl.close()
    np.save(os.path.join(out_dir, '{0}_Terr_iter{1:03d}.npy'.format(modelname, it)), err)

def plot_t_err3(t_ref, t_cm, modelname, out_dir="out", it=0, mask=None):
    """
    A function to plot the error on T fields (log10(T_ref)-log10(T_CM))
    """

    t_ref = t_ref[0,:,:]
    t_cm = t_cm[0,:,:]
    # mask = np.transpose(mask)

    # if mask is not None:
    #     t_ref = np.ma.array(t_ref, mask=mask)
    #     t_cm = np.ma.array(t_cm, mask=mask)


    err = np.log10(t_ref)-np.log10(t_cm)
    err_abs = np.abs(err)
    
    fig, ax = pl.subplots(2,1,sharex=True)
    ax[0].set_title("$\log(T^\mathrm{{(ref)}})-\log(T^\mathrm{{{0}}})$".format(it))
    im = ax[0].imshow(err, vmin=-np.max(err_abs),
                   vmax=np.max(err_abs), interpolation="none",
                   cmap="Spectral")
    divider = make_axes_locatable(ax[0])
    cax = divider.append_axes("right", size="5%", pad=0.05)
#    ax[0].set_xlabel("cells along $x$")
    ax[0].set_ylabel("cells along $y$")
    pl.colorbar(im, cax=cax)

#    ax[0].set_title("$\log(T^\mathrm{{(ref)}})-\log(T^\mathrm{{{0}}})$".format(it))
    im = ax[1].imshow(err, interpolation="none", cmap="Spectral",
                      vmin=-fixed_odg_T, vmax=fixed_odg_T)
    divider = make_axes_locatable(ax[1])
    cax = divider.append_axes("right", size="5%", pad=0.05)
    ax[1].set_xlabel("cells along $x$")
    ax[1].set_ylabel("cells along $y$")
    pl.colorbar(im, cax=cax)


    pl.savefig(os.path.join(out_dir, '{0}_Terr_iter{1:03d}.png'.format(modelname, it)), dpi=DPI)
    pl.close()
    

def merge_t(t_est, t_old, mode="arithmetic", grad=None, flow=None, mask=None):
    """ 
    Merge the T_est computed with different data sets.
    """
    if mode=="arithmetic":
        out = np.mean(t_est, axis=0)
    elif mode=="geometric":
        out = ss.mstats.gmean(t_est, axis=0)
    elif mode=="harmonic":
        out = ss.mstats.hmean(t_est, axis=0)
    elif mode=="median":
        out = np.median(t_est, axis=0)
    elif mode=="mincorrX":
        # QUESTA È UNA INTERPRETATIONE DIFFERENTE CHE HO DATO IO, NON
        # CORRISPONDE PROPRIAMENTE ALLA MINIMUM CORRECTION
        # Differences between old and new
        comp = np.array([np.abs(t_est[i, :,:,:]-t_old) for i in range(t_est.shape[0])])
#        print(comp.shape)
        # Min of the differences
        comp_min = np.min(comp, axis=0)
        # List of number of elements of each dataset that are <= min
        min_eq = [np.sum( comp[i, :,:,:] <= comp_min) for i in range(comp.shape[0])]
        # Select the index of the data-set with minimum correction.
        # (the one with more elements <= min...)
        id_min = np.argmax(min_eq)
        module_logger.info("Index of the dataset selected by minimum correction: {0}".format(id_min))
        out = t_est[id_min,:,:,:]

        # # Differences between old and new
        # comp = np.array([np.abs(t_est[i, :,:,:]-t_old) for i in range(t_est.shape[0])])
        # print(comp.shape)
        # # Min of the differences
        # comp_min = np.min(comp)
        # # List of number of elements of each dataset that are <= min
        # min_eq = [np.sum( comp[i, :,:,:] <= comp_min) for i in range(comp.shape[0])]
        # # Select the index of the data-set with minimum correction.
        # # (the one with more elements <= min...)
        # id_min = np.argmax(min_eq)
        # module_logger.info("Index of the dataset selected by minimum correction: {0}".format(id_min))
        # out = t_est[id_min,:,:,:]

    elif mode=="mincorr":
        # An array containing the differnces between the estimated and the old T field
        out = np.zeros(t_est[0,:,:,:].shape)
        nb_ds = t_est.shape[0]
        comp = np.array([np.abs(t_est[i, :,:,:]-t_old) for i in range(nb_ds)])
#        for i in range(nb_ds):
#            out = np.where(comp
        coords = np.argmin(comp, axis=0)
        for i in range(coords.shape[0]):
            for j in range(coords.shape[1]):
                for k in range(coords.shape[2]):
                    out[i,j,k] = t_est[coords[i,j,k], i, j, k]
    elif mode=="darcy":
        # ATTENZIONE, QUI DEVO PROBABILMENTE RIVEDERE IL MODO IN CUI
        # SONO CALCOLATI I FLUSSI, PERCHÈ MODFLOW LI RESTITUISCE SOLO
        # PER LE CELLE INTERNE, MENTRE MAGARI PUÒ VALER LA PENA TENER
        # CONTO ANCHE DEGLI ALTRI? MAH, IN PRINCIPIO NON DOVREBBE
        # CAMBIARE GRAN CHE.
        dar_res = darcy_res(t_est, flow, grad)
        dar_res_min = np.min(dar_res, axis=0)
        # List of number of elements of each dataset that are <= min
        min_eq = [np.sum( dar_res[i, :,:,:] <= dar_res_min) for i in range(dar_res.shape[0])]
        # Select the index of the data-set with minimum correction.
        # (the one with more elements <= min...)
        module_logger.info("Cells numbers <= min darcy residuals: {0}".format( min_eq))
        id_min = np.argmax(min_eq) # METTENDO QUI ARGMAX ESCONO COSE CURIOSE...
        module_logger.info("Index of the dataset selected by Darcy's residuals: {0}".format(id_min))
        out = t_est[id_min,:,:,:]
    else:
        module_logger.warning('Selected merging method ("{0}") unknown'.format(mode))
    if mask is not None:
        out = np.ma.array(out, mask=mask)
    return out


def darcy_res(t, flow, grad):
    """
    Compute the Darcy residuals according to formula...
    """

    # Compute the number of data sets
    nb_ds = t.shape[0]
    
    dar_res = np.zeros(t.shape)

    for i in range(nb_ds):
        t_sqrt = np.sqrt(t[i,:,:,:])
#        print(i, flow[i][0].shape, grad[i][0].shape)
        dr_x = flow[i][0][0,:,:]/t_sqrt + t_sqrt/grad[0][i][:,:]
        dr_y = flow[i][1][0,:,:]/t_sqrt + t_sqrt/grad[1][i][:,:]                        
        dar_res[i,:,:,:] = np.hypot(dr_x, dr_y)
    
    return dar_res



# =======================================================
# Here the part related to mf6
# =======================================================



def vtk2Dto_spd_h(par, ds=0):
    """
    Read a VTK file containing 2D data and put the content

    CHIARAMENTE PER IL MOMENTO FORNISCE SOLO DELLE CONDIZIONI DI DIRICHLET.
    """

    # Read an external file containing the shape of the domain
    bcs = np.fliplr(np.transpose(np.loadtxt(os.path.join(par["general"]["data"],
                                                         par["fwd"]["bcs"]),
                                            dtype="U1")))

    h_BCs = np.fliplr(np.transpose(np.loadtxt(os.path.join(par["general"]["data"], par["fwd"]["data_sets"][ds]["h_BCs"]),
         skiprows=10).reshape((par["fwd"]["nx"], par["fwd"]["ny"],1), order="F")))


    jj, ii = np.where(bcs=='D')


    # Define the stress period data
    spd = [[(0,i,j), h_BCs[0,i,j] ] for (i,j) in zip(ii, jj)]

    return spd
    
    
def run_fp(par, spd_h, k, sdir=None, ds=None, noise=False):
    """
    Run a forward problem with mf6.

    Parameters:
        par: dict
            All the input parameters organized as a dictionary
        spd: stress pediod data
            Stress period data as required by the module `ModflowGwfchd`.
            These are the heads used to define the constant head boundary conditions.
        k: The permeability field to be used.
        sdir: This is a "sub-directory" where the problem will be run
           in case this argument is provided.

    NOTA: AL MOMENTO C'È UNA NOTAZIONE UN PO' IBRIDA PER IDENTIFICARE I DATA SET, CHE SI POTREBBERO
    CHIAMARE PER NOME OPPURE PER L'INDICE RELATIVO ALL'ORDINE CON IL QUALE SONO STATI DEFINITI...
    """
    nrow = par["fwd"]["ny"]
    ncol = par["fwd"]["nx"]
    delr = par["fwd"]["dy"]
    delc = par["fwd"]["dx"]

    par_ds = par["fwd"]["data_sets"][ds]

    # Define the directory where the FP will run
    if sdir is not None:
        if ds is not None:
            # We are working with multiple data sets
            fp_ws = os.path.join(par["fwd"]["ws"], sdir, "ds{0:03d}".format(ds))
        else:
            fp_ws = os.path.join(par["fwd"]["ws"], sdir)
    else:
        fp_ws = par["fwd"]["ws"]
    
    # Create a mf6 simulation class
    sim = flopy.mf6.MFSimulation(sim_name=par["fwd"]["name"],
                                 sim_ws=fp_ws,
                                 exe_name=par["fwd"]["exe_name"])

    # Create temporal discretization
    tdis = flopy.mf6.ModflowTdis(sim, time_units="SECONDS")
    
    # Create an Iterative model solution
    ims = flopy.mf6.ModflowIms(sim)
    
    # Create a Groundwater Flow model
    gwf = flopy.mf6.ModflowGwf(sim, modelname=par["fwd"]["name"], save_flows=True)
    
    # Define the discretization for the GFM 
    dis = flopy.mf6.ModflowGwfdis(gwf, length_units="METERS", nrow=nrow, ncol=ncol, delr=delr, delc=delc)
    
    # Define the initial conditions
    ic = flopy.mf6.ModflowGwfic(gwf)

    # Create a template for the K values
    k_template = flopy.mf6.ModflowGwfnpf.k.empty(gwf, False)

    k_template["data"] = np.ravel(k).tolist()

    # Define the node property flow package
    npf = flopy.mf6.ModflowGwfnpf(gwf, pname="npf",
                                  save_specific_discharge=True, k=k_template, icelltype=0,
                                  k33=k_template)

    # Define a constant recharge
    # (flux rate, units are L/T)
    rcha = flopy.mf6.ModflowGwfrcha(gwf, recharge=par_ds["rch"])
    
    # Define the constant heads
    # (ilay, irow, icol)
    chd = flopy.mf6.ModflowGwfchd(gwf,
                                  stress_period_data=spd_h)

    #
    # Define some wells
    # (this is deactivated for the DCM head run)
    #

    #
    
    maxbound = len(par_ds["wells_ID"])

    if maxbound>0:
        # Only if some wells are defined...
        module_logger.info("Found the definition for {0} wells.".format(maxbound))
        
        # First, create and empty stress period data
        stress_prd = flopy.mf6.ModflowGwfwel.stress_period_data.empty(gwf,
                                                                      maxbound=maxbound,
                                                                      boundnames=True,
                                                                      timeseries=True)
        # q: volumetric flow rate, posivive<=>injection.
        for i in range(len(par_ds["wells_ID"])): 
            stress_prd[0][i] = (tuple(par_ds["wells_loc"][i]), par_ds["wells_q"][i], par_ds["wells_ID"][i])
        stress_period_data = {}
        stress_period_data[0] = stress_prd[0]

        wel = flopy.mf6.ModflowGwfwel(gwf, pname='wel', print_input=True,
                                      print_flows=True, maxbound=maxbound,
                                      stress_period_data=stress_period_data,
                                      boundnames=True, save_flows=True)

    else:
        module_logger.warning("No wells defined.")
        
    # Define the names of some useful files
    budget_file = par["fwd"]["name"] + '.bud'
    head_file = par["fwd"]["name"] + '.hds'
    
    # Define the Output control
    oc = flopy.mf6.ModflowGwfoc(gwf, budget_filerecord=budget_file,
                                head_filerecord=head_file,
                                saverecord=[('HEAD', 'ALL'), ('BUDGET', 'ALL')])
    # Write and run
    sim.write_simulation()
    sim.run_simulation(silent=True)
    
    # Get head and budget values
    head = flopy.utils.HeadFile(os.path.join(fp_ws, head_file)).get_data()
    bud = flopy.utils.CellBudgetFile(os.path.join(fp_ws, budget_file),
                                     precision='double')


    # Add noise here!
    if noise:
        if par["noise"]["std"]>0.0:
            head = head + create_noise(par)
        else:
            # Set std=0.0 in the JSON file to deactivate it
            module_logger.warning('Noise option "True", but noise std~0.0.')

    spdis = bud.get_data(text='DATA-SPDIS')[0]
    pmv = flopy.plot.PlotMapView(gwf)

    img = pmv.plot_array(head)
    divider = make_axes_locatable(img.axes)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    pl.colorbar(img, cax)    
    pmv.plot_grid(colors='white')
    levels = np.linspace(np.min(head), np.max(head), 20)
    pmv.contour_array(head, levels=levels, linewidths=1.)
    pmv.plot_specific_discharge(spdis, color='white')
    pl.savefig(os.path.join(fp_ws, par["fwd"]["name"]+".png"), dpi=400)
    pl.close()

    
#    print(head.shape)

    # - QUI POTREI GUARDARE COME FANNO SU get_gradient IN flopy PER TRATTARE CON I MASKED ARRAYS
    # - TIENE CONTO ANCHE DELLA TAGLIA DELLE CELLE...
    gcol, grow = np.gradient(head[0,:,:], delc, delr, edge_order=edge_order)

    # Here compute the module of the gradient
    gmod = mod_grad2(gcol, grow)

    #    m = flopy.modflow.Modflow.load(par["fwd"]["name"]+".nam", model_ws=fp_ws)
    
    # from flopy.utils.postprocessing import get_gradients

    # grad = get_gradients(head, m, nodata=-9999)
    
    return head, gcol, grow, gmod, spdis


def create_t_ref(par):
    # Create a model
    nx = par["fwd"]["nx"]
    ny = par["fwd"]["ny"]
    nlay = par["fwd"]["nlay"]
    
    model = gs.Gaussian(dim=par["t_gen"]["dim"], var=par["t_gen"]["var"],
                        len_scale=par["t_gen"]["len_scale"])
    srf = gs.SRF(model, seed=par["t_gen"]["seed"])
    srf((range(ny), range(nx)), mesh_type='structured')
    t_ref = 10**(srf.field.reshape((nlay, ny, nx), order="F")-2.0)
    return(t_ref)

def create_noise(par):
    # Create a model
    nx = par["fwd"]["nx"]
    ny = par["fwd"]["ny"]
    nlay = par["fwd"]["nlay"]
    
    model = gs.Gaussian(dim=par["noise"]["dim"], var=par["noise"]["std"]**2,
                        len_scale=par["noise"]["len_scale"])
    srf = gs.SRF(model, seed=par["noise"]["seed"])
    srf((range(ny), range(nx)), mesh_type='structured')
    noise = srf.field.reshape((nlay, ny, nx), order="F")
    return(noise)



def plot_t2(t, modelname, out_dir="out", mode="ref", it=0, minmax=None, mask=None):
    """
    A function to plot the T fields
    """


    
    mode_opt = {}
    mode_opt["ref"] = "$T^\mathrm{(ref)}$ ($\si{m^2/s}$)"
    mode_opt["iter"] = "$T^\mathrm{{{0}}}$ ($\si{{m^2/s}}$)".format(it)
    name_opt = {}
    name_opt["ref"] = "ref"
    name_opt["iter"] = "iter{0:03d}".format(it)

    t = t[0,:,:]
    mask = mask

    if mask is not None:
        t = np.ma.array(t, mask=mask)

    if minmax is None:
        t_min = np.min(t)
        t_max = np.max(t)
    else:
        t_min = minmax[0]
        t_max = minmax[1]
        
    ax = pl.subplot(111)
    ax.set_title(mode_opt[mode])
    im = ax.imshow(t, norm=LogNorm(vmin=t_min, vmax=t_max),
                   interpolation="none", cmap="inferno")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    ax.set_xlabel("cells along $x$")
    ax.set_ylabel("cells along $y$")
    pl.colorbar(im, cax=cax)
    pl.savefig(os.path.join(out_dir, '{0}_T_{1}.png'.format(modelname, name_opt[mode])), dpi=DPI)
    pl.close()


def spd4all(par, value):
    """
    """
    spd = {}
    ny = par["fwd"]["ny"]
    nx = par["fwd"]["nx"]    
    out = [((0,i,j), value) for i in range(ny) for j in range(nx)]
    spd[0] = out
    return(spd)


def wells_h4spd(h, par):
    """
    Get the head information as a matrix and, at the well location, put it in a format
    readable as "stress_pediod_data"

    par are the fwd problem parameters
    """

    print(h.shape)
    spd = []
    for i, well in enumerate(par["wells_ID"]):
        loc = tuple(par["wells_loc"][i])
        print(loc)
        spd.append([loc, h[loc]])
    return spd

def randpiezo(h, par, nb):
    """
    Generate a list of random location where to put some piezometers.

    IN REALTÀ BASTEREBBE LEGGERE H PER POI AVERE LE INFO SULLA TAGLIA...

    POI CI SAREBBE DA FARE ATTENZIONE ALLA SOVRAPPOSIZIONE CON I VERI POZZI!

    SE ANCHE AGGIUNGO SOPRA UN POZZO CON FLUSSO NON NULLO, DOPO CONTROLLO
    CHE NON CI SIANO COMUNQUE SOVRAPPOSIZIONI CON LA FUNZIONE
    "check_piezowell_overlap"
    """
    border = 1
    spd = []
    ncol = par["fwd"]["ny"]
    nrow = par["fwd"]["nx"]

    max_rc = (ncol-border*2)*(nrow-border*2)

    if nb > max_rc:
        print("    WARNING: All available nodes selected as piezometers!")
        nb = max_rc

    all_loc = []
    for i in range(border, nrow-border):
        for j in range(border, ncol-border):
            all_loc.append((0, j, i))
            

    # Randomize selection
    np.random.shuffle(all_loc)

    # Here the seleted index
    loc_sel = all_loc[:nb]

    for i in range(nb):
        spd.append([loc_sel[i], h[loc_sel[i]]])

    return(spd)

    
def check_piezowell_overlap(spd_p, spd_w):
    """
    Check if in the list of the randomly created piezometers there is some overallapping with an existing
    well, and in case drop the overap from the list of piezometers.
    """
    loc_wells = [loc[0] for loc in spd_w]

    blacklist = []
    for elem in spd_p:
        if elem[0] in loc_wells:
            print("overlapping", elem)            
            spd_p.remove(elem)


            
    return spd_p    



def spdis2mat(spdis, nrow, ncol):
    """
    """
    ncps = nrow*ncol
    qx = np.zeros((ncps))
    qy = np.zeros((ncps))

    idx = np.array(spdis['node']) - 1
    qx[idx] = spdis["qx"]
    qy[idx] = spdis["qy"]

    qx.shape = (1, nrow, ncol)
    qy.shape = (1, nrow, ncol)
    u = qx[:, :, :]
    v = qy[:, :, :]
    
    return (u, v)


def save_h_vtk(h, par, loc):
    """
    Save a VTK file containing the heads.

    .. warning: This works only in 2D.
    """
    nx = par["fwd"]["nx"]
    ny = par["fwd"]["ny"]
    nlay = par["fwd"]["nlay"]
    dx = par["fwd"]["dx"]
    dy = par["fwd"]["dy"]
    header = ("# vtk DataFile Version 3.4\n"
              "Image\n"
              "ASCII\n"
              "DATASET STRUCTURED_POINTS\n"
              "DIMENSIONS {0:d} {1:d} {2:d}\n"
              "ORIGIN 0.000000 0.000000 0.000000\n"
              "SPACING {3} {4} 1.0\n"
              "POINT_DATA {5}\n"
              "SCALARS h float 1\n"
              "LOOKUP_TABLE default".format(
                  nx, ny, nlay, dx, dy, nx*ny))

    h = np.flipud(h[0,:,:])
    np.savetxt(os.path.join(loc, "h.vtk"), np.c_[np.ravel(h)], header=header, fmt="%.3e", comments="")
    
