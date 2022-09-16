import math

import streamlit as st


def time_parser(time_str):
    time_str = time_str.upper()
    parts = time_str.split(" ")

    seconds_in_minute = 60
    seconds_in_hour = seconds_in_minute * 60
    seconds_in_day = seconds_in_hour * 24
    seconds_in_week = seconds_in_day * 7
    seconds_in_year = seconds_in_week * 52

    time_value = float(parts[0])
    time_word = parts[1]
    if "YEAR" in time_word:
        output = time_value * seconds_in_year
    elif "WEEK" in time_word:
        output = time_value * seconds_in_week
    elif "DAY" in time_word:
        output = time_value * seconds_in_day
    elif "HOUR" in time_word:
        output = time_value * seconds_in_hour
    elif "MINUTE" in time_word:
        output = time_value * seconds_in_minute
    else:
        output = time_value

    return int(output)


def step_calculator():
    st.sidebar.header("Step calculator")

    simulation_length = time_parser(st.sidebar.text_input(
        label="Length of simulation",
        value="10 days"
    ))

    simulation_step_size = time_parser(st.sidebar.text_input(
        label="Length of steps",
        value="15 minutes"
    ))

    simulation_steps = int(math.ceil(simulation_length / simulation_step_size))

    st.sidebar.write(f"Number steps: ***{simulation_steps}***")
    st.sidebar.write(f"Step size: ***{simulation_step_size}***")

    st.sidebar.write("***Note***: You will still need to update these in model parameters config")
