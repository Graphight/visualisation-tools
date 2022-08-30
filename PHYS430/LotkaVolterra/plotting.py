import numpy as np
import plotly.graph_objects as go


def plot_lotka_volterra(t, X, X_original, show_original):
    fig = go.Figure()

    if show_original:
        opacity = 0.3
        fig.add_trace(
            go.Scatter(
                x=t,
                y=X_original[:, 0],
                name="Prey - Original",
                mode="lines",
                opacity=opacity,
                line=dict(
                    color="blue"
                )
            )
        )

        fig.add_trace(
            go.Scatter(
                x=t,
                y=X_original[:, 1],
                name="Predator - Original",
                mode="lines",
                opacity=opacity,
                line=dict(
                    color="orange"
                )
            )
        )

    fig.add_trace(
        go.Scatter(
            x=t,
            y=X[:, 0],
            name="Prey",
            mode="lines",
            line=dict(
                color="blue"
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=t,
            y=X[:, 1],
            name="Predator",
            mode="lines",
            line=dict(
                color="orange"
            )
        )
    )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Population",
        legend_title_text="Animal"
    )

    return fig
