import pandas as pd
import plotly.express as px
import streamlit as st

# CSV 불러오기
df = pd.read_csv("data/renewable_energy.csv")

# 그래프 생성
fig = px.bar(df.sort_values('Renewable_Percentage', ascending=False),
             x='Country', y='Renewable_Percentage',
             title='국가별 재생에너지 발전 비율 (%)')

# Streamlit에 그래프 출력
st.plotly_chart(fig)

# 설명 출력
st.markdown("### 🌍 국가별 에너지 특징 분석")

# 국가별 자동 분석 문장 생성
for i, row in df.iterrows():
    percent = row["Renewable_Percentage"]
    country = row["Country"]

    if percent >= 60:
        summary = f"✅ **{country}**은/는 재생에너지 비율이 매우 높으며, 수력 등 친환경 에너지 중심입니다."
    elif percent >= 30:
        summary = f"🔶 **{country}**은/는 재생에너지 확대가 잘 진행 중입니다."
    elif percent >= 15:
        summary = f"⚠️ **{country}**은/는 전환 단계에 있으며, 더 많은 투자가 필요합니다."
    else:
        summary = f"❌ **{country}**은/는 재생에너지 비중이 낮아 개선이 시급합니다."

    st.markdown(summary)
