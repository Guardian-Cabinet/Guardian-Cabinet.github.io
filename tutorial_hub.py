import streamlit as st
import os

st.set_page_config(page_title="Streamlit Tutorial Hub", layout="wide")

st.sidebar.title("📚 Tutorial Chapters")
chapters = {
    "Chapter 1: 기본 출력": "1_app.py",
    "Chapter 2: 데이터 위젯": "2_app.py",
    "Chapter 3: 상호작용 레이아웃": "3_app.py",
    "Chapter 4: 시각화 실습": "4_app.py"
}

selection = st.sidebar.radio("Go to", list(chapters.keys()))

st.title(selection)

file_path = os.path.join("tutorials", chapters[selection])

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    
    # Execute the code in the local context
    # Note: Streamlit execution model means we might need to be careful with imports.
    # A better way is to move the logic into functions, but for a quick hack:
    exec(code, globals())
else:
    st.error(f"File {file_path} not found.")

st.sidebar.markdown("---")
st.sidebar.info("이 앱은 개별 튜토리얼 파일들을 하나로 통합한 대시보드입니다.")
