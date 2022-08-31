import fair

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from fair.RCPs import rcp3pd, rcp45, rcp6, rcp85


@st.cache
def compute_fair(emissions):
    return fair.forward.fair_scm(emissions=emissions)


def plot_emissions(original_emissions, half_emissions, double_emissions, column_index, units):
    fig = plt.figure(figsize=(10,8), dpi=200)

    plt.plot(rcp45.Emissions.year, original_emissions[:, column_index], color='orange', label='RCP4.5 original')
    plt.plot(rcp45.Emissions.year, half_emissions[:, column_index], color='blue', label='RCP4.5 half')
    plt.plot(rcp45.Emissions.year, double_emissions[:, column_index], color='black', label='RCP4.5 double')

    plt.title("Emissions over time")
    plt.ylabel(f'Fossil Emissions {units}')
    plt.legend()

    return fig


def plot_carbon_concentrations(original_emissions, half_emissions, double_emissions, column_index, units):
    C45_original, F45_original, T45_original = compute_fair(original_emissions)
    C45_half, F45_half, T45_half = compute_fair(half_emissions)
    C45_double, F45_double, T45_double = compute_fair(double_emissions)

    fig = plt.figure(figsize=(10,8), dpi=200)

    plt.plot(rcp45.Emissions.year, C45_original[:, column_index], color='orange', label='RCP4.5 original')
    plt.plot(rcp45.Emissions.year, C45_half[:, column_index], color='blue', label='RCP4.5 half')
    plt.plot(rcp45.Emissions.year, C45_double[:, column_index], color='black', label='RCP4.5 double')

    plt.title("CO2 concentrations over time")
    plt.ylabel(f'CO2 concentrations ({units})')
    plt.legend()

    return fig


def plot_radiative_forcing(original_emissions, half_emissions, double_emissions):
    C45_original, F45_original, T45_original = compute_fair(original_emissions)
    C45_half, F45_half, T45_half = compute_fair(half_emissions)
    C45_double, F45_double, T45_double = compute_fair(double_emissions)

    fig = plt.figure(figsize=(10,8), dpi=200)

    # Total radiative forcing
    plt.plot(rcp45.Emissions.year, np.sum(F45_original, axis=1), color='orange', label='RCP4.5 original')
    plt.plot(rcp45.Emissions.year, np.sum(F45_half, axis=1), color='blue', label='RCP4.5 half')
    plt.plot(rcp45.Emissions.year, np.sum(F45_double, axis=1), color='black', label='RCP4.5 double')

    plt.title("Radiative forcing over time")
    plt.ylabel('Total radiative forcing (W.m$^{-2}$)')
    plt.legend()

    return fig


def plot_temperature_anomalies(original_emissions, half_emissions, double_emissions):
    C45_original, F45_original, T45_original = compute_fair(original_emissions)
    C45_half, F45_half, T45_half = compute_fair(half_emissions)
    C45_double, F45_double, T45_double = compute_fair(double_emissions)

    fig = plt.figure(figsize=(10,8), dpi=200)

    # Temperature anomaly
    _, _, T26 = fair.forward.fair_scm(emissions=rcp3pd.Emissions.emissions)
    _, _, T60 = fair.forward.fair_scm(emissions=rcp6.Emissions.emissions)
    _, _, T85 = fair.forward.fair_scm(emissions=rcp85.Emissions.emissions)
    plt.plot(rcp45.Emissions.year, T45_original, color='orange', label="RCP4.5 Original")
    plt.plot(rcp45.Emissions.year, T45_half, color='blue', label="RCP4.5 Half")
    plt.plot(rcp45.Emissions.year, T45_double, color='black', label="RCP4.5 Double")
    plt.plot(rcp45.Emissions.year, T26, color='gray', label="RCP2.6")
    plt.plot(rcp45.Emissions.year, T60, color='green', label="RCP6.0")
    plt.plot(rcp45.Emissions.year, T85, color='red', label="RCP8.5")

    plt.title("Temperature anomaly over time")
    plt.ylabel('Temperature anomaly (K)')
    plt.legend()

    return fig
