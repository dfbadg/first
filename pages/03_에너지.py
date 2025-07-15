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
import folium
import streamlit as st

m = folium.Map(location=[20, 0], zoom_start=2)

for i, row in df.iterrows():
    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=row["Renewable_Percentage"] / 5,
        popup=f"{row['Country']}: {row['Renewable_Percentage']}%",
        color='green',
        fill=True
    ).add_to(m)

st.components.v1.html(m._repr_html_(), height=500)
