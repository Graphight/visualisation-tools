import streamlit as st
import pandas as pd
import numpy as np


def location_picker():
    st.sidebar.header("Location Picker")

    df = pd.read_csv("tools/misc_data/worldcities.csv")

    chosen_country = st.sidebar.selectbox(
        label="Please pick a country",
        options=sorted(df["country"].unique())
    )

    df_country = df.loc[df["country"] == chosen_country]

    chosen_city = st.sidebar.selectbox(
        label="Please pick a city",
        options=sorted(df_country["city"].unique())
    )

    df_city = df_country.loc[df_country["city"] == chosen_city]

    chosen_lat = df_city.iloc[0]["lat"]
    st.sidebar.write(f"Latitude: ***{chosen_lat}***")

    chosen_long = df_city.iloc[0]["lng"]
    st.sidebar.write(f"Longitude: ***{chosen_long}***")

    st.sidebar.write("***Note***: You will still need to update these in model parameters config")
