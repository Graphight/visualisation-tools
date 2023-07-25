import streamlit as st


def update_temps(should_tether, direction):
    if should_tether:
        if direction == "w-b":
            st.session_state["sl_temp_ideal_black"] = st.session_state["sl_temp_ideal_white"]
        else:
            st.session_state["sl_temp_ideal_white"] = st.session_state["sl_temp_ideal_black"]


KELVIN_OFFSET = 273.15

DEFAULT_VARS = {
    "sl_tilt_angle": 23.0,
}


def reset_options():
    for key, value in DEFAULT_VARS.items():
        st.session_state[key] = value


def axial_tilt_page():
    st.title("Axial Tilt of Earth-like planet")

    chosen_tilt_angle = st.sidebar.slider(
        label="Axial tilt of the planet",
        key="sl_tilt_angle",
        min_value=0.5,
        max_value=90.0,
        step=0.50,
        value=20.0,
    )

    chosen_temp = st.sidebar.slider(
        label="Temperature",
        key="sl_temperature",
        min_value=0.0,
        max_value=100.0,
        step=0.50,
        value=5.0,
    )

    mass_hydrogen = 1.01
    mass_neon = 20.18
    new_molecular_mass = 1E-3 * (mass_hydrogen * 0.15) + (mass_neon * 0.85)

    gas_constant = 8.314

    new_gas_constant_dry = gas_constant / new_molecular_mass

    st.write(f"New dry gas constant: {new_gas_constant_dry}")

    scale_height = (new_gas_constant_dry * chosen_temp) / 9.81

    st.sidebar.button(label="Reset sliders", key="bt_dw_reset", on_click=reset_options)


if __name__ == "__main__":
    axial_tilt_page()
