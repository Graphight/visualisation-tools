import plotly.graph_objects as go


def plot_daisy_coverage(
        fluxes_a,
        fluxes_b,
        area_black_vec_a,
        area_black_vec_b,
        area_white_vec_a,
        area_white_vec_b,
        show_original=False
):
    fig = go.Figure()

    if show_original:
        fig.add_trace(
            go.Scatter(
                x=fluxes_a,
                y=100 * area_black_vec_a,
                mode="lines",
                name="Black Daisies - Old",
                opacity=0.3,
                line=dict(
                    color="black"
                )
            )
        )

        fig.add_trace(
            go.Scatter(
                x=fluxes_a,
                y=100 * area_white_vec_a,
                mode="lines",
                name="White Daisies - Old",
                opacity=0.3,
                line=dict(
                    color="red"
                )
            )
        )

    fig.add_trace(
        go.Scatter(
            x=fluxes_b,
            y=100 * area_black_vec_b,
            mode="lines",
            name="Black Daisies - New",
            line=dict(
                color="black"
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=fluxes_b,
            y=100 * area_white_vec_b,
            mode="lines",
            name="White Daisies - New",
            line=dict(
                color="red"
            )
        )
    )

    fig.update_layout(
        title="Daisy coverage as a function of solar luminosity",
        xaxis_title="Solar Luminosity",
        yaxis_title="Area (%)",
        legend_title_text="Terrain"
    )

    return fig


def plot_planetary_temperature(
        fluxes_a,
        fluxes_b,
        Tp_vec_a,
        Tp_vec_b,
        KELVIN_OFFSET,
        show_original=False
):
    fig = go.Figure()

    if show_original:
        fig.add_trace(
            go.Scatter(
                x=fluxes_a,
                y=Tp_vec_a - KELVIN_OFFSET,
                mode="lines",
                opacity=0.3,
                line=dict(
                    color="black"
                ),
                name="Old"
            )
        )

    fig.add_trace(
        go.Scatter(
            x=fluxes_b,
            y=Tp_vec_b - KELVIN_OFFSET,
            mode="lines",
            line=dict(
                color="black"
            ),
            name="New"
        )
    )

    fig.update_layout(
        title="Temperature as a function of solar luminosity",
        xaxis_title="Solar Luminosity",
        yaxis_title="Global temperature (C)"
    )

    return fig
