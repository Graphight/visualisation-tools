import streamlit as st

from AxialTilt import axial_tilt_page


PAGE_OPTIONS = [
    "Axial Tilt",
]


def main():
    st.sidebar.header("Page Selection")

    page_choice = st.sidebar.radio(
        label="Which page would you like to view?",
        options=PAGE_OPTIONS
    )

    st.sidebar.write("-------")
    st.sidebar.header("Variables")

    if page_choice == "Daisy World":
        axial_tilt_page()


if __name__ == "__main__":
    main()
