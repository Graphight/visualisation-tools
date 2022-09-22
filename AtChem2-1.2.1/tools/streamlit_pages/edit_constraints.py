import streamlit as st

from streamlit_ace import st_ace

from tools.streamlit_pages.step_calculator import time_parser


def read_file(file_path):
    with open(file_path) as f:
        lines = f.read()
    return lines


def write_file(file_path, value):
    with open(file_path, "w") as f:
        f.write(value)
    f.close()


def show_example_constraint(key):
    if st.checkbox("Show example?", key=key):
        st.write("You want to edit the constraints as time (seconds since first midnight) and value")
        st.write("The following constrains the temperature to increase 0.4 C each year")
        st.code("0\t298\n31557600\t298.4\n63115200\t298.8", language="plaintext")


def generate_file(key):
    chosen_length = time_parser(st.text_input(
        label="How long do you want to generate?",
        value="10 years",
        key=f"generate_length_{key}"
    ))

    chosen_time_step = time_parser(st.text_input(
        label="How often did you want to change your value?",
        value="1 year",
        key=f"generate_time_step_{key}"
    ))

    current_value = st.number_input(
        label="What did you want to start your value at?",
        value=298.0,
        key=f"generate_value_{key}"
    )

    chosen_increment = st.number_input(
        label="How much did you want to increase your value by?",
        value=0.4,
        key=f"generate_increment_{key}"
    )

    current_time = 0
    output = f"{current_time}\t{current_value}"
    while current_time < (chosen_time_step * (chosen_length / chosen_time_step)):
        current_time += chosen_time_step
        current_value = round(current_value + chosen_increment, 2)
        output += f"\n{current_time}\t{current_value}"

    st.success("Generated your file")
    return output


def edit_constraints_environment():
    st.subheader("Edit your enviroment constraints")

    environment_folder = "model/constraints/environment"
    environment_file_map = {
        "Temperature": f"{environment_folder}/TEMP",
        "Pressure": f"{environment_folder}/PRESS",
        "Relatively Humidity": f"{environment_folder}/RH",
        "Water Concentration": f"{environment_folder}/H2O",
        "Sun Declination": f"{environment_folder}/DEC",
        "Boundary Layer Height": f"{environment_folder}/BLHEIGHT",
        "Aerosol Surface Area": f"{environment_folder}/ASA",
        "Correction Factor": f"{environment_folder}/JFAC",
    }

    chosen_constraint = st.selectbox(
        label="Choose an evironmental constraints file to edit",
        options=sorted(environment_file_map.keys())
    )

    st.write(f"**NOTE**: You will need to change the `Configuration/environmentVariables.config` corresponding variable (`{environment_file_map[chosen_constraint].split('/')[-1]}`) to `CONSTRAINED` for this to work")

    show_example_constraint("example_environment")

    if st.checkbox("Im feeling lazy, help me generate the file", key="lazy_environment"):
        content = st_ace(
            value=generate_file("environment"),
        )
    else:
        content = st_ace(
            value=read_file(environment_file_map[chosen_constraint]),
        )
    write_file(environment_file_map[chosen_constraint], content)


def edit_constraints_species():
    st.subheader("Edit your species constraints")

    species_folder ="model/constraints/species"
    species_file_map = {
        "O": f"{species_folder}/O",
        "O3": f"{species_folder}/O3",
        "NO": f"{species_folder}/NO",
        "NO2": f"{species_folder}/NO2",
        "NO3": f"{species_folder}/NO3",
        "O1D": f"{species_folder}/O1D",
        "N2O5": f"{species_folder}/N2O5",
        "OH": f"{species_folder}/OH",
        "HO2": f"{species_folder}/HO2",
        "H2": f"{species_folder}/H2",
        "CO": f"{species_folder}/CO",
        "H2O2": f"{species_folder}/H2O2",
        "HONO": f"{species_folder}/HONO",
        "HNO3": f"{species_folder}/HNO3",
        "HO2NO2": f"{species_folder}/HO2NO2",
        "SO2": f"{species_folder}/SO2",
        "SO3": f"{species_folder}/SO3",
        "HSO3": f"{species_folder}/HSO3",
        "NA": f"{species_folder}/NA",
        "SA": f"{species_folder}/SA",
        "CL": f"{species_folder}/CL",
        "CH4": f"{species_folder}/CH4",
        "CH3O2": f"{species_folder}/CH3O2",
        "CH3OOH": f"{species_folder}/CH3OOH",
        "HCHO": f"{species_folder}/HCHO",
        "CH3NO3": f"{species_folder}/CH3NO3",
        "CH3O": f"{species_folder}/CH3O",
        "CH3O2NO2": f"{species_folder}/CH3O2NO2",
        "CH3OH": f"{species_folder}/CH3OH",
    }

    chosen_constraint = st.selectbox(
        label="Choose an evironmental constraints file to edit",
        options=sorted(species_file_map.keys())
    )

    st.write(f"**NOTE**: You will need to manually the `Configuration/speciesConstrained.config` corresponding variable (`{species_file_map[chosen_constraint].split('/')[-1]}`) to `CONSTRAINED` for this to work")

    show_example_constraint("example_species")

    if st.checkbox("Im feeling lazy, help me generate the file", key="lazy_species"):
        content = st_ace(
            value=generate_file("species")
        )
    else:
        content = st_ace(
            value=read_file(species_file_map[chosen_constraint])
        )
    write_file(species_file_map[chosen_constraint], content)
