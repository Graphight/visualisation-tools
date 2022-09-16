import streamlit as st

from tools.streamlit_pages.edit_config import edit_config
from tools.streamlit_pages.run_atchem2 import run_atchem2
from tools.streamlit_pages.generate_plots import generate_plots
from tools.streamlit_pages.location_picker import location_picker
from tools.streamlit_pages.step_calculator import step_calculator


def main():
    st.title("Interactive AtChem2")
    st.write("Welcome to this very basic GUI tool for running AtChem2 simualtions")

    # Sidebar edits

    st.sidebar.header("Here are some basic setup things")

    show_configuration = st.sidebar.checkbox(
        label="Edit configuration?",
        value=False
    )
    show_output = st.sidebar.checkbox(
        label="Show AtChem output?",
        value=False
    )
    drop_spin_up = st.sidebar.checkbox(
        label="Skip spin up period?",
        value=False
    )

    # Sidebar widgets

    location_picker()

    step_calculator()

    if show_configuration:
        edit_config()

    # Main page

    st.header("Run the simulation")
    st.button(
        label="Run AtChem2",
        on_click=run_atchem2,
        args=[show_output]
    )

    generate_plots(drop_spin_up)


if __name__ == "__main__":
    main()