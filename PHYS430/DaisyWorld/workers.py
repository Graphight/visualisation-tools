# -*- coding: utf-8 -*-
"""
Originally created on Thu Jul 14 12:50:32 2022 by ajm226
Updated on Tue Aug 30 13:47:51 2022 by tma127

Function form of an original implementation
below:

Implementation of the Daisyworld model described in:
    Watson, A.J.; Lovelock, J.E (1983). "Biological homeostasis of
    the global environment: the parable of Daisyworld". Tellus.35B:
    286–9.
    Bibcode:1983TellB..35..284W. doi:10.1111/j.1600-0889.1983.tb00031.x.
Copyright (c) 2017 Andrew Bennett, Peter Greve, Eric Jaeger
All rights reserved.
Redistribution and use in source and binary forms are permitted
provided that the above copyright notice and this paragraph are
duplicated in all such forms and that any documentation,
advertising materials, and other materials related to such
distribution and use acknowledge that the software was developed
by the authors. The name of the authors may not be used to endorse
or promote products derived from this software without specific prior
written permission.

THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
"""

import numpy as np


def daisyworld_model(
        temp_ideal_black,
        temp_ideal_white,
        albedo_white,
        albedo_black,
        albedo_barren,
        REVERSE
):
    #   This function runs the diasyworld model for a set of conditions defiend by the inputs above
    #   temp_ideal_black is the ideal growing temperature of black daisies in Kelvin
    #   temp_ideal_white is the ideal growing temperature of white daisies in Kelvin
    #   albedo_white is the albedo of white daisies
    #   albedo_black is the albedo of black daisies
    #   albedo_barren is the albedo of bare ground
    #   REVERSE is a Boolean value (True or False) and defines whether we run the model
    #   with fluxes increasing (False) or decreasing (True)

    # Convergence criteria - this is for the black box that completes the integraiton
    # I suggest you do not play with either of these numebrs
    maxconv = 5000
    tol = 0.0000001

    # Initialise  Temperature parameters
    KELVIN_OFFSET = 273.15
    temp_min = 5 + KELVIN_OFFSET
    temp_max = 40 + KELVIN_OFFSET
    area_white = 0.01  # This is the initail area covered by white daisies
    area_black = 0.01  # This is the initail area covered by black daisies
    insul = 20  # this is a proportiately constant DO NOT CHANGE
    drate = 0.3  # This is the death rate of daisies, we need this because daisies can't live in certain conditions

    # Flux terms
    SOLAR_CONST = 1000.0  # This is the solar constant in W/m^2, To make numbers nice we have simplified to 1000
    sigma = 5.67032e-8  # Stefan Boltzmann constant  in kg/ s^3 K^4

    # Flux limits and step. This defines the range of solar flux values considered
    Sflux_min = 0.5
    Sflux_max = 1.6
    Sflux_step = 0.002

    # Initialize arrays
    fluxes = np.arange(Sflux_min, Sflux_max, Sflux_step)
    if REVERSE:
        fluxes = fluxes[::-1]  # This reverses the order of the solar flux values
    area_black_vec = np.zeros_like(fluxes)
    area_white_vec = np.zeros_like(fluxes)
    area_barren_vec = np.zeros_like(fluxes)
    Tp_vec = np.zeros_like(fluxes)

    # Loop over fluxes
    for j, flux in enumerate(fluxes):
        # Minimum daisy coverage
        if area_black < 0.01:
            area_black = 0.01
        if area_white < 0.01:
            area_white = 0.01
        area_barren = 1 - (area_black + area_white)

        # This section does the maths for the birth and death and gets to a steady state areal coverage and temperature at each solar flux level
        # Reset iteration metrics
        it = 0
        dA_black = 2 * tol
        dA_white = 2 * tol
        darea_black_old = 0
        darea_white_old = 0

        # this loop keeps going around until we reach a steady state for a particular flux.
        while it <= maxconv and dA_black > tol and dA_white > tol:
            # Planetary albedo made up of a weighted sum of albedos for the three possibilities
            # black or white daisies or land that is barren (no diasies)
            albedo_p = (area_black * albedo_black + area_white * albedo_white + area_barren * albedo_barren)
            # Planetary temperature
            Tp = np.power(flux * SOLAR_CONST * (1 - albedo_p) / sigma,
                          0.25)  # This calculates the temperature based on the average albedo

            # Local temperatures for black and white daisies
            temp_black = insul * (albedo_p - albedo_black) + Tp
            temp_white = insul * (albedo_p - albedo_white) + Tp

            # Determine the rate that black and white daisies grow
            # outside a specified temperature range the daisies do NOT grow
            if temp_min <= temp_black <= temp_max and area_black >= 0.01:
                birth_black = 1 - 0.003265 * (temp_ideal_black - temp_black) ** 2
            else:
                birth_black = 0.0

            if temp_min <= temp_white <= temp_max and area_white >= 0.01:
                birth_white = 1 - 0.003265 * (temp_ideal_white - temp_white) ** 2
            else:
                birth_white = 0.0

            # Change in areal extents
            darea_black = area_black * (birth_black * area_barren - drate)
            darea_white = area_white * (birth_white * area_barren - drate)

            # Change from previous iteration
            dA_black = abs(darea_black - darea_black_old)
            dA_white = abs(darea_white - darea_white_old)

            # Update areas, states, and iteration count
            darea_black_old = darea_black
            darea_white_old = darea_white
            area_black = area_black + darea_black
            area_white = area_white + darea_white
            area_barren = 1 - (area_black + area_white)
            it += 1

        # Save states - here we are writing everything to an array for plotting later!
        area_black_vec[j] = area_black
        area_white_vec[j] = area_white
        area_barren_vec[j] = area_barren
        Tp_vec[j] = Tp

    return fluxes, area_black_vec, area_white_vec, area_barren_vec, Tp_vec
