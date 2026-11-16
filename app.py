import streamlit as st

import db


db.init_db()

pages = [
    st.Page("pages/1_요약.py", title="요약", default=True),
    st.Page("pages/2_장비별_상세.py", title="장비별 상세"),
    st.Page("pages/3_주간_비교.py", title="주간 비교"),
    st.Page("pages/4_정비_요청.py", title="정비 요청"),
]

navigation = st.navigation(pages)
navigation.run()
