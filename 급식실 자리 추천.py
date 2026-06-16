import stremit as st
st.title('급식자리추천')
st.write('냠냠')
import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(
    page_title="급식실 자리 추천 챗봇",
    page_icon="🍽️",
)

st.title("🍽️ 급식실 자리 추천 챗봇")
st.caption("상황에 맞는 급식실 자리를 추천해드립니다.")

# API 키 
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 초기화 오류: {e}")
    st.stop()

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요! 🍽️\n\n"
                "급식실 자리 추천 챗봇입니다.\n"
                "예시:\n"
                "- 혼자 조용히 먹고 싶어요\n"
                "- 친구 4명이랑 같이 먹어요\n"
                "- 빨리 먹고 수업 가야 해요\n"
                "- 시끄러운 곳은 싫어요"
            ),
        }
    ]

# 이전 대화 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
user_input = st.chat_input("어떤 자리를 찾고 있나요?")

if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # 대화 기록 문자열 생성
    conversation = ""
    for m in st.session_state.messages:
        role = "사용자" if m["role"] == "user" else "챗봇"
        conversation += f"{role}: {m['content']}\n"

    system_prompt = """
너는 학교 급식실 자리 추천 전문가다.

사용자의 상황을 분석해서 가장 적합한 자리를 추천해라.

추천 시 다음을 고려해라.
- 혼밥 여부
- 인원수
- 조용한 환경 선호 여부
- 빠른 식사 필요 여부
- 친구와 대화 목적 여부
- 출입구와의 거리
- 배식대와의 거리

답변 형식:
1. 추천 자리
2. 추천 이유
3. 추가 팁

친절하고 간결하게 답변해라.
"""

    try:
        with st.chat_message("assistant"):
            with st.spinner("자리 추천 중..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=f"""
{system_prompt}

대화 기록:
{conversation}

사용자 요청:
{user_input}
""",
                )

                answer = response.text

                st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

    except Exception as e:
        error_msg = (
            f"오류가 발생했습니다.\n\n"
            f"오류 내용: {str(e)}"
        )

        with st.chat_message("assistant"):
            st.error(error_msg)

        st.session_state.messages.append(
            {"role": "assistant", "content": error_msg}
        )
