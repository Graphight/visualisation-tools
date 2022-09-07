import streamlit as st

from fair.RCPs import rcp3pd, rcp45, rcp6, rcp85

from .workers import *


def fair_stop_emitting_carbon_page():
    st.title("FaIR - Turning carbon off")
    st.write("What happens when carbon emissions stop after a certain amount of time?")

    st.sidebar.slider(
        label="What year would you like to stop emi-"
    )

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
    fair_stop_emitting_carbon_page()

