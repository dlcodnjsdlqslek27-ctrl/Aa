import streamlit as st
from google import genai

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="급실실 자리예약 챗봇",
    page_icon="💺",
)

st.title("💺 급실실 자리예약 챗봇")
st.caption("급실실 자리 예약 관련 문의를 도와드립니다.")

# -----------------------------
# API Key 불러오기
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("GEMINI_API_KEY가 Secrets에 설정되지 않았습니다.")
    st.stop()

# -----------------------------
# Gemini Client 생성
# -----------------------------
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# -----------------------------
# 시스템 프롬프트
# -----------------------------
SYSTEM_PROMPT = """
너는 '급실실 자리예약 전용 챗봇'이다.

역할:
- 급실실 자리 예약 관련 문의 응대
- 이용 방법 안내
- 예약 절차 설명
- 좌석 이용 규칙 안내

규칙:
- 항상 친절하고 간결하게 답변한다.
- 급실실 자리예약과 관련 없는 질문에는
  '저는 급실실 자리예약 관련 문의만 도와드릴 수 있습니다.'
  라고 답한다.
"""

# -----------------------------
# 채팅 기록 초기화
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# 이전 대화 표시
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
user_input = st.chat_input("질문을 입력하세요")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        # 대화 이력 구성
        conversation = SYSTEM_PROMPT + "\n\n"

        for msg in st.session_state.messages:
            role = "사용자" if msg["role"] == "user" else "챗봇"
            conversation += f"{role}: {msg['content']}\n"

        # Gemini 호출
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=conversation,
        )

        answer = response.text

    except Exception as e:
        answer = (
            "죄송합니다. 현재 응답을 생성하는 중 오류가 발생했습니다.\n\n"
            f"오류 내용: {str(e)}"
        )

    # 응답 저장
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    with st.chat_message("assistant"):
        st.markdown(answer)

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.header("설정")

    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()
