import streamlit as st

from BudkyoSellers.page_view import budkyo_sellers_page
from DaisyWorld.page_view import daisy_world_page
from LotkaVolterra.page_view import lotka_volterra_page

PAGE_OPTIONS = [
    "Daisy World",
    "Budkyo Sellers",
    "Lotka Volterra"
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
        daisy_world_page()
    elif page_choice == "Budkyo Sellers":
        budkyo_sellers_page()
    elif page_choice == "Lotka Volterra":
        lotka_volterra_page()


if __name__ == "__main__":
    main()
