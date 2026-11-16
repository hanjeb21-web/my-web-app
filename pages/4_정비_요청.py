from pathlib import Path

import streamlit as st

import calc
import db


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "readiness_W45.csv"
equipment_data = calc.load_readiness(str(DATA_PATH))[["장비코드", "장비명"]].drop_duplicates()
equipment_names = dict(zip(equipment_data["장비코드"], equipment_data["장비명"]))

st.title("정비 요청")
st.caption(f"현재 저장소: {db.backend_name()}")

st.subheader("정비 요청 등록")
with st.form("maintenance_request_form"):
    equipment_code = st.selectbox(
        "장비",
        equipment_data["장비코드"].tolist(),
        format_func=lambda code: f"{code} · {equipment_names[code]}",
    )
    request_title = st.text_area("요청 내용")
    priority = st.selectbox("우선순위", db.PRIORITIES)
    requester_role = st.text_input("요청자 역할명")
    submitted = st.form_submit_button("요청 등록")

if submitted:
    try:
        request_id = db.add_request(equipment_code, request_title, priority, requester_role)
        st.success(f"정비 요청 #{request_id}을(를) 등록했습니다.")
    except ValueError as error:
        st.error(str(error))

st.subheader("정비 요청 목록")
status_filter = st.selectbox("상태 필터", ["전체", *db.STATUSES])
visible_requests = db.list_requests(status=None if status_filter == "전체" else status_filter)

if visible_requests.empty:
    st.info("표시할 정비 요청이 없습니다.")
else:
    display_requests = visible_requests.rename(
        columns={
            "id": "번호",
            "created_at": "접수 시각",
            "equipment_code": "장비코드",
            "title": "요청 내용",
            "priority": "우선순위",
            "requester_role": "요청자 역할명",
            "status": "상태",
        }
    )
    st.dataframe(display_requests, hide_index=True, use_container_width=True)

st.subheader("요청 상태 변경")
all_requests = db.list_requests()
if all_requests.empty:
    st.info("상태를 변경할 정비 요청이 없습니다.")
else:
    request_labels = {
        int(row.id): f"#{row.id} · {row.equipment_code} · {row.title} ({row.status})"
        for row in all_requests.itertuples(index=False)
    }
    with st.form("maintenance_status_form"):
        request_id = st.selectbox(
            "요청 번호",
            all_requests["id"].astype(int).tolist(),
            format_func=lambda value: request_labels[value],
        )
        new_status = st.selectbox("바꿀 상태", db.STATUSES)
        change_submitted = st.form_submit_button("상태 변경")

    if change_submitted:
        db.update_status(int(request_id), new_status)
        st.success(f"정비 요청 #{request_id} 상태를 '{new_status}'(으)로 변경했습니다.")
        st.rerun()
