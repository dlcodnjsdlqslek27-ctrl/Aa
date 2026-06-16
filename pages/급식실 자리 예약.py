import streamlit as st
from google import genai
from datetime import date

st.set_page_config(
    page_title="급실실 자리예약",
    page_icon="💺",
    layout="wide"
)

# --------------------
# Gemini API
# --------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("GEMINI_API_KEY 설정을 확인해주세요.")
    st.stop()

st.title("💺 급실실 자리예약")
st.caption("항공권 예약 화면처럼 예약 정보를 입력하세요.")

# --------------------
# 예약 입력 영역
# --------------------
col1, col2, col3 = st.columns(3)

with col1:
    seat_zone = st.selectbox(
        "좌석 구역",
        [
            "A구역",
            "B구역",
            "C구역",
            "D구역"
        ]
    )

with col2:
    reserve_date = st.date_input(
        "이용 날짜",
        min_value=date.today()
    )

with col3:
    people = st.number_input(
        "인원 수",
        min_value=1,
        max_value=10,
        value=1
    )

time_slot = st.selectbox(
    "이용 시간",
    [
        "09:00~11:00",
        "11:00~13:00",
        "13:00~15:00",
        "15:00~17:00",
        "17:00~19:00"
    ]
)

# --------------------
# 조회 버튼
# --------------------
if st.button("예약 가능 여부 조회", use_container_width=True):

    try:

        prompt = f"""
        다음 예약 정보를 기반으로 예약 안내를 작성해줘.

        좌석구역: {seat_zone}
        이용일: {reserve_date}
        이용시간: {time_slot}
        인원수: {people}

        아래 형식으로 작성:
        1. 예약 정보 요약
        2. 이용 안내
        3. 주의사항

        친절하게 작성해줘.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        st.success("예약 조회 완료")

        st.subheader("예약 결과")

        st.markdown(response.text)

    except Exception as e:
        st.error(f"오류 발생: {e}")

# --------------------
# 예약 현황 예시
# --------------------
st.divider()

st.subheader("현재 좌석 현황")

seat_data = {
    "A구역": 12,
    "B구역": 8,
    "C구역": 5,
    "D구역": 15
}

for zone, remain in seat_data.items():
    st.metric(zone, f"{remain}석")
