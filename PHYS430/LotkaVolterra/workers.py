# -*- coding: utf-8 -*-
"""
This code provides you with an example of how Ordinary Differential Equations
are solved in python and also creates a relevant visualisation of the system.
Originally created on Sun Aug 16 10:28:20 2020 ajm226
Updated on Tue Aug 30 21:50:50 2022 by tma127
"""

import numpy as np
import streamlit as st


@st.cache
def Lotka_Volterra(X, t, alpha, beta, gamma, delta):
    """ Return the growth rate of predator and prey populations
    based on the Lotka Volterra equations.
    X[0] is prey species number
    X[1] is predator species numebrs
    Note X[0] represents the first value in an array (set of numbers) and the inputs need
    to be in this format to work with the code that does integration in scipy.

    alpha, beta, gamma and delta are variable factors identifying the species interactions
    """
    dx_dt = alpha * X[0] - beta * X[0] * X[1]
    dy_dt = -gamma * X[1] + delta * X[0] * X[1]
    return np.array([dx_dt, dy_dt])

