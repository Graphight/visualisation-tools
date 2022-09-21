import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from tools.streamlit_pages.step_calculator import time_parser


MODEL_OUTPUT_DIR = "model/output"


def generate_species_concentrations_plot(starting_seconds):
    output_file_name = f"{MODEL_OUTPUT_DIR}/speciesConcentrations.output"

    with open(output_file_name) as f:
        titles = f.readline().split()

    df = np.loadtxt(output_file_name, skiprows=1, unpack=True)

    fig = plt.figure(figsize=(11, 7))
    j = 1
    for i in range(1, df.shape[0]):
        ax = fig.add_subplot(3, 2, j)
        ax.plot(df[0], df[i], linestyle="-", color="black")
        ax.set(title=titles[i], xlabel="seconds", ylabel="")
        ax.set_xlim(left=starting_seconds)
        if j == 4:
            # ax.set_ylim(1e9,1e10)
            ax.set_yscale("log")
        elif j == 5:
            # ax.set_ylim(0,0.5e10)
            ax.set_yscale("log")
        else:
            plt.ticklabel_format(style="sci", axis="y", useMathText=True)
        plt.tight_layout()

        if j == 6:
            st.pyplot(fig)
            fig = plt.figure(figsize=(11, 7))
            j = 1
        else:
            j += 1

    if j != 1:
        st.pyplot(fig)


def generate_environment_variables_plot(starting_seconds):
    output_file_name = f"{MODEL_OUTPUT_DIR}/environmentVariables.output"

    with open(output_file_name) as f:
        titles = f.readline().split()

    df = np.loadtxt(output_file_name, skiprows=1, unpack=True)

    fig = plt.figure(figsize=(11, 7))
    j = 1
    for i in range(1,df.shape[0]):
        ax = fig.add_subplot(3, 2, j)
        ax.plot(df[0], df[i], linestyle="-", color="black")
        ax.set(title=titles[i], xlabel="seconds", ylabel="")
        ax.set_xlim(left=starting_seconds)
        plt.tight_layout()
        plt.ticklabel_format(style="sci", axis="y", useMathText=True)

        if j == 6:
            st.pyplot(fig)
            fig = plt.figure(figsize=(11, 7))
            j = 1
        else:
            j += 1

    if j != 1:
        st.pyplot(fig)


def generate_photolysis_rates_plot(starting_seconds):
    output_file_name = f"{MODEL_OUTPUT_DIR}/photolysisRates.output"
    with open(output_file_name) as f:
        titles = f.readline().split()

    df = np.loadtxt(output_file_name, skiprows=1, unpack=True)

    fig = plt.figure(figsize=(11, 7))
    j = 1
    for i in range(1, df.shape[0]):
        ax = fig.add_subplot(3, 2, j)
        ax.plot(df[0], df[i], linestyle="-", color="black")
        ax.set(title=titles[i], xlabel="seconds", ylabel="")
        ax.set_xlim(left=starting_seconds)
        plt.tight_layout()
        plt.ticklabel_format(style="sci", axis="y", useMathText=True)

        if j == 6:
            st.pyplot(fig)
            fig = plt.figure(figsize=(11, 7))
            j = 1
        else:
            j += 1

    if j != 1:
        st.pyplot(fig)


def generate_photolysis_rates_params_plot(starting_seconds):
    output_file_name = f"{MODEL_OUTPUT_DIR}/photolysisRatesParameters.output"
    with open(output_file_name) as f:
        titles = f.readline().split()

    df = np.loadtxt(output_file_name, skiprows=1, unpack=True)

    fig = plt.figure(figsize=(11, 7))
    j = 1
    for i in range(1, df.shape[0]):
        ax = fig.add_subplot(3, 2, j)
        ax.plot(df[0], df[i], linestyle="-", color="black")
        ax.set(title=titles[i], xlabel="seconds", ylabel="")
        ax.set_xlim(left=starting_seconds)
        plt.tight_layout()
        plt.ticklabel_format(style="sci", axis="y", useMathText=True)

        if j == 6:
            st.pyplot(fig)
            fig = plt.figure(figsize=(11, 7))
            j = 1
        else:
            j += 1

    if j != 1:
        st.pyplot(fig)


def generate_plots(drop_start=False):
    st.header("Plotting")
    if drop_start:
        starting_seconds = time_parser(st.text_input(
            label="What is your spin up period?",
            value="2 days"
        ))
    else:
        starting_seconds = 0

    st.button(
        label="Generate species concentrations plot",
        on_click=generate_species_concentrations_plot,
        args=[starting_seconds]
    )

    st.button(
        label="Generate environment variables plot",
        on_click=generate_environment_variables_plot,
        args=[starting_seconds]
    )

    st.button(
        label="Generate photolysis rates plot",
        on_click=generate_photolysis_rates_plot,
        args=[starting_seconds]
    )

    st.button(
        label="Generate photolysis rates params plot",
        on_click=generate_photolysis_rates_params_plot,
        args=[starting_seconds]
    )