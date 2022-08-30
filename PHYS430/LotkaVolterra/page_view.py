import streamlit as st
import numpy as np

from scipy import integrate
from .plotting import plot_lotka_volterra
from .workers import Lotka_Volterra


DEFAULT_VARS = {
    "sl_alpha": 1.0,
    "sl_beta": 0.1,
    "sl_delta": 0.15,
    "sl_gamma": 0.75,
    "cb_show_original_lv": False
}


def reset_options_lotka_volterra():
    for key, value in DEFAULT_VARS.items():
        st.session_state[key] = value


def lotka_volterra_page():
    st.title("Lotka-Volterra")
    st.header("Predator-Prey population dynamics")

    alpha = st.sidebar.slider(
        label="Alpha",
        key="sl_alpha",
        min_value=0.0,
        max_value=1.5,
        step=0.05,
        value=1.0
    )

    beta = st.sidebar.slider(
        label="Beta",
        key="sl_beta",
        min_value=0.0,
        max_value=0.5,
        step=0.01,
        value=0.1
    )

    delta = st.sidebar.slider(
        label="Delta",
        key="sl_delta",
        min_value=0.0,
        max_value=0.5,
        step=0.01,
        value=0.15
    )

    gamma = st.sidebar.slider(
        label="Gamma",
        key="sl_gamma",
        min_value=0.0,
        max_value=1.5,
        step=0.05,
        value=0.75
    )

    show_original = st.sidebar.checkbox(
        label="Show original conditions?",
        key="cb_show_original_lv",
        value=False
    )

    t = np.linspace(0, 40,  2000)
    X0 = np.array([10.0, 5.0])
    X = integrate.odeint(Lotka_Volterra, X0, t, (alpha, beta, gamma, delta))
    X_original = X if not show_original else integrate.odeint(Lotka_Volterra, X0, t, (1.0, 0.1, 0.75, 0.15))

    st.sidebar.button(label="Reset sliders", on_click=reset_options_lotka_volterra)

    st.plotly_chart(plot_lotka_volterra(t, X, X_original, show_original))


if __name__ == "__main__":
    lotka_volterra_page()


