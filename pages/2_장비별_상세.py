from pathlib import Path

import streamlit as st

import calc


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
WEEK_FILES = {
    "W44 · 지난주": "readiness_W44.csv",
    "W45 · 이번 주": "readiness_W45.csv",
}

st.title("장비별 상세")

week_label = st.selectbox("주차", list(WEEK_FILES))
readiness = calc.load_readiness(str(DATA_DIR / WEEK_FILES[week_label]))
equipment = calc.rate_by_equipment(readiness)

equipment_names = dict(zip(equipment["장비코드"], equipment["장비명"]))
equipment_code = st.selectbox(
    "장비",
    equipment["장비코드"].tolist(),
    format_func=lambda code: f"{code} · {equipment_names[code]}",
)

equipment_summary = equipment.loc[equipment["장비코드"] == equipment_code].iloc[0]
rate_col, runtime_col, planned_col = st.columns(3)
rate_col.metric("가동률", f"{equipment_summary['가동률']:.1f}%")
runtime_col.metric("가동시간 합계", f"{equipment_summary['가동시간']:g}시간")
planned_col.metric("계획시간 합계", f"{equipment_summary['계획시간']:g}시간")

daily = readiness.loc[readiness["장비코드"] == equipment_code].sort_values("일자")
daily_chart = daily.set_index("일자")[["계획시간(h)", "가동시간(h)"]].rename(
    columns={"계획시간(h)": "계획시간", "가동시간(h)": "가동시간"}
)
st.subheader("일별 계획 · 가동시간")
st.line_chart(daily_chart, y_label="시간")
st.dataframe(
    daily[["일자", "장비코드", "장비명", "계획시간(h)", "가동시간(h)"]],
    hide_index=True,
    use_container_width=True,
)
