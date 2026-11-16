from pathlib import Path

import pandas as pd
import streamlit as st

import calc


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
previous_week = calc.load_readiness(str(DATA_DIR / "readiness_W44.csv"))
current_week = calc.load_readiness(str(DATA_DIR / "readiness_W45.csv"))
comparison = calc.compare_weeks(previous_week, current_week)

st.title("주간 비교")

up_col, down_col = st.columns(2)
with up_col:
    st.subheader("상승 상위 3")
    st.dataframe(comparison.head(3), hide_index=True, use_container_width=True)
with down_col:
    st.subheader("하락 상위 3")
    st.dataframe(
        comparison.tail(3).sort_values("증감", ascending=True),
        hide_index=True,
        use_container_width=True,
    )

st.subheader("전체 장비 비교")
st.dataframe(comparison, hide_index=True, use_container_width=True)

st.subheader("비고가 있는 일별 행")
previous_notes = previous_week.loc[
    previous_week["비고"].fillna("").astype(str).str.strip().ne("")
].copy()
current_notes = current_week.loc[
    current_week["비고"].fillna("").astype(str).str.strip().ne("")
].copy()
previous_notes.insert(0, "주차", "W44")
current_notes.insert(0, "주차", "W45")
notes = pd.concat([previous_notes, current_notes], ignore_index=True)

if notes.empty:
    st.info("비고가 있는 행이 없습니다.")
else:
    st.dataframe(notes, hide_index=True, use_container_width=True)
