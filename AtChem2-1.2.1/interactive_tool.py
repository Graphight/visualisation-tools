import streamlit as st

from tools.streamlit_pages.edit_config import edit_config
from tools.streamlit_pages.run_atchem2 import run_atchem2
from tools.streamlit_pages.generate_plots import generate_plots
from tools.streamlit_pages.location_picker import location_picker
from tools.streamlit_pages.step_calculator import step_calculator
from tools.streamlit_pages.chemical_equations import kinetics_equations, SATP_equations
from tools.streamlit_pages.edit_constraints import edit_constraints_environment, edit_constraints_species


def main():
    st.title("Interactive AtChem2")
    st.write("Welcome to this very basic GUI tool for running AtChem2 simualtions")

    # Sidebar edits

    st.sidebar.header("Here are some basic setup things")

    show_output = st.sidebar.checkbox(
        label="Show AtChem output?",
        value=False
    )

    if st.sidebar.checkbox(
        label="Edit configuration?",
        value=False
    ):
        edit_config()

    if st.sidebar.checkbox(
        label="Edit environment constraints?",
        value=False
    ):
        edit_constraints_environment()

    if st.sidebar.checkbox(
        label="Edit species constraints?",
        value=False
    ):
        edit_constraints_species()

    drop_spin_up = st.sidebar.checkbox(
        label="Skip spin up period?",
        value=False
    )

    # Sidebar widgets

    location_picker()

    step_calculator()

    # Main page

    st.header("Run the simulation")
    st.button(
        label="Run AtChem2",
        on_click=run_atchem2,
        args=[show_output]
    )

    generate_plots(drop_spin_up)

    st.header("Chemical Equations")
    if st.checkbox(
        label="Did you want to do some kinetics equations?"
    ):
        kinetics_equations()
    if st.checkbox(
        label="Did you want to do some SATP equations?"
    ): SATP_equations()


if __name__ == "__main__":
    main()