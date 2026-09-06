from pathlib import Path

PROJECT_DATA_DIR = Path(__file__).resolve().parents[2] / "data"

import streamlit as st
import pandas as pd

st.title("価格推移")

tokyo = pd.read_csv(
    PROJECT_DATA_DIR / "processed/electricity/price_tokyo.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)

st.line_chart(tokyo["price"])
