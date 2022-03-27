#!/usr/bin/env python-sirius

"""Lattice Optics."""

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
    





