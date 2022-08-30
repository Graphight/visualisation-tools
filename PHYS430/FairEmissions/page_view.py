import streamlit as st

from fair.RCPs import rcp45

from .plotting import *


GAS_INDICES = {
    "Fossil CO2": 1,
    "Other CO2": 2,
    "Methane": 3,
    "Nitrous Oxide": 4
}

GAS_UNITS = {
    "Fossil CO2": "Gt C yr^-1",
    "Other CO2": "Gt C yr^-1",
    "Methane": "Mt yr^-1",
    "Nitrous Oxide": "Mt N2 yr^-1"
}


def fair_emissions_page():
    st.title("FaIR - Emissions")
    st.write("Finite Amplitude Impulse-Response simple climate-carbon-cycle model")

    chosen_gas = st.sidebar.selectbox(
        label="Please pick a gas to test",
        options=GAS_INDICES.keys()
    )
    chosen_index = GAS_INDICES[chosen_gas]

    normal_emissions = rcp45.Emissions.emissions

    double_emissions = normal_emissions.copy()
    double_emissions[:, chosen_index] *= 2

    half_emissions = normal_emissions.copy()
    half_emissions[:, chosen_index] *= 0.5

    st.pyplot(plot_emissions(
        normal_emissions,
        half_emissions,
        double_emissions,
        chosen_index,
        GAS_UNITS[chosen_gas]
    ))

    st.pyplot(plot_carbon_concentrations(normal_emissions, half_emissions, double_emissions))

    st.pyplot(plot_radiative_forcing(normal_emissions, half_emissions, double_emissions))

    st.pyplot(plot_temperature_anomalies(normal_emissions, half_emissions, double_emissions))


if __name__ == "__main__":
    fair_emissions_page()
