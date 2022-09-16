import subprocess
import time

import streamlit as st


def run_atchem2(show_output=False):
    st.info("Running AtChem2")
    t_start = time.time()

    result = subprocess.run("./atchem2", capture_output=True, text=True)

    try:
        result.check_returncode()
        if show_output:
            st.subheader("Output:")
            st.text(result.stdout)
    except subprocess.CalledProcessError as e:
        st.subheader("Errors:")
        st.write(result.stderr)
        raise e

    t_taken = time.time() - t_start
    st.success(f"Done! Took {t_taken} s")
