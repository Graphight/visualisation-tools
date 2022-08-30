import math

import numpy as np

from scipy import signal


def Lorenz_model(X, t, r, sigma, b):
    """Returns right-hand side of Lorenz model ODEs.
    In this X[0] is the X variable in the Lorenz equations
    X[1] is the Y variable in the Lorenz equations
    X[2] is the Z variable in the Lorenz equations
    """
    deriv1 = sigma*(X[1]-X[0])
    deriv2 = r*X[0] - X[1] - X[0]*X[2]
    deriv3 = X[0]*X[1] - b*X[2]
    return np.array([deriv1,deriv2,deriv3])


def forced_Lorenz_model(X, t, r, sigma, b, f0, theta):
    """Returns right-hand side of Lorenz model ODEs"""
    deriv1 = sigma*(X[1]-X[0]) + f0*math.cos(math.radians(theta))
    deriv2 = r*X[0] - X[1] - X[0]*X[2] + f0*math.sin(math.radians(theta))
    deriv3 = X[0]*X[1] - b*X[2]
    return np.array([deriv1,deriv2,deriv3])


def low_pass_Butterworth_filter(fs, fc, x):
    #fs = 1000  # Sampling frequency
    #fc = 30  # Cut-off frequency of the filter
    w = fc / (fs / 2) # Normalize the frequency
    #print(w)
    [b, a] = signal.butter(4, w, 'low')
    #print(b)
    #print(a)
    output = signal.filtfilt(b, a, x)
    return np.array(output)
