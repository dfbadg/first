import streamlit as st
import plotly.express as px

st.set_page_config(page_title="재생에너지 비율", layout="wide")
st.title("국가별 재생에너지 비율 및 특징")

countries = ["대한민국", "독일", "미국", "중국", "노르웨이", "인도", "브라질", "일본"]
ratios = [7.5, 46.2, 20.1, 29.0, 98.0, 22.3, 83.5, 19.8]
features = [
    "태양광 위주, 낮은 비율. 석탄 의존 여전.",
    "풍력·태양광 중심, 원전 탈피 중.",
    "풍력·수력 확대, 주별 차이 큼.",
    "풍력·태양광 세계 최대, 석탄 병행.",
    "거의 전량 수력발전, 비율 세계 최고.",
    "농촌 태양광 확대, 에너지 접근 개선.",
    "수력 위주, 전력의 80% 이상 재생에너지.",
    "지열·태양광 개발 중, 아직 화석연료 의존.",
]

fig = px.bar(x=countries, y=ratios, labels={"x": "국가", "y": "비율(%)"}, text=ratios,
             title="국가별 재생에너지 비율")
fig.update_traces(texttemplate="%{text}%", textposition="outside")
fig.update_layout(yaxis_range=[0, 100])

st.plotly_chart(fig, use_container_width=True)

st.subheader("국가별 재생에너지 특징")
for i in range(len(countries)):
    st.markdown(f"**{countries[i]}**: {features[i]}")
