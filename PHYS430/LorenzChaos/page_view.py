import streamlit as st
import numpy as np

from scipy import integrate

from .plotting import *
from .workers import *


DEFAULT_VARS_LORENZ = {
    "sl_r": 28.0,
    "sl_sigma": 10.0,
    "sl_b": 8.0 / 3.0,
    "cb_show_original_lz": False
}

DEFAULT_VARS_FORCED = {
    "cb_show_original_f_lz": False,
    "sl_f_f0": 2.5,
    "sl_f_theta": 45.0
}


def reset_options_lorenz():
    for key, value in DEFAULT_VARS_LORENZ.items():
        st.session_state[key] = value


def reset_options_forced_lorenz():
    for key, value in DEFAULT_VARS_FORCED.items():
        st.session_state[key] = value


def show_lorenz():
    r = st.sidebar.slider(
        label="r",
        key="sl_r",
        min_value=0.0,
        max_value=50.0,
        step=1.0,
        value=28.0
    )

    sigma = st.sidebar.slider(
        label="Sigma",
        key="sl_sigma",
        min_value=0.0,
        max_value=20.0,
        step=0.1,
        value=10.0
    )

    b = st.sidebar.slider(
        label="b",
        key="sl_b",
        min_value=0.0,
        max_value=10.0,
        step=0.10,
        value=8.0 / 3.0
    )

    show_original = st.sidebar.checkbox(
        label="Show original conditions?",
        key="cb_show_original_lv",
        value=False
    )

    n = 2_000

    t = np.linspace(0, 80.0, n)
    tmax=np.max(t)
    X0=np.array([0.0, 5.01, 1.05])
    X = integrate.odeint(Lorenz_model, X0, t, (r, sigma, b))
    X_original = integrate.odeint(Lorenz_model, X0, t, (28, 10, 8.0/3.0)) if show_original else None

    st.sidebar.button(label="Reset sliders", on_click=reset_options_lorenz)

    st.plotly_chart(plot_lorenz_2d_x(t, X, X_original, show_original))
    st.plotly_chart(plot_lorenz_2d_y(t, X, X_original, show_original))
    st.plotly_chart(plot_lorenz_2d_z(t, X, X_original, show_original))
    st.plotly_chart(plot_lorenz_3d_plotly(X, X_original, show_original, n))


def show_forced_lorenz():
    f0 = st.sidebar.slider(
        label="Force",
        key="sl_f_f0",
        min_value=0.0,
        max_value=20.0,
        step=0.5,
        value=2.5
    )

    theta = st.sidebar.slider(
        label="angle",
        key="sl_f_theta",
        min_value=0.0,
        max_value=180.0,
        step=5.0,
        value=45.0
    )

    show_original = st.sidebar.checkbox(
        label="Show original conditions?",
        key="cb_show_original_f_lv",
        value=False
    )

    r = 28.0
    sigma = 10.0
    b = 8.0/3.0

    n = 20_000

    t = np.linspace(0, 1800.0, n)
    tmax=np.max(t)
    X0=np.array([1.0,1.0,1.05])
    X = integrate.odeint(forced_Lorenz_model, X0, t, (r, sigma, b, f0, theta))
    X_original = integrate.odeint(forced_Lorenz_model, X0, t, (r, sigma, b, 2.5, 45.0)) if show_original else None

    #This does some maths to make the diagram look nicer you don't need to change this
    X_sample = np.squeeze(X[:, 0])
    Y_sample = np.squeeze(X[:, 1])
    fs = 1.0/(t[1]-t[0])
    fc = 1.0/4.0
    X_sample_LPF = low_pass_Butterworth_filter(fs, fc, X_sample)
    Y_sample_LPF = low_pass_Butterworth_filter(fs, fc, Y_sample)

    st.sidebar.button(label="Reset sliders", on_click=reset_options_forced_lorenz)

    st.pyplot(plot_forced_lorenz_2d(X_sample_LPF, Y_sample_LPF, f0, theta))
    st.plotly_chart(plot_lorenz_3d_plotly(X, X_original, show_original, n))


def lorenz_chaos_page():
    st.title("Lorenz Chaos!")

    options = [
        "Lorenz",
        "Forced Lorenz"
    ]

    chosen_option = st.selectbox(
        label="Which model would you like to look at?",
        options=options
    )

    if chosen_option == "Lorenz":
        show_lorenz()
    elif chosen_option == "Forced Lorenz":
        show_forced_lorenz()


if __name__ == "__main__":
    lorenz_chaos_page()


