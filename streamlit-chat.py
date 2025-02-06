import streamlit as st
from annotated_text import annotated_text
from streamlit_chat import message
import json
import requests
import time

URL = "https://humble-space-computing-machine-4qqg9rvrg7927qj4-8080.app.github.dev/score"
HEADERS = {"Content-Type": "application/json"}
EXCLUDED_ANSWER_TEXT = "이 질문은 답변하기 어려워요 😥"  # 특정 문구 포함 시 카테고리 숨김


st.title("알딱깔딱봇")

# 디버깅용
# response_data = requests.post(URL, json={"text": "알바시렁"}, headers=HEADERS)
# formatted_response = response_data.json()
# print(formatted_response)

# ✅ 채팅 기록을 저장할 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ 카테고리 출력 함수
def display_categories(categories):
    """카테고리를 리스트로 변환하고 `annotated_text()`로 출력"""
    if isinstance(categories, str):
        categories = [cat.strip() for cat in categories.split(",")]
    
    category_tuples = [(f"# {category}", "") for category in categories]
    
    # ✅ 간격을 추가하기 위해 각 카테고리 사이에 공백 튜플 추가
    spaced_category_tuples = []
    for cat in category_tuples:
        spaced_category_tuples.append(cat)
        spaced_category_tuples.append(("  "))  # 공백 추가

    # ✅ `annotated_text()`를 한 번만 호출
    annotated_text(*spaced_category_tuples)


def display_response(message):
    """API 응답을 UI에 출력 (특정 응답 포함 시 카테고리 숨김)"""
    answer_text = message.get("answer", "응답 없음")

    with st.chat_message("assistant"):
        # ✅ 특정 문구 포함 시 카테고리 숨김
        if EXCLUDED_ANSWER_TEXT not in answer_text:
            display_categories(message.get("category", "카테고리 없음"))

        # ✅ 답변을 Markdown JSON 블록으로 출력
        st.markdown(
            f"""
            <div style="overflow-y: auto; padding: 15px; 
                    border-radius: 10px; background-color: rgba(38, 39, 48, 0.5);
                    color: white; font-size: 16px; line-height: 1.5;
                    display: inline-block; width: 100%; word-wrap: break-word;">
                <pre style="white-space: pre-wrap; font-family: 'Courier New', monospace; margin: 0;">
{answer_text}
                </pre>
            </div>
            """,
            unsafe_allow_html=True
        )


# ✅ 채팅 히스토리 출력 (이전 메시지 유지)
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        display_response(msg)
    else:
        with st.chat_message("user"):
            st.markdown(msg["content"])

# ✅ 사용자 입력 처리
if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    # ✅ 세션 상태에 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})

    # ✅ API 요청
    with st.spinner("Wait for it..."):
        response_data = requests.post(URL, json={"question": prompt}, headers=HEADERS)

    # ✅ API 응답 처리
    try:
        formatted_response = response_data.json()
    except requests.exceptions.JSONDecodeError:
        formatted_response = {"answer": "응답 오류", "category": "알 수 없음"}

    time.sleep(0.05)  # UX 개선을 위한 약간의 대기

    # ✅ 응답 표시 및 세션 저장
    display_response(formatted_response)
    st.session_state.messages.append({
        "role": "assistant",
        "category": formatted_response.get("category", "카테고리 없음"),
        "answer": formatted_response.get('answer', '응답 없음')
    })

