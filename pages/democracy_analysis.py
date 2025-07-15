# 필터링 및 비교 섹션
    st.subheader("🔍 필터링 및 비교")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_types = st.multiselect(
            "민주주의 유형 선택",
            df['democracy_type'].unique(),
            default=df['democracy_type'].unique()
        )
    
    with col2:
        min_score, max_score = st.slider(
            "민주주의 지수 범위",
            min_value=float(df['democracy_index'].min()),
            max_value=float(df['democracy_index'].max()),
            value=(float(df['democracy_index'].min()), float(df['democracy_index'].max()))
        )
    
    # 필터된 데이터
    filtered_df = df[
        (df['democracy_type'].isin(selected_types)) &
        (df['democracy_index'] >= min_score) &
        (df['democracy_index'] <= max_score)
    ]
    
    if not filtered_df.empty:
        # 비교 지도 (이전 vs 현재)
        col1, col2 = st.columns(2)
        
        with col1:
            # 전체 데이터 지도
            fig_all = px.scatter_geo(
                df,
                lat='latitude',
                lon='longitude',
                hover_name='country',
                hover_data=['democracy_index', 'democracy_type'],
                color='democracy_type',
                color_discrete_map=color_map,
                size='democracy_index',
                size_max=15,
                title="전체 데이터"
            )
            fig_all.update_layout(height=400)
            st.plotly_chart(fig_all, use_container_width=True)
        
        with col2:
            # 필터된 데이터 지도
            fig_filtered = px.scatter_geo(
                filtered_df,
                lat='latitude',
                lon='longitude',
                hover_name='country',
                hover_data=['democracy_index', 'democracy_type'],
                color='democracy_type',
                color_discrete_map=color_map,
                size='democracy_index',
                size_max=15,
                title=f"필터된 데이터 ({len(filtered_df)}개국)"
            )
            fig_filtered.update_layout(height=400)
            st.plotly_chart(fig_filtered, use_container_width=True)
    else:
        st.warning("선택한 조건에 맞는 국가가 없습니다.")
    
    # 거리 기반 분석
    st.subheader("📏 거리 기반 분석")
    
    reference_country = st.selectbox(
        "기준 국가 선택",
        df['country'].tolist()
    )
    
    if reference_country:
        ref_row = df[df['country'] == reference_country].iloc[0]
        
        # 거리 계산 (단순 유클리드 거리)
        def calculate_distance(row):
            return ((row['latitude'] - ref_row['latitude'])**2 + 
                   (row['longitude'] - ref_row['longitude'])**2)**0.5
        
        df['distance_from_ref'] = df.apply(calculate_distance, axis=1)
        
        # 가장 가까운 5개국
        nearest_countries = df[df['country'] != reference_country].nsmallest(5, 'distance_from_ref')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**{reference_country}와 가장 가까운 5개국:**")
            for _, row in nearest_countries.iterrows():
                st.write(f"• {row['country']} (지수: {row['democracy_index']})")
        
        with col2:
            # 근처 국가들의 지도
            nearby_df = pd.concat([df[df['country'] == reference_country], nearest_countries])
            
            fig_nearby = px.scatter_geo(
                nearby_df,
                lat='latitude',
                lon='longitude',
                hover_name='country',
                hover_data=['democracy_index', 'democracy_type'],
                color='democracy_type',
                color_discrete_map=color_map,
                size='democracy_index',
                size_max=20,
                title=f"{reference_country} 주변 국가들"
            )
            
            # 기준 국가 강조
            fig_nearby.add_trace(
                go.Scattergeo(
                    lon=[ref_row['longitude']],
                    lat=[ref_row['latitude']],
                    marker=dict(size=25, color='red', symbol='star'),
                    name=f"{reference_country} (기준)",
                    hoverinfo='text',
                    hovertext=f"{reference_country}<br>민주주의 지수: {ref_row['democracy_index']}"
                )
            )
            
            fig_nearby.update_layout(height=400)
            st.plotly_chart(fig_nearby, use_container_width=True)import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.patches import Rectangle
import io

# 페이지 설정
st.set_page_config(
    page_title="민주주의 지수 분석",
    page_icon="🗳️",
    layout="wide"
)

# 데이터 로드 함수
@st.cache_data
def load_data():
    democracy_data = {
        'country': [
            'Norway', 'Iceland', 'Sweden', 'New Zealand', 'Finland',
            'Denmark', 'Ireland', 'Taiwan', 'Australia', 'Switzerland',
            'Netherlands', 'Canada', 'Uruguay', 'United Kingdom', 'Luxembourg',
            'Germany', 'South Korea', 'Japan', 'United States', 'France',
            'Israel', 'Italy', 'Spain', 'Botswana', 'South Africa',
            'India', 'Brazil', 'Poland', 'Hungary', 'Turkey',
            'Russia', 'China', 'Iran', 'North Korea', 'Saudi Arabia'
        ],
        'democracy_index': [
            9.81, 9.37, 9.26, 9.25, 9.20,
            9.09, 9.00, 8.99, 8.90, 8.89,
            8.88, 8.87, 8.85, 8.28, 8.68,
            8.67, 8.09, 8.15, 7.85, 7.99,
            7.93, 7.69, 8.07, 7.83, 7.24,
            7.04, 6.86, 6.93, 5.49, 4.35,
            2.28, 2.21, 2.20, 1.08, 1.98
        ],
        'latitude': [
            60.472, 64.963, 60.128, -40.900, 61.924,
            56.263, 53.413, 23.697, -25.274, 46.818,
            52.132, 56.130, -32.522, 55.378, 49.815,
            51.165, 35.907, 36.204, 37.090, 46.227,
            31.046, 41.871, 40.463, -22.328, -30.559,
            20.593, -14.235, 51.919, 47.162, 38.963,
            61.524, 35.861, 32.427, 40.339, 23.885
        ],
        'longitude': [
            8.468, -19.020, 18.643, 174.885, 25.748,
            9.501, -8.243, 120.960, 133.775, 8.227,
            5.291, -106.346, -55.765, -3.435, 6.129,
            10.451, 127.766, 138.252, -95.712, 2.213,
            34.851, 12.567, -3.749, 24.684, 22.937,
            78.962, -51.925, 19.145, 19.503, 35.243,
            105.318, 104.195, 53.688, 127.510, 45.079
        ]
    }
    
    df = pd.DataFrame(democracy_data)
    
    # 민주주의 수준별 분류
    def classify_democracy(score):
        if score >= 8.0:
            return 'Full Democracy'
        elif score >= 6.0:
            return 'Flawed Democracy'
        elif score >= 4.0:
            return 'Hybrid Regime'
        else:
            return 'Authoritarian'
    
    df['democracy_type'] = df['democracy_index'].apply(classify_democracy)
    
    # 지역 분류
    def classify_region(lat):
        if lat > 50:
            return 'Northern Europe/North America'
        elif lat > 25:
            return 'Europe/North America/Asia'
        elif lat > -25:
            return 'Africa/Asia/Central America'
        else:
            return 'Southern Africa/Oceania'
    
    df['region'] = df['latitude'].apply(classify_region)
    
    return df

# 색상 매핑
color_map = {
    'Full Democracy': '#2E8B57',
    'Flawed Democracy': '#FFD700',
    'Hybrid Regime': '#FF8C00',
    'Authoritarian': '#DC143C'
}

# 메인 앱
def main():
    st.title("🗳️ 민주주의 지수 지리적 분석")
    st.markdown("---")
    
    # 데이터 로드
    df = load_data()
    
    # 사이드바
    st.sidebar.header("🔧 설정")
    
    # 페이지 선택
    page = st.sidebar.selectbox(
        "분석 페이지 선택",
        ["📊 대시보드", "🗺️ 지도 시각화", "📈 통계 분석", "🔍 국가 검색", "📋 데이터 보기"]
    )
    
    if page == "📊 대시보드":
        show_dashboard(df)
    elif page == "🗺️ 지도 시각화":
        show_map_visualization(df)
    elif page == "📈 통계 분석":
        show_statistics(df)
    elif page == "🔍 국가 검색":
        show_country_search(df)
    elif page == "📋 데이터 보기":
        show_data_view(df)

def show_dashboard(df):
    st.header("📊 민주주의 지수 대시보드")
    
    # 주요 지표
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 분석 국가 수", len(df))
    
    with col2:
        st.metric("평균 민주주의 지수", f"{df['democracy_index'].mean():.2f}")
    
    with col3:
        st.metric("최고 지수", f"{df['democracy_index'].max():.2f}")
    
    with col4:
        st.metric("최저 지수", f"{df['democracy_index'].min():.2f}")
    
    # 민주주의 유형별 분포
    st.subheader("민주주의 유형별 분포")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 파이 차트
        type_counts = df['democracy_type'].value_counts()
        fig_pie = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            title="민주주의 유형별 국가 수",
            color_discrete_map=color_map
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # 바 차트
        fig_bar = px.bar(
            x=type_counts.index,
            y=type_counts.values,
            title="민주주의 유형별 국가 수",
            color=type_counts.index,
            color_discrete_map=color_map
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # 상위/하위 국가
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 상위 10개국")
        top_10 = df.nlargest(10, 'democracy_index')[['country', 'democracy_index', 'democracy_type']]
        st.dataframe(top_10, use_container_width=True)
    
    with col2:
        st.subheader("⚠️ 하위 10개국")
        bottom_10 = df.nsmallest(10, 'democracy_index')[['country', 'democracy_index', 'democracy_type']]
        st.dataframe(bottom_10, use_container_width=True)

def show_map_visualization(df):
    st.header("🗺️ 지도 시각화")
    
    # 지도 타입 선택
    map_type = st.selectbox(
        "지도 타입 선택",
        ["🌍 산점도 지도", "🗺️ 코로플레스 지도", "🔥 히트맵", "🌐 3D 지구본"]
    )
    
    if map_type == "🌍 산점도 지도":
        # 기본 산점도 지도
        fig = px.scatter_geo(
            df,
            lat='latitude',
            lon='longitude',
            hover_name='country',
            hover_data=['democracy_index', 'democracy_type'],
            color='democracy_type',
            color_discrete_map=color_map,
            size='democracy_index',
            size_max=25,
            title="세계 민주주의 지수 분포 (산점도)"
        )
        
        # 지도 스타일 설정
        fig.update_geos(
            projection_type="natural earth",
            showland=True,
            landcolor="rgb(243, 243, 243)",
            coastlinecolor="rgb(204, 204, 204)",
            showocean=True,
            oceancolor="rgb(230, 245, 255)",
            showlakes=True,
            lakecolor="rgb(230, 245, 255)",
            showrivers=True,
            rivercolor="rgb(230, 245, 255)"
        )
        
        fig.update_layout(height=700)
        st.plotly_chart(fig, use_container_width=True)
    
    elif map_type == "🗺️ 코로플레스 지도":
        # 국가 코드 추가 (간단한 예시)
        country_codes = {
            'Norway': 'NOR', 'Iceland': 'ISL', 'Sweden': 'SWE', 'New Zealand': 'NZL',
            'Finland': 'FIN', 'Denmark': 'DNK', 'Ireland': 'IRL', 'Taiwan': 'TWN',
            'Australia': 'AUS', 'Switzerland': 'CHE', 'Netherlands': 'NLD',
            'Canada': 'CAN', 'Uruguay': 'URY', 'United Kingdom': 'GBR',
            'Luxembourg': 'LUX', 'Germany': 'DEU', 'South Korea': 'KOR',
            'Japan': 'JPN', 'United States': 'USA', 'France': 'FRA',
            'Israel': 'ISR', 'Italy': 'ITA', 'Spain': 'ESP', 'Botswana': 'BWA',
            'South Africa': 'ZAF', 'India': 'IND', 'Brazil': 'BRA',
            'Poland': 'POL', 'Hungary': 'HUN', 'Turkey': 'TUR',
            'Russia': 'RUS', 'China': 'CHN', 'Iran': 'IRN',
            'North Korea': 'PRK', 'Saudi Arabia': 'SAU'
        }
        
        df_choropleth = df.copy()
        df_choropleth['iso_alpha'] = df_choropleth['country'].map(country_codes)
        
        fig = px.choropleth(
            df_choropleth,
            locations='iso_alpha',
            color='democracy_index',
            hover_name='country',
            hover_data=['democracy_type'],
            color_continuous_scale='RdYlGn',
            title="민주주의 지수 코로플레스 지도"
        )
        
        fig.update_layout(height=700)
        st.plotly_chart(fig, use_container_width=True)
    
    elif map_type == "🔥 히트맵":
        # 밀도 히트맵
        fig = px.density_mapbox(
            df,
            lat='latitude',
            lon='longitude',
            z='democracy_index',
            radius=20,
            center=dict(lat=20, lon=0),
            zoom=1,
            mapbox_style="open-street-map",
            title="민주주의 지수 밀도 히트맵"
        )
        
        fig.update_layout(height=700)
        st.plotly_chart(fig, use_container_width=True)
    
    elif map_type == "🌐 3D 지구본":
        # 3D 지구본 시각화
        fig = px.scatter_geo(
            df,
            lat='latitude',
            lon='longitude',
            hover_name='country',
            hover_data=['democracy_index', 'democracy_type'],
            color='democracy_index',
            size='democracy_index',
            size_max=20,
            color_continuous_scale='RdYlGn',
            title="3D 지구본 - 민주주의 지수"
        )
        
        fig.update_geos(
            projection_type="orthographic",
            showland=True,
            landcolor="rgb(243, 243, 243)",
            coastlinecolor="rgb(204, 204, 204)",
            showocean=True,
            oceancolor="rgb(0, 100, 200)",
        )
        
        fig.update_layout(height=700)
        st.plotly_chart(fig, use_container_width=True)
    
    # 지도 설정 옵션
    st.subheader("🎛️ 지도 설정")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        projection = st.selectbox(
            "지도 투영법",
            ["natural earth", "orthographic", "mercator", "equirectangular", "robinson"]
        )
    
    with col2:
        show_country_labels = st.checkbox("국가명 표시", value=True)
    
    with col3:
        animation_speed = st.slider("애니메이션 속도", 0.1, 2.0, 1.0)
    
    # 상세 지도 (선택된 설정 적용)
    if map_type == "🌍 산점도 지도":
        fig_detailed = px.scatter_geo(
            df,
            lat='latitude',
            lon='longitude',
            hover_name='country',
            hover_data=['democracy_index', 'democracy_type', 'region'],
            color='democracy_type',
            color_discrete_map=color_map,
            size='democracy_index',
            size_max=30,
            title=f"상세 지도 - {projection} 투영법",
            animation_frame=None
        )
        
        # 국가명 라벨 추가
        if show_country_labels:
            for _, row in df.iterrows():
                fig_detailed.add_trace(
                    go.Scattergeo(
                        lon=[row['longitude']],
                        lat=[row['latitude']],
                        text=[row['country']],
                        mode='text',
                        textfont=dict(size=8, color='black'),
                        showlegend=False,
                        hoverinfo='skip'
                    )
                )
        
        fig_detailed.update_geos(
            projection_type=projection,
            showland=True,
            landcolor="rgb(243, 243, 243)",
            coastlinecolor="rgb(204, 204, 204)",
            showocean=True,
            oceancolor="rgb(230, 245, 255)",
            showlakes=True,
            lakecolor="rgb(230, 245, 255)",
            showrivers=True,
            rivercolor="rgb(230, 245, 255)",
            showframe=False,
            showcoastlines=True
        )
        
        fig_detailed.update_layout(height=700)
        st.plotly_chart(fig_detailed, use_container_width=True)
    
    # 대륙별 분석
    st.subheader("🌏 대륙별 분석")
    
    # 대륙별 분류 (위도/경도 기반)
    def classify_continent(row):
        lat, lon = row['latitude'], row['longitude']
        if -60 <= lat <= 70 and -170 <= lon <= -30:
            return "Americas"
        elif -40 <= lat <= 80 and -30 <= lon <= 70:
            return "Europe/Africa"
        elif -50 <= lat <= 80 and 70 <= lon <= 180:
            return "Asia/Oceania"
        else:
            return "Other"
    
    df['continent'] = df.apply(classify_continent, axis=1)
    
    # 대륙별 통계
    continent_stats = df.groupby('continent').agg({
        'democracy_index': ['mean', 'count', 'std'],
        'democracy_type': lambda x: x.mode()[0] if not x.empty else 'None'
    }).round(2)
    
    continent_stats.columns = ['평균 지수', '국가 수', '표준편차', '주요 유형']
    st.dataframe(continent_stats, use_container_width=True)
    
    # 대륙별 바 차트
    continent_avg = df.groupby('continent')['democracy_index'].mean().sort_values(ascending=False)
    
    fig_continent = px.bar(
        x=continent_avg.index,
        y=continent_avg.values,
        title="대륙별 평균 민주주의 지수",
        color=continent_avg.values,
        color_continuous_scale='RdYlGn'
    )
    
    fig_continent.update_layout(
        xaxis_title="대륙",
        yaxis_title="평균 민주주의 지수",
        showlegend=False
    )
    
    st.plotly_chart(fig_continent, use_container_width=True)

def show_statistics(df):
    st.header("📈 통계 분석")
    
    # 히스토그램
    st.subheader("민주주의 지수 분포")
    
    fig_hist = px.histogram(
        df,
        x='democracy_index',
        color='democracy_type',
        color_discrete_map=color_map,
        title="민주주의 지수 분포",
        nbins=20
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # 지역별 분석
    st.subheader("지역별 민주주의 지수")
    
    regional_stats = df.groupby('region').agg({
        'democracy_index': ['mean', 'std', 'count']
    }).round(2)
    
    regional_stats.columns = ['평균', '표준편차', '국가 수']
    st.dataframe(regional_stats, use_container_width=True)
    
    # 박스 플롯
    fig_box = px.box(
        df,
        x='democracy_type',
        y='democracy_index',
        color='democracy_type',
        color_discrete_map=color_map,
        title="민주주의 유형별 지수 분포"
    )
    st.plotly_chart(fig_box, use_container_width=True)
    
    # 상관관계 분석
    st.subheader("위도와 민주주의 지수의 관계")
    
    fig_scatter = px.scatter(
        df,
        x='latitude',
        y='democracy_index',
        color='democracy_type',
        color_discrete_map=color_map,
        hover_name='country',
        title="위도 vs 민주주의 지수",
        trendline="ols"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # 상관계수 계산
    correlation = df['latitude'].corr(df['democracy_index'])
    st.metric("위도-민주주의 지수 상관계수", f"{correlation:.3f}")

def show_country_search(df):
    st.header("🔍 국가 검색")
    
    # 검색 옵션
    search_option = st.radio(
        "검색 방법 선택",
        ["국가명으로 검색", "민주주의 지수 범위로 검색", "지역별 검색"]
    )
    
    if search_option == "국가명으로 검색":
        country_name = st.text_input("국가명 입력 (영어)")
        
        if country_name:
            results = df[df['country'].str.contains(country_name, case=False, na=False)]
            
            if not results.empty:
                for _, row in results.iterrows():
                    with st.expander(f"🏛️ {row['country']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("민주주의 지수", f"{row['democracy_index']}")
                            st.metric("민주주의 유형", row['democracy_type'])
                        
                        with col2:
                            st.metric("위도", f"{row['latitude']}")
                            st.metric("경도", f"{row['longitude']}")
                            st.metric("지역", row['region'])
            else:
                st.warning(f"'{country_name}'과 일치하는 국가를 찾을 수 없습니다.")
    
    elif search_option == "민주주의 지수 범위로 검색":
        min_val, max_val = st.slider(
            "민주주의 지수 범위 선택",
            min_value=float(df['democracy_index'].min()),
            max_value=float(df['democracy_index'].max()),
            value=(5.0, 8.0)
        )
        
        results = df[(df['democracy_index'] >= min_val) & (df['democracy_index'] <= max_val)]
        
        st.write(f"검색 결과: {len(results)}개 국가")
        st.dataframe(results[['country', 'democracy_index', 'democracy_type']], use_container_width=True)
    
    elif search_option == "지역별 검색":
        selected_region = st.selectbox("지역 선택", df['region'].unique())
        
        results = df[df['region'] == selected_region]
        
        st.write(f"'{selected_region}' 지역의 국가들:")
        st.dataframe(results[['country', 'democracy_index', 'democracy_type']], use_container_width=True)

def show_data_view(df):
    st.header("📋 데이터 보기")
    
    # 데이터 표시 옵션
    col1, col2 = st.columns(2)
    
    with col1:
        show_all = st.checkbox("모든 데이터 표시", value=True)
    
    with col2:
        if not show_all:
            num_rows = st.number_input("표시할 행 수", min_value=1, max_value=len(df), value=10)
        else:
            num_rows = len(df)
    
    # 정렬 옵션
    sort_column = st.selectbox(
        "정렬 기준 선택",
        ['country', 'democracy_index', 'democracy_type', 'latitude', 'longitude']
    )
    
    sort_order = st.radio("정렬 순서", ["오름차순", "내림차순"])
    
    # 데이터 정렬
    sorted_df = df.sort_values(
        by=sort_column,
        ascending=(sort_order == "오름차순")
    ).head(num_rows)
    
    # 데이터 표시
    st.dataframe(sorted_df, use_container_width=True)
    
    # 다운로드 버튼
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 CSV 다운로드",
            data=csv,
            file_name='democracy_data.csv',
            mime='text/csv'
        )
    
    with col2:
        json_data = df.to_json(orient='records', indent=2)
        st.download_button(
            label="📥 JSON 다운로드",
            data=json_data,
            file_name='democracy_data.json',
            mime='application/json'
        )

if __name__ == "__main__":
    main()
