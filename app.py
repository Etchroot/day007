import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = "gpt-4o-mini"  # 🔌 사용할 모델

st.set_page_config(page_title="간단 챗봇", page_icon="💬")
st.title("💬 간단 챗봇")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error(".env에 OPENAI_API_KEY가 없어요. .env.example을 보고 채워 주세요")
    st.stop()

client = OpenAI(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "너는 친절한 한국어 어시스턴트야."}
    ]

with st.sidebar:
    if st.button("대화 초기화"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()

# 이전 대화 표시 (system 메시지는 숨김)
for m in st.session_state.messages[1:]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("메시지를 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # 🔌 API 호출
            stream = client.chat.completions.create(
                model=MODEL,
                messages=st.session_state.messages,
                stream=True,
                timeout=30,
            )
            reply = st.write_stream(
                chunk.choices[0].delta.content or ""
                for chunk in stream
                if chunk.choices
            )
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception:
            st.error("답변을 가져오지 못했어요. 키·사용량·네트워크를 확인해 주세요.")
