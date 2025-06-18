import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pyrebase4 as pyrebase
import time
import io

# ----------------------------
# Firebase 설정
# ----------------------------
firebase_config = {
    "apiKey": "AIzaSyCswFmrOGU3FyLYxwbNPTp7hvQxLfTPIZw",
    "authDomain": "sw-projects-49798.firebaseapp.com",
    "databaseURL": "https://sw-projects-49798-default-rtdb.firebaseio.com",
    "projectId": "sw-projects-49798",
    "storageBucket": "sw-projects-49798.appspot.com",
    "messagingSenderId": "812186368395",
    "appId": "1:812186368395:web:be2f7291ce54396209d78e"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

# ----------------------------
# 세션 상태 초기화
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

# ----------------------------
# 페이지 설정 및 테마 적용
# ----------------------------
st.set_page_config(layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #1e1e1e !important;
        color: white !important;
    }
    html, body, [class*="css"] {
        background-color: #1e1e1e !important;
        color: white !important;
    }
    .stDataFrame table {
        background-color: #2c2c2c !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ----------------------------
# 로그인/회원가입 화면
# ----------------------------
def login():
    st.title("🔐 로그인")
    email = st.text_input("이메일")
    password = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success("로그인 성공!")
            time.sleep(1)
            st.experimental_rerun()
        except:
            st.error("로그인 실패")

def register():
    st.title("📝 회원가입")
    email = st.text_input("이메일")
    password = st.text_input("비밀번호", type="password")
    name = st.text_input("이름")
    if st.button("회원가입"):
        try:
            auth.create_user_with_email_and_password(email, password)
            db.child("users").child(email.replace(".", "_")).set({"name": name, "email": email})
            st.success("회원가입 완료! 로그인 해주세요.")
            time.sleep(1)
            st.experimental_rerun()
        except:
            st.error("회원가입 실패")

# ----------------------------
# EDA 기능 클래스
# ----------------------------
class EDA:
    def __init__(self):
        st.title("지역별 인구 분석 웹 앱")

    def run(self):
        st.write("`population_trends.csv`파일을 업로드해서 연도별 지역 인구 추이를 분석합니다.")
        uploaded_file = st.file_uploader("Upload population_trends.csv", type=["csv"])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")

            tab1, tab2 = st.tabs(["기초 통계", "연도별 추이"])

            with tab1:
                df.loc[df['지역'] == '세종', df.columns] = df.loc[df['지역'] == '세종', df.columns].replace('-', '0')
                for col in ['인구', '출생아수(명)', '사망자수(명)']:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                st.subheader("📄 Sample Rows")
                st.dataframe(df.head())
                st.subheader("📊 Summary Statistics")
                st.dataframe(df.describe().T.style.format("{:.0f}"))
                st.subheader("🔧 DataFrame Info")
                buffer = io.StringIO()
                df.info(buf=buffer)
                s = buffer.getvalue()
                st.code(s, language='python')

            with tab2:
                national = df[df['지역'] == '전국'].set_index('연도')
                pop = national['인구'].dropna() / 1000
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(pop.index, pop.values, marker='o')
                ax.set_title('National Population Trend (in thousands)')
                ax.set_xlabel('Year')
                ax.set_ylabel('Population (thousands)')
                ax.grid(True)
                st.pyplot(fig)

# ----------------------------
# 메인 앱 라우팅
# ----------------------------
menu = st.sidebar.selectbox("메뉴 선택", ["로그인", "회원가입"] if not st.session_state.logged_in else ["EDA", "로그아웃"])

if menu == "로그인":
    login()
elif menu == "회원가입":
    register()
elif menu == "EDA" and st.session_state.logged_in:
    app = EDA()
    app.run()
elif menu == "로그아웃":
    st.session_state.logged_in = False
    st.session_state.user_email = ""
    st.success("로그아웃 완료")
    time.sleep(1)
    st.experimental_rerun()
else:
    st.warning("로그인 후 이용 가능합니다.")
