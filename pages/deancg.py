import streamlit as st
import pandas as pd
import plotly.express as px

# 데이터 생성
data = {
    "Country": ["Korea", "Korea", "Korea", "Germany", "Germany", "Germany", "USA", "USA", "USA"],
    "Year": [2010, 2015, 2020, 2010, 2015, 2020, 2010, 2015, 2020],
    "Renewable_Energy_GWh": [12000, 18000, 25000, 50000, 90000, 120000, 40000, 65000, 90000]
}
df = pd.DataFrame(data)

# 사이드바 메뉴
st.sidebar.title("메뉴")
page = st.sidebar.radio("페이지 선택", ["홈", "국가별 생산량 추이", "데이터 소개", "재생에너지 비율"])

if page == "홈":
    st.title("재생에너지 발표")
    st.write("""
        재생에너지는 환경 보호와 지속가능한 발전의 핵심 요소입니다.
        본 발표에서는 주요 국가들의 재생에너지 생산량 추이를 살펴봅니다.
    """)
    st.image("https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80", use_column_width=True)

elif page == "국가별 생산량 추이":
    st.title("국가별 재생에너지 생산량 추이")

    # 선 그래프
    fig_line = px.line(
        df,
        x="Year",
        y="Renewable_Energy_GWh",
        color="Country",
        markers=True,
        title="선 그래프: 국가별 재생에너지 생산량 추이 (GWh 단위)",
        labels={"Renewable_Energy_GWh": "생산량 (GWh)", "Year": "연도"}
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # 막대 그래프 (2020년만)
    df_2020 = df[df["Year"] == 2020]
    fig_bar = px.bar(
        df_2020,
        x="Country",
        y="Renewable_Energy_GWh",
        color="Country",
        title="막대 그래프: 2020년 국가별 재생에너지 생산량",
        labels={"Renewable_Energy_GWh": "생산량 (GWh)", "Country": "국가"}
    )
    st.plotly_chart(fig_bar, use_container_width=True)

elif page == "데이터 소개":
    st.title("데이터 소개")
    st.write("""
        - 데이터는 2010년, 2015년, 2020년 세 시점의 주요 국가별 재생에너지 생산량(GWh 단위)을 포함합니다.
        - 국가: 한국, 독일, 미국
        - 생산량은 국가별 재생에너지 발전소에서 생산된 전력량을 나타냅니다.
    """)
    st.dataframe(df)

elif page == "재생에너지 비율":
    st.title("2020년 재생에너지 생산 비율 (원형 차트)")
    df_2020 = df[df["Year"] == 2020]

    fig_pie = px.pie(
        df_2020,
        names="Country",
        values="Renewable_Energy_GWh",
        title="2020년 국가별 재생에너지 생산 비율",
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)
