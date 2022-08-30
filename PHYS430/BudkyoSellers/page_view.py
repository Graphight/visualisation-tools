import streamlit as st

from .plotting import plot_budkyo_sellers_model_albedo, plot_budkyo_sellers_model_temp
from .workers import Budyko_Sellers_model


KELVIN_OFFSET = 273.15
SOLAR_CONSTANT = 1370

DEFAULT_VARS = {
    "sl_solar_input": 1.0,
    "sl_phiedgeIC": 70.0,
    "sl_relaxation": 3.8,
    "sl_co2_concentration": 280.0,
    "ck_show_original": False
}


def reset_options():
    for key, value in DEFAULT_VARS.items():
        st.session_state[key] = value


def show_graphs(
        solar_input,
        phiedgeIC,
        relaxation,
        co2_concentration,
        show_original=False
):
    if show_original:
        phi_old, temps_old, albedo_old, t_planet_old = Budyko_Sellers_model(
            phiedgeIC=DEFAULT_VARS["sl_phiedgeIC"],
            S0=DEFAULT_VARS["sl_solar_input"] * SOLAR_CONSTANT,
            relaxation_coefficient=DEFAULT_VARS["sl_relaxation"],
            CO2_concentration=DEFAULT_VARS["sl_co2_concentration"]
        )
    else:
        phi_old, temps_old, albedo_old, t_planet_old = None, None, None, None

    phi_new, temps_new, albedo_new, t_planet_new = Budyko_Sellers_model(
        phiedgeIC=phiedgeIC,
        S0=solar_input * SOLAR_CONSTANT,
        relaxation_coefficient=relaxation,
        CO2_concentration=co2_concentration
    )

    st.plotly_chart(plot_budkyo_sellers_model_temp(
        phi_old,
        phi_new,
        temps_old,
        temps_new,
        t_planet_old,
        t_planet_new,
        KELVIN_OFFSET,
        show_original
    ))

    st.plotly_chart(plot_budkyo_sellers_model_albedo(
        phi_old,
        phi_new,
        albedo_old,
        albedo_new,
        show_original
    ))


def budkyo_sellers_page():
    st.title("Budkyo-Sellers")
    st.header("One dimensional energy balance model")

    solar_input = st.sidebar.slider(
        label="Solar input variation (multiple of S_o)",
        key="sl_solar_input",
        min_value=0.0,
        max_value=2.0,
        step=0.05,
        value=1.0
    )

    phiedgeIC = st.sidebar.slider(
        label="Ice sheet initial location (degrees)",
        key="sl_phiedgeIC",
        min_value=0.0,
        max_value=90.0,
        step=1.0,
        value=70.0
    )

    relaxation = st.sidebar.slider(
        label="Relaxation coefficient",
        key="sl_relaxation",
        min_value=0.0,
        max_value=5.0,
        step=0.1,
        value=3.8
    )

    co2_concentration = st.sidebar.slider(
        label="Carbon Dioxide concentration",
        key="sl_co2_concentration",
        min_value=0.0,
        max_value=1000.0,
        step=10.0,
        value=280.0
    )

    show_original = st.sidebar.checkbox(
        label="Show original lines?",
        key="ck_show_original",
        value=False
    )

    st.sidebar.button(label="Reset sliders", key="bt_bs_reset", on_click=reset_options)

    show_graphs(
        solar_input,
        phiedgeIC,
        relaxation,
        co2_concentration,
        show_original
    )


if __name__ == "__main__":
    budkyo_sellers_page()
