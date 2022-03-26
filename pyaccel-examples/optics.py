#!/usr/bin/env python-sirius

"""Lattice Optics."""

import matplotlib.pyplot as plt
from pymodels import si
import pyaccel


def plot_optics(model):
    """."""

    # calc optics
    twiss, *_ = pyaccel.optics.calc_twiss(model)

    _, axs = plt.subplots(1, 1, figsize=(10, 5))

    plt.plot(twiss.spos, twiss.betax, color=(0.5,0.5,1.0), label='X')
    plt.plot(twiss.spos, twiss.betay, color=(1.0,0.5,0.5), label='Y')
    pyaccel.graphics.draw_lattice(model, offset=-5, height=5, gca=axs)
    plt.xlabel('pos [m]')
    plt.ylabel('Beta function [m]')
    plt.xlim([0, model.length/10])
    plt.ylim([-10, 30])
    plt.title('Optical Functions')
    plt.grid()
    plt.legend()
    plt.show()
    
    
# create SI model
model = si.create_accelerator()


if __name__ == '__main__':
    plot_optics(model)
    





