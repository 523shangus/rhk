import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io

# ✅ 페이지 설정은 반드시 맨 위에!
st.set_page_config(layout="wide")

# ✅ 배경을 연한 빨간색으로 설정
st.markdown("""
    <style>
    .stApp {
        background-color: #ffdddd;
    }
    </style>
""", unsafe_allow_html=True)

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

class EDA:
    def __init__(self):
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
        st.dataframe(df.head())
        st.write(df.describe())
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())
        st.write(df.isnull().sum())
        st.write(f"Number of duplicate rows: {df.duplicated().sum()}")

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
        df.loc[df['지역'] == '세종', df.columns] = df.loc[df['지역'] == '세종', df.columns].replace('-', '0')
        for col in ['인구', '출생아수(명)', '사망자수(명)']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        region_map = {
            '서울':'Seoul', '부산':'Busan', '대구':'Daegu', '인천':'Incheon',
            '광주':'Gwangju', '대전':'Daejeon', '울산':'Ulsan', '세종':'Sejong',
            '경기':'Gyeonggi', '강원':'Gangwon', '충북':'Chungbuk', '충남':'Chungnam',
            '전북':'Jeonbuk', '전남':'Jeonnam', '경북':'Gyeongbuk', '경남':'Gyeongnam', '제주':'Jeju'
        }
        df = df[df['지역'] != '전국']
        df['Region_EN'] = df['지역'].map(region_map)
        latest = df['연도'].max()
        past = latest - 4
        recent = df[df['연도'].isin([past, latest])]
        pivot = recent.pivot(index='Region_EN', columns='연도', values='인구')
        pivot = pivot.dropna()
        change = (pivot[latest] - pivot[past]) / 1000
        change_rate = ((pivot[latest] - pivot[past]) / pivot[past]) * 100
        fig1, ax1 = plt.subplots(figsize=(12, 6))
        sns.barplot(x=change.values, y=change.index, ax=ax1, palette='Blues_d')
        ax1.set_title(f'Population Change ({past}-{latest})')
        st.pyplot(fig1)
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        sns.barplot(x=change_rate.values, y=change_rate.index, ax=ax2, palette='Oranges')
        ax2.set_title(f'Population Change Rate (%) ({past}-{latest})')
        st.pyplot(fig2)

    def change_analysis(self, df):
        st.header("4. Change Analysis")
        df.loc[df['지역'] == '세종', df.columns] = df.loc[df['지역'] == '세종', df.columns].replace('-', '0')
        for col in ['인구', '출생아수(명)', '사망자수(명)']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df[df['지역'] != '전국'].copy()
        df = df.sort_values(by=['지역', '연도'])
        df['증감'] = df.groupby('지역')['인구'].diff()
        top = df.dropna(subset=['증감']).nlargest(100, '증감', keep='all')
        top['증감'] = top['증감'].apply(lambda x: f'{x:,.0f}')
        st.dataframe(top[['연도', '지역', '인구', '증감']])

    def visualization(self, df):
        st.header("5. Visualization")
        df.loc[df['지역'] == '세종', df.columns] = df.loc[df['지역'] == '세종', df.columns].replace('-', '0')
        for col in ['인구', '출생아수(명)', '사망자수(명)']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df[df['지역'] != '전국']
        region_map = {
            '서울':'Seoul', '부산':'Busan', '대구':'Daegu', '인천':'Incheon',
            '광주':'Gwangju', '대전':'Daejeon', '울산':'Ulsan', '세종':'Sejong',
            '경기':'Gyeonggi', '강원':'Gangwon', '충북':'Chungbuk', '충남':'Chungnam',
            '전북':'Jeonbuk', '전남':'Jeonnam', '경북':'Gyeongbuk', '경남':'Gyeongnam', '제주':'Jeju'
        }
        df['Region_EN'] = df['지역'].map(region_map)
        pivot = df.pivot_table(index='연도', columns='Region_EN', values='인구', fill_value=0)
        pivot = pivot / 1000
        fig, ax = plt.subplots(figsize=(12, 6))
        pivot.plot(kind='area', stacked=True, cmap='tab20', ax=ax)
        ax.set_title('Regional Population Trend (stacked)')
        ax.set_xlabel('Year')
        ax.set_ylabel('Population (thousands)')
        ax.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
        st.pyplot(fig)

if __name__ == "__main__":
    app = EDA()
    app.run()
