import streamlit as st

from streamlit_ace import st_ace


def read_file(file_path):
    with open(file_path) as f:
        lines = f.read()
    return lines


def write_file(file_path, value):
    with open(file_path, "w") as f:
        f.write(value)
    f.close()


CONFIG_FOLDER = "model/configuration"
FILE_MAP = {
    "environment variables": f"{CONFIG_FOLDER}/environmentVariables.config",
    "initial concentrations": f"{CONFIG_FOLDER}/initialConcentrations.config",
    "model parameters": f"{CONFIG_FOLDER}/model.parameters",
    "output rates": f"{CONFIG_FOLDER}/outputRates.config",
    "output species": f"{CONFIG_FOLDER}/outputSpecies.config",
    "photolysis constant": f"{CONFIG_FOLDER}/photolysisConstant.config",
    "photolysis constrained": f"{CONFIG_FOLDER}/photolysisConstrained.config",
    "solver": f"{CONFIG_FOLDER}/solver.parameters",
    "species constant": f"{CONFIG_FOLDER}/speciesConstant.config",
    "species constrained": f"{CONFIG_FOLDER}/speciesConstrained.config"
}


def edit_config():
    chosen_config_file = st.selectbox(
        label="Choose a config file to edit",
        options=sorted(FILE_MAP.keys())
    )

    if chosen_config_file == "initial concentrations":
        show_species = st.checkbox("Show possible species?")
        if show_species:
            st.subheader("Possible species list")
            st.text(read_file(f"{CONFIG_FOLDER}/mechanism.species"))

    content = st_ace(
        value=read_file(FILE_MAP[chosen_config_file])
    )
    write_file(FILE_MAP[chosen_config_file], content)
