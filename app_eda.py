
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

class EDA:
    def __init__(self):
        st.set_page_config(layout="wide")
        st.title("지역별 인구 분석 웹 앱")

    def run(self):
        st.write("`population_trends.csv` 파일을 업로드하여 연도별 지역 인구 추이를 분석합니다.")

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

        st.write("`세종` 지역의 '-' 값을 0으로 치환하고, '인구', '출생아수(명)', '사망자수(명)' 열을 숫자로 변환했습니다.")
        st.dataframe(df.head())

        st.subheader("Data Summary Statistics (`df.describe()`)")
        st.write(df.describe())

        st.subheader("DataFrame Structure (`df.info()`)")
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

        st.subheader("Missing Values Check")
        st.write(df.isnull().sum())

        st.subheader("Duplicate Rows Check")
        st.write(f"Number of duplicate rows: {df.duplicated().sum()}")

if __name__ == "__main__":
    app = EDA()
    app.run()
