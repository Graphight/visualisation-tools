import streamlit as st

from fair.RCPs import rcp45

from .plotting import *
from .text_supplement import *


GASES_DICT = {
    "Fossil CO2": {
        "em_index": 1, "em_units": "Gt C yr^-1", "con_index": 0, "con_units": "ppm"},
    "Other CO2": {
        "em_index": 2, "em_units": "Gt C yr^-1", "con_index": 0, "con_units": "ppm"},
    "Methane CH4": {
        "em_index": 3, "em_units": "Mt yr^-1", "con_index": 1, "con_units": "ppb"},
    "Nitrous Oxide N2O": {
        "em_index": 4, "em_units": "Mt N2 yr^-1", "con_index": 2, "con_units": "ppb"},
}


def fair_emissions_page():
    st.title("FaIR - Emissions")
    st.write("Finite Amplitude Impulse-Response simple climate-carbon-cycle model")
    text_intro()

    chosen_gas = st.sidebar.selectbox(
        label="Please pick a gas to test",
        options=GASES_DICT.keys()
    )
    chosen_index = GASES_DICT[chosen_gas]["em_index"]

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
        GASES_DICT[chosen_gas]["em_units"]
    ))

    st.pyplot(plot_carbon_concentrations(
        normal_emissions,
        half_emissions,
        double_emissions,
        GASES_DICT[chosen_gas]["con_index"],
        GASES_DICT[chosen_gas]["con_units"]
    ))

    st.pyplot(plot_radiative_forcing(normal_emissions, half_emissions, double_emissions))

    st.pyplot(plot_temperature_anomalies(normal_emissions, half_emissions, double_emissions))


if __name__ == "__main__":
    fair_emissions_page()
