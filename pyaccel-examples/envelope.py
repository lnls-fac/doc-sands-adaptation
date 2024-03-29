#!/usr/bin/env python-sirius

"""Tracking envelope."""

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


def run_tracking(model):
    """."""
    # calc optics from model
    twiss, *_ = pyaccel.optics.calc_twiss(model, indices='closed')

    mm2m = 1e-3
    # initial particle position
    rx0 = 0.1 * mm2m  # horizontal pos[m]
    px0 = 0.0 * mm2m  # horizontal angle [rad]
    ry0 = 0.0 * mm2m  # vertical pos [m]
    py0 = 0.0 * mm2m  # vertical angle [rad]
    de0 = 0.0 * mm2m  # relative energy deviation
    dl0 = 0.0 * mm2m  # longitudinal deviation [m]
    pos = [rx0, px0, ry0, py0, de0, dl0]

    action = rx0**2/twiss.betax[0]
    envelop = np.sqrt(twiss.betax * action)

    # tracking
    nrturns = 10
    traj_turns = list()
    for _ in range(nrturns):
        traj, *_ = pyaccel.tracking.line_pass(model, pos, indices='closed')
        traj_turns.append(traj)
        # take particle pos at end of turn as initial condition for next turn
        pos = traj[:,-1]
    
    return twiss, action, envelop, traj_turns
    

def plot_envelope(model):
    """."""
    twiss, action, envelop, traj_turns = run_tracking(model)
    rx0 = traj_turns[0][0,0]

    m2um = 1e6
    m2nm = 1e9
    for n in range(len(traj_turns)):
        rx = m2um * traj_turns[n][0, :]
        plt.plot(twiss.spos, rx, '-.', label=f'Turn {n}')
    label = r'Envelope $\propto \sqrt{\beta(s)}$'
    plt.plot(twiss.spos, +m2um*envelop, color='k', label=label)
    plt.plot(twiss.spos, -m2um*envelop, color='k')
    plt.xlim([0, model.length/10])
    plt.xlabel('pos [m]')
    plt.ylabel('rx [um]')
    title = 'Horizontal position from Tracking\n' + \
        f'(Envelope function defined by initial' + \
        f' condition x = {m2um*rx0:.0f} um,' + \
        f' J = {action*m2nm:.2f} nm.rad)'
    plt.title(title)
    plt.legend()
    plt.show()
    
        
# create SI model
model = si.create_accelerator()

# refine elements in the model
model = pyaccel.lattice.refine_lattice(model, 0.05)

# turn longitudinal dynamics off
model.cavity_on = False
model.radiation_on = False


if __name__ == '__main__':
    plot_envelope(model)
    





