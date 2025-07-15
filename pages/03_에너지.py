import pandas as pd
import plotly.express as px

# 올바른 경로
df = pd.read_csv("data/renewable_energy.csv")

fig = px.bar(df.sort_values('Renewable_Percentage', ascending=False),
             x='Country', y='Renewable_Percentage',
             title='국가별 재생에너지 발전 비율 (%)')
fig.show()
