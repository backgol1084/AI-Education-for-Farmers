import streamlit as st
from google import genai

# 수정된 올바른 설정 함수
st.set_page_config(page_title="제미나이 체험 실습장", page_icon="🤖")

st.title("🤖 생성형 AI 제미나이(Gemini) 체험하기")
st.write("로그인 없이 간편하게 제미나이의 성능을 테스트해 보세요!")

# Secrets에서 API 키 안전하게 가져오기
API_KEY = st.secrets.get("GEMINI_API_KEY", "")

if not API_KEY:
    st.warning("⚠️ Streamlit Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
else:
    client = genai.Client(api_key=API_KEY)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("제미나이에게 물어보고 싶은 내용을 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("생각 중입니다..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt,
                    )
                    reply = response.text
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
