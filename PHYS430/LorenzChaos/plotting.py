import numpy as np
import plotly.graph_objects as go
import matplotlib as mpl
import matplotlib.pyplot as plt


def plot_lorenz_2d_x(t, X, X_original, show_original):
    fig = go.Figure()

    if show_original:
        fig.add_trace(
            go.Scatter(
                x=t,
                y=X_original[:, 0],
                opacity=0.5,
                name="X - original",
                mode="lines",
                line=dict(
                    color="blue"
                )
            )
        )

    fig.add_trace(
        go.Scatter(
            x=t,
            y=X[:, 0],
            name="X",
            mode="lines",
            line=dict(
                color="orange" if show_original else "blue"
            )
        )
    )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="X values"
    )

    return fig


def plot_lorenz_2d_y(t, X, X_original, show_original):
    fig = go.Figure()

    if show_original:
        fig.add_trace(
            go.Scatter(
                x=t,
                y=X_original[:, 1],
                opacity=0.5,
                name="Y - original",
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
            name="Y",
            mode="lines",
            line=dict(
                color="orange" if show_original else "blue"
            )
        )
    )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Y values"
    )

    return fig


def plot_lorenz_2d_z(t, X, X_original, show_original):
    fig = go.Figure()

    if show_original:
        fig.add_trace(
            go.Scatter(
                x=t,
                y=X_original[:, 2],
                opacity=0.5,
                name="Z - original",
                mode="lines",
                line=dict(
                    color="blue"
                )
            )
        )

    fig.add_trace(
        go.Scatter(
            x=t,
            y=X[:, 2],
            name="Z",
            mode="lines",
            line=dict(
                color="orange" if show_original else "blue"
            )
        )
    )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Z values"
    )

    return fig


def plot_lorenz_3d(X, n):
    # plt a three dimensional version of the plat
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Make the line multi-coloured by plotting it in segments of length s which
    # change in colour across the whole time series.
    s = 10
    c = np.linspace(0,1,n)
    for i in range(0,n-s,s):
        ax.plot(X[i:i+s+1,0], X[i:i+s+1,1], X[i:i+s+1,2], color=(c[i],0.0,1.0), alpha=0.4)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')


def plot_lorenz_3d_plotly(X, X_original, show_original, n):
    fig = go.Figure()

    if show_original:
        fig.add_trace(
            go.Scatter3d(
                x=X_original[:, 0],
                y=X_original[:, 1],
                z=X_original[:, 2],
                name="Original",
                mode="lines",
                opacity=0.9,
                line=dict(
                    color=np.linspace(0, 1, n),
                    colorscale="plotly3"
                )
            )
        )

    if not show_original:
        fig.add_trace(
            go.Scatter3d(
                x=X[:, 0],
                y=X[:, 1],
                z=X[:, 2],
                name="New",
                mode="lines",
                opacity=0.8,
                line=dict(
                    color=np.linspace(0, 1, n),
                    colorscale="redor"
                )
            )
        )

    fig.update_layout(
        width=750,
        height=750,
    )

    return fig


def plot_forced_lorenz_2d(X_sample_LPF, Y_sample_LPF, f0, theta):
    plt.figure()
    plt.hist2d(
        x=X_sample_LPF,
        y=Y_sample_LPF,
        norm=mpl.colors.LogNorm(),
        range=[[-20.0,20.0],[-20.0,20.0]],
        bins=(50,50),
        cmap='Reds'
    )
    plt.axis('square')
    plt.xlim([-20.0,20.0])
    plt.ylim([-20.0,20.0])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('F='+str(f0)+' $theta$='+str(theta))
    return plt