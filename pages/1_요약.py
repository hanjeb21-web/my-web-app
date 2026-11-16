from pathlib import Path

import streamlit as st

import calc


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
previous_week = calc.load_readiness(str(DATA_DIR / "readiness_W44.csv"))
current_week = calc.load_readiness(str(DATA_DIR / "readiness_W45.csv"))

previous_rate = calc.total_rate(previous_week)
current_rate = calc.total_rate(current_week)
change = current_rate - previous_rate
target_gap = current_rate - 90

st.title("요약")

current_col, previous_col, target_col = st.columns(3)
current_col.metric("이번 주 전체 가동률", f"{current_rate:.1f}%", f"{change:+.1f}%p")
previous_col.metric("지난주 전체 가동률", f"{previous_rate:.1f}%")
target_col.metric("목표 90%와 차이", f"{target_gap:+.1f}%p")

st.subheader("장비별 이번 주 가동률")
equipment_rates = calc.rate_by_equipment(current_week)
st.bar_chart(equipment_rates.set_index("장비명")["가동률"], y_label="가동률 (%)")
