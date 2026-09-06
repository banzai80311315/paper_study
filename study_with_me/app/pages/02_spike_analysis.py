from pathlib import Path

PROJECT_DATA_DIR = Path(__file__).resolve().parents[2] / "data"

import streamlit as st
import pandas as pd

st.title("スパイク分析")

tokyo = pd.read_csv(
    PROJECT_DATA_DIR / "processed/electricity/price_tokyo.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)

spike = tokyo[tokyo["u"] == 1]

st.dataframe(spike)
