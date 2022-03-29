#!/usr/bin/env python-sirius

"""Phase Space."""

import numpy as np
import matplotlib.pyplot as plt

# pyaccel is a package developed by FAC that is used for modelling accelerators
# and to do tracking and calculation of optical functions. this package
# requires our tracking code packge written in c++ called trackcpp
# https://github.com/lnls-fac/trackcpp
# https://github.com/lnls-fac/pyaccel

import pyaccel

# pymodels is a package written by FAC with current Sirius accelerator models.
# it uses the general pyaccel package to define Sirius accelerator's lattices.
# the package defines convenient symbols so that users can more easily access
# package and subpackages modules, functions classes. for example, 'si' symbol
# imported bellow access code related to srius storage rinf. 'bo' for booster,
# 'li' for linac, and so on...
# https://github.com/lnls-fac/pymodels

from pymodels import si


def run_tracking(model, rx0, elements):
    """."""
    mm2m = 1e-3
    # initial particle position
    px0 = 0.0* mm2m  # horizontal angle [rad]
    ry0 = 0.0* mm2m  # vertical pos [m]
    py0 = 0.0* mm2m  # vertical angle [rad]
    de0 = 0.0* mm2m  # relative energy deviation
    dl0 = 0.0* mm2m  # longitudinal deviation [m]
    pos = [rx0, px0, ry0, py0, de0, dl0]

    # track one turn from initial condition
    traj, *_ = pyaccel.tracking.line_pass(model, pos, indices='open')
    traj_init = traj[:, elements]  # select traj pos at required elements

    nrturns = 1000
    traj = np.zeros((len(elements), 6, nrturns+1))
    # track nrturns
    for idx, elem in enumerate(elements):
        pos = traj_init[:, idx]
        traj_, *_ = pyaccel.tracking.ring_pass(model, pos, nrturns, turn_by_turn=True, element_offset=elem)
        traj[idx, :, :] = traj_

    return traj


def plot_phase_space(model, rx0):
    """."""
    # select where in the ring trajectory is to be plotted in phase space
    elements = [0, 1000, 2100]
    spos = pyaccel.lattice.find_spos(model, indices='open')

    # do tracking
    traj = run_tracking(model, rx0=rx0, elements=elements)

    m2mm = 1e3
    m2um = rad2urad = 1e6
    # plot trajectory in phase space
    for idx, ele in enumerate(elements):
        fam_name = '{} @ {:.3f} m'.format(model[ele].fam_name, spos[ele])
        rx, px = m2um * traj[idx, 0, :], rad2urad * traj[idx, 1, :]
        plt.plot(rx, px, '.', label=fam_name)
    plt.legend()
    plt.xlabel('rx [um]')
    plt.ylabel('px [urad]')
    plt.title(f'Trajectory in Phase Space, x0 = {m2mm*rx0:.2f} mm\n(at different ring positions)')
    plt.show()
    
    
# create SI model
model = si.create_accelerator()

# turn longitudinal dynamics off (purely symplectic transverse dynamics)
model.cavity_on = False
model.radiation_on = False


if __name__ == '__main__':
    # small action (ellipses in phase space)
    plot_phase_space(model, rx0=-1.0/1000)
    # large action (distorted ellipses)
    plot_phase_space(model, rx0=-8.0/1000)
    
    





