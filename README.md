# visualisation-tools

---

Welcome to my hastily put-together repo featuring a collection of visual tools for learning various subjects.

These make heavy use of a Python package called [streamlit](https://streamlit.io/) for the web based applications.

## Installation

---

- Make sure you have Python 3.9+ and conda installed
- From terminal/anaconda prompt `conda env create -f vt-env.yml`

## Usage

---
Using a terminal of your choice navigate to one of subject folders and start a streamlit application.

```bash
conda activate vt-env
cd PHYS430
streamlit run overview.py
```

***Alternatively***, you can navigate to one of the sub-directories and run just the page for that.

```bash
conda activate vt-env
cd PHYS430/DaisyWorld
streamlit run page_view.py
```

## Notes

---
This is very much a work in progress, I will be adding to it over time.

Feel free to make suggestions / requests.

