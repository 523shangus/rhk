import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io

# 페이지 설정
st.set_page_config(layout="wide")

# 다크 테마 적용
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

class EDA:
    def __init__(self):
        st.title("지역별 인구 분석 웹 앱")

    def run(self):
        st.write("`population_trends.csv`파일을 업로드해서 연동별 지역 인구 추이를 분석합니다.")
        uploaded_file = st.file_uploader("Upload population_trends.csv", type=["csv"])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")

            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "Basic Statistics", "Annual Trends", "Regional Analysis", "Change Analysis", "Visualization"
            ])

            with tab1:
                self.basic_statistics(df.copy())
            with tab2:
                self.annual_trends(df.copy())
            with tab3:
                self.regional_analysis(df.copy())
            with tab4:
                self.change_analysis(df.copy())
            with tab5:
                self.visualization(df.copy())
        else:
            st.info("Please upload a CSV file to begin analysis.")

    def basic_statistics(self, df):
        st.header("1. Basic Statistics")

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

        st.subheader("❗ Missing Values")
        st.dataframe(df.isnull().sum().reset_index().rename(columns={"index": "Column", 0: "Missing Count"}))

        st.subheader("📌 Duplicate Check")
        dupes = df.duplicated().sum()
        st.write(f"중복된 행 수: **{dupes}개**")

    def annual_trends(self, df):
        st.header("2. Annual Trends")
        df.loc[df['지역'] == '세종', df.columns] = df.loc[df['지역'] == '세종', df.columns].replace('-', '0')
        for col in ['인구', '출생아수(명)', '사망자수(명)']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        national = df[df['지역'] == '전국'].set_index('연도')
        pop = national['인구'].dropna() / 1000
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(pop.index, pop.values, marker='o')
        ax.set_title('National Population Trend (in thousands)')
        ax.set_xlabel('Year')
        ax.set_ylabel('Population (thousands)')
        ax.grid(True)
        try:
            recent = national.tail(3)
            avg_birth = recent['출생아수(명)'].mean()
            avg_death = recent['사망자수(명)'].mean()
            last_year = national.index.max()
            last_pop = national.loc[last_year, '인구']
            future_year = 2035
            predict = last_pop + (avg_birth - avg_death) * (future_year - last_year)
            predict /= 1000
            ax.plot(future_year, predict, 'rx', markersize=10)
            ax.annotate(f'{predict:.1f}K', (future_year, predict),
                        textcoords="offset points", xytext=(5,-10), ha='center')
        except:
            st.warning("Prediction failed.")
        st.pyplot(fig)

    def regional_analysis(self, df):
        st.header("3. Regional Analysis")
        st.info("This section is under development.")

    def change_analysis(self, df):
        st.header("4. Change Analysis")
        st.info("This section is under development.")

    def visualization(self, df):
        st.header("5. Visualization")
        st.info("This section is under development.")

if __name__ == "__main__":
    app = EDA()
    app.run()
