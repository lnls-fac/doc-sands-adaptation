#!/usr/bin/env python-sirius

"""Tracking envelope."""

import numpy as np
import matplotlib.pyplot as plt
from pymodels import si
import pyaccel


def run_tracking(model):
    """."""
    # calc optics from model
    twiss, *_ = pyaccel.optics.calc_twiss(model, indices='closed')

    # initial particle position
    rx0 = 0.1 / 1000  # horizontal pos[m]
    px0 = 0.0 / 1000  # horizontal angle [rad]
    ry0 = 0.0 / 1000  # vertical pos [m]
    py0 = 0.0 / 1000  # vertical angle [rad]
    de0 = 0.0 / 100   # relative energy deviation
    dl0 = 0.0 / 1000  # longitudinal deviation [m]
    pos = [rx0, px0, ry0, py0, de0, dl0]

    action = rx0**2/twiss.betax[0]
    envelop = np.sqrt(twiss.betax * action)

    # tracking
    nrturns = 10
    traj_turns = list()
    for n in range(nrturns):
        traj, *_ = pyaccel.tracking.line_pass(model, pos, indices='closed')
        traj_turns.append(traj)
        # take particle pos at end of turn as initial condiction for next turn
        pos = traj[:,-1]
    
    return twiss, envelop, traj_turns
    

def plot_envelope(model):
    """."""
    twiss, envelop, traj_turns = run_tracking(model)
    rx0 = traj_turns[0][0,0]

    for n in range(len(traj_turns)):
        rx = traj_turns[n][0, :]
        plt.plot(twiss.spos, 1e6*rx, '-.', label=f'Turn {n}')
    label = r'Envelope $\propto \sqrt{\beta(s)}$'
    plt.plot(twiss.spos, +1e6*envelop, color='k', label=label)
    plt.plot(twiss.spos, -1e6*envelop, color='k')
    plt.xlim([0, model.length/10])
    plt.xlabel('pos [m]')
    plt.ylabel('rx [um]')
    title = 'Horizontal position from Tracking\n' + \
        f'(Envelope function defined by initial condition x = {1e6*rx0:.0f} um)'
    plt.title(title)
    plt.legend()
    plt.show()
    
        
# create SI model
model = si.create_accelerator()

# refine elemts in the model
model = pyaccel.lattice.refine_lattice(model, 0.05)

# turne longitudinal dynamics off
model.cavity_on = False
model.radiation_on = False


if __name__ == '__main__':
    plot_envelope(model)
    





