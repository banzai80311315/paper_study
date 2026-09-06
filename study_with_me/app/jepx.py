from pathlib import Path

PROJECT_DATA_DIR = Path(__file__).resolve().parents[1] / "data"

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="JEPX Data Viewer",
    layout="wide",
)

st.title("JEPX Data Viewer")

# -------------------------
# データ読み込み
# -------------------------
tokyo = pd.read_csv(
    PROJECT_DATA_DIR / "processed/electricity/price_tokyo.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)

# 年度・年・月を追加
tokyo["year"] = tokyo.index.year
tokyo["month"] = tokyo.index.month

# -------------------------
# サイドバー
# -------------------------
st.sidebar.header("表示条件")

selected_year = st.sidebar.selectbox(
    "表示する年",
    sorted(tokyo["year"].unique()),
)

price_col = st.sidebar.selectbox(
    "表示する価格",
    ["price", "price_scaled"],
)

show_spike_only = st.sidebar.checkbox(
    "スパイク発生日のみ表示",
    value=False,
)

# -------------------------
# データ絞り込み
# -------------------------
df = tokyo[tokyo["year"] == selected_year].copy()

if show_spike_only:
    df = df[df["u"] == 1]

# -------------------------
# 指標表示
# -------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("データ件数", len(df))
col2.metric("平均価格", round(df[price_col].mean(), 2))
col3.metric("最大価格", round(df[price_col].max(), 2))
col4.metric("スパイク回数", int(df["u"].sum()))

# -------------------------
# グラフ
# -------------------------
st.subheader(f"{selected_year}年の価格推移")

st.line_chart(df[price_col])

# -------------------------
# スパイク超過量
# -------------------------
st.subheader("スパイク超過量 x")

st.bar_chart(df["x"])

# -------------------------
# データ表示
# -------------------------
st.subheader("データ確認")

st.dataframe(df)
