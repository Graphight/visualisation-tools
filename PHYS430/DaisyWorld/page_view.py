import streamlit as st

from .plotting import plot_daisy_coverage, plot_planetary_temperature
from .workers import daisyworld_model


def update_temps(should_tether, direction):
    if should_tether:
        if direction == "w-b":
            st.session_state["sl_temp_ideal_black"] = st.session_state["sl_temp_ideal_white"]
        else:
            st.session_state["sl_temp_ideal_white"] = st.session_state["sl_temp_ideal_black"]


KELVIN_OFFSET = 273.15

DEFAULT_VARS = {
    "ck_tether_temps": True,
    "sl_temp_ideal_black": 22.5,
    "sl_temp_ideal_white": 22.5,
    "sl_albedo_white": 0.75,
    "sl_albedo_black": 0.25,
    "sl_albedo_barren": 0.50,
    "ck_reverse": False,
    "ck_show_barren": False,
    "ck_show_original": False
}


def reset_options():
    for key, value in DEFAULT_VARS.items():
        st.session_state[key] = value


def show_graphs(
        temp_ideal_black,
        temp_ideal_white,
        albedo_white,
        albedo_black,
        albedo_barren,
        reverse,
        show_original
):
    fluxes_new, area_black_vec_new, area_white_vec_new, _, Tp_vec_new = daisyworld_model(
        temp_ideal_black + KELVIN_OFFSET,
        temp_ideal_white + KELVIN_OFFSET,
        albedo_white,
        albedo_black,
        albedo_barren,
        reverse
    )

    # It would be more useful to look at the original when not reversing solar luminosity
    if not reverse:
        temp_ideal_black = DEFAULT_VARS["sl_temp_ideal_black"] + KELVIN_OFFSET
        temp_ideal_white = DEFAULT_VARS["sl_temp_ideal_white"] + KELVIN_OFFSET
        albedo_white = DEFAULT_VARS["sl_albedo_white"]
        albedo_black = DEFAULT_VARS["sl_albedo_black"]
        albedo_barren = DEFAULT_VARS["sl_albedo_barren"]

    fluxes_old, area_black_vec_old, area_white_vec_old, _, Tp_vec_old = daisyworld_model(
        temp_ideal_black,
        temp_ideal_white,
        albedo_white,
        albedo_black,
        albedo_barren,
        False
    )

    st.plotly_chart(plot_daisy_coverage(
        fluxes_old,
        fluxes_new,
        area_black_vec_old,
        area_black_vec_new,
        area_white_vec_old,
        area_white_vec_new,
        show_original
    ))

    st.plotly_chart(plot_planetary_temperature(
        fluxes_old,
        fluxes_new,
        Tp_vec_old,
        Tp_vec_new,
        KELVIN_OFFSET,
        show_original
    ))


def daisy_world_page():
    st.title("Daisy World")

    tether_temps = st.sidebar.checkbox(
        label="Tether temperatures?",
        key="ck_tether_temps",
        value=True
    )

    temp_ideal_black = st.sidebar.slider(
        label="Ideal black daisy temperature (C)",
        key="sl_temp_ideal_black",
        min_value=5.0,
        max_value=40.0,
        step=0.50,
        value=22.5,
        on_change=update_temps,
        kwargs={"should_tether": tether_temps, "direction": "b-w"}
    )
    temp_ideal_white = st.sidebar.slider(
        label="Ideal white daisy temperature (C)",
        key="sl_temp_ideal_white",
        min_value=5.0,
        max_value=40.0,
        step=0.50,
        value=22.5,
        on_change=update_temps,
        kwargs={"should_tether": tether_temps, "direction": "w-b"}
    )

    albedo_white = st.sidebar.slider(
        label="White daisy albedo",
        key="sl_albedo_white",
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        value=0.75
    )
    albedo_black = st.sidebar.slider(
        label="Black daisy albedo",
        key="sl_albedo_black",
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        value=0.25
    )
    albedo_barren = st.sidebar.slider(
        label="Barren land albedo",
        key="sl_albedo_barren",
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        value=0.50
    )

    REVERSE = st.sidebar.checkbox(
        label="Reverse solar luminosity?",
        key="ck_reverse",
        value=False
    )
    show_original = st.sidebar.checkbox(
        label="Show original lines?",
        key="ck_show_original",
        value=False
    )

    st.sidebar.button(label="Reset sliders", key="bt_dw_reset", on_click=reset_options)

    show_graphs(
        temp_ideal_black,
        temp_ideal_white,
        albedo_white,
        albedo_black,
        albedo_barren,
        REVERSE,
        show_original
    )


if __name__ == "__main__":
    daisy_world_page()
