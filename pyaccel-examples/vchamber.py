#!/usr/bin/env python-sirius

"""Vacuum Chamber Limits."""

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


def print_model(model):
    """."""
    # print basic information about accelerator model
    print('--- accelerator ---')
    print(f'circumference       : {model.length:.4f} m')
    print(f'energy              : {model.energy/1e9} GeV')
    print(f'beta                : {model.beta_factor:.10f}')
    print(f'gamma               : {model.gamma_factor:.1f}')
    print(f'brho (mag. rigidity): {model.brho:.6f} T.m')


def plot_vchamber(model):

    # get vacuum chamber dimension along the ring
    spos = pyaccel.lattice.find_spos(model)
    hmin = pyaccel.lattice.get_attribute(model, 'hmin')
    hmax = pyaccel.lattice.get_attribute(model, 'hmax')
    vmin = pyaccel.lattice.get_attribute(model, 'vmin')
    vmax = pyaccel.lattice.get_attribute(model, 'vmax')

    color = (0.4,0.4,0.4)  # vchamver color
    title = 'SI {} Vacuum Chamber and Magnets\n(shifted to InjSeptF)'

    # plot vacuum chamber horizontal limits
    _, axs = plt.subplots(1, 1, figsize=(10, 5))
    plt.plot(spos, 1e3*hmax, color=color)
    plt.plot(spos, 1e3*hmax, 'o', color=color)
    plt.plot(spos, 1e3*hmin, color=color)
    plt.plot(spos, 1e3*hmin, 'o', color=color)
    plt.xlabel('pos [m]')
    plt.ylabel('limits [mm]')
    plt.xlim([0, 4*model.length/20])
    # plt.xlim([0, 34])
    plt.title(title.format('Horizontal'))
    pyaccel.graphics.draw_lattice(model, height=5, gca=axs)
    plt.savefig('vchamber-horizontal-limits.png')
    plt.show()

    # plot vacuum chamber vertical limits
    _, axs = plt.subplots(1, 1, figsize=(10, 5))
    plt.plot(spos, 1e3*vmax, color=color)
    plt.plot(spos, 1e3*vmax, 'o', color=color)
    plt.plot(spos, 1e3*vmin, color=color)
    plt.plot(spos, 1e3*vmin, 'o', color=color)
    plt.xlabel('pos [m]')
    plt.ylabel('limits [mm]')
    plt.xlim([0, 4*model.length/20])
    # plt.xlim([0, 34])
    plt.title(title.format('Vertical'))
    pyaccel.graphics.draw_lattice(model, height=5, gca=axs)
    plt.savefig('vchamber-vertical-limits.png')
    plt.show()


# create SI model
model = si.create_accelerator()

# shift model so that it starts right after the thin injection septum
injseptf = pyaccel.lattice.find_indices(model, 'fam_name', 'InjSeptF')
model = pyaccel.lattice.shift(model, start=injseptf[0])


if __name__ == '__main__':
    print_model(model)
    plot_vchamber(model)





