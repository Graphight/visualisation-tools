import math

import streamlit as st


def methane_cl(temperature):
    return 6.6e-12 * math.exp(-1240/temperature)


def methane_oh(temperature):
    return 1.85e-12 * math.exp(-1690/temperature)


def kinetics_equations():
    st.subheader("Kinetics equations")

    start_temp = st.number_input(
        label="What is the starting temperature? (K)",
        value=298.0,
        step=1.0
    )

    end_temp = st.number_input(
        label="What is the ending temperature? (K)",
        value=302.0,
        step=1.0
    )

    perc_1 = round(100.0 * (methane_cl(end_temp)-methane_cl(start_temp)) / methane_cl(start_temp), 6)
    perc_2 = round(100.0 * (methane_oh(end_temp)-methane_oh(start_temp)) / methane_oh(start_temp), 6)

    st.write(f"CL + CH4 = CH3O2 **:** _{methane_cl(start_temp)}_ **-->** _{methane_cl(end_temp)}_ [ {perc_1:.2f} % ]")
    st.write(f"OH + CH4 = CH3O2 **:** _{methane_oh(start_temp)}_ **-->** _{methane_oh(end_temp)}_ [ {perc_2:.2f} % ]")


def SATP_equations():
    st.subheader("SATP equations")

    chosen_concentration = st.number_input(
        label="Chosen concentration",
        value=1630
    )

    st.code(
        body=
        """
        # We should be calculating this each time but I want to save CPU cycles 
        # Here is what is happening under the hood:
        n_a = 6.022e+23
        n = 1_000_000_000 / n_a
        
        T = 25
        P = 1
        R = 8.206e-5
        
        V = (n * R * T) / P
        
        result = concentration / V
        """,
        language="python"
    )
    volume = 4.059e-11

    result = chosen_concentration / volume
    st.write(f"Molecules per cubic cm = {result:e}")
