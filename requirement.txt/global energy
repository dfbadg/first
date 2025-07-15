import pandas as pd
import plotly.express as px
import folium

# 데이터 불러오기
df = pd.read_csv("data/renewable_energy.csv")

# Plotly - 국가별 재생에너지 비율 막대그래프
fig = px.bar(df.sort_values('Renewable_Percentage', ascending=False),
             x='Country', y='Renewable_Percentage',
             title='국가별 재생에너지 발전 비율 (%)',
             labels={'Renewable_Percentage': '재생에너지 비율'})
fig.show()

# Folium - 지도 시각화
m = folium.Map(location=[20, 0], zoom_start=2)

for i, row in df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=row['Renewable_Percentage'] / 5,
        popup=f"{row['Country']}: {row['Renewable_Percentage']}%",
        color='green',
        fill=True,
        fill_opacity=0.6
    ).add_to(m)

m.save("map.html")
