#!/usr/bin/env python-sirius

"""Phase Space."""

import numpy as np
import matplotlib.pyplot as plt
from pymodels import si
import pyaccel


def run_tracking(model, rx0, elements):
    """."""
    # initial particle position
    px0 = 0.0 / 1000  # horizontal angle [rad]
    ry0 = 0.0 / 1000  # vertical pos [m]
    py0 = 0.0 / 1000  # vertical angle [rad]
    de0 = 0.0 / 100   # relative energy deviation
    dl0 = 0.0 / 1000  # longitudinal deviation [m]
    pos = [rx0, px0, ry0, py0, de0, dl0]

    # track one turn from initial condition
    traj, *_ = pyaccel.tracking.line_pass(model, pos, indices='open')
    traj_init = traj[:, elements]  # select traj pos at defined elements

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

    # plot trajectory in phase space
    for idx, ele in enumerate(elements):
        fam_name = '{} @ {:.3f} m'.format(model[ele].fam_name, spos[ele])
        rx, px = traj[idx, 0, :], traj[idx, 1, :]
        plt.plot(1e6*rx, 1e6*px, '.', label=fam_name)
    plt.legend()
    plt.xlabel('rx [um]')
    plt.ylabel('px [urad]')
    plt.title(f'Trajectory in Phase Space, x0 = {1e3*rx0:.2f} mm\n(at different ring positions)')
    plt.show()
    
    
# create SI model
model = si.create_accelerator()

# turne longitudinal dynamics off
model.cavity_on = False
model.radiation_on = False


if __name__ == '__main__':
    # small action (ellipses in phase space)
    plot_phase_space(model, rx0=-1.0/1000)
    # large action (distorted ellipses)
    plot_phase_space(model, rx0=-8.0/1000)
    
    





