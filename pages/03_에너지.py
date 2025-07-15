import pandas as pd
import plotly.express as px
import streamlit as st  # 꼭 필요함!

# 올바른 경로
df = pd.read_csv("data/renewable_energy.csv")

fig = px.bar(df.sort_values('Renewable_Percentage', ascending=False),
             x='Country', y='Renewable_Percentage',
             title='국가별 재생에너지 발전 비율 (%)')

# 핵심 출력 함수!
st.plotly_chart(fig)
