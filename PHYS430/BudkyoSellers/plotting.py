import numpy as np
import streamlit as st
import plotly.graph_objects as go


def plot_budkyo_sellers_model_temp(
        phi_old,
        phi_new,
        temps_old,
        temps_new,
        t_planet_old,
        t_planet_new,
        kelvin_offset,
        show_original=False
):
    fig = go.Figure()

    if show_original:
        fig.add_trace(
            go.Scatter(
                x=phi_old,
                y=temps_old - kelvin_offset,
                name="old",
                mode="lines",
                opacity=0.3
            )
        )

        avg_planet_temp_old = str(np.round(t_planet_old - kelvin_offset, 0))
        st.write(f'Average old temperature of planet = {avg_planet_temp_old} C')

    fig.add_trace(
        go.Scatter(
            x=phi_new,
            y=temps_new - kelvin_offset,
            name="new",
            mode="lines"
        )
    )

    avg_planet_temp_new = str(np.round(t_planet_new - kelvin_offset, 0))
    st.write(f'Average new temperature of planet = {avg_planet_temp_new} C')

    fig.update_layout(
        xaxis_title='Latitude (degrees)',
        yaxis_title="Temperature (C)",

    )

    fig.update_xaxes(range=(-95, 95))

    return fig


def plot_budkyo_sellers_model_albedo(
        phi_old,
        phi_new,
        albedo_old,
        albedo_new,
        show_original
):
    fig = go.Figure()

    if show_original:
        fig.add_trace(
            go.Scatter(
                x=phi_old,
                y=albedo_old * 100,
                name="old",
                mode="lines",
                opacity=0.3
            )
        )


    fig.add_trace(
        go.Scatter(
            x=phi_new,
            y=albedo_new * 100,
            name="new",
            mode="lines"
        )
    )

    fig.update_layout(
        xaxis_title='Latitude (degrees)',
        yaxis_title="Albedo (%)",
    )

    fig.update_xaxes(range=(-95, 95))
    fig.update_yaxes(range=(0, 100))

    return fig
