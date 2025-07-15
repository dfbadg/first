import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import requests
import json

# 주요 국가들의 민주주의 지수 데이터 (2023년 기준 예시)
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

# 데이터프레임 생성
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

# 색상 매핑
color_map = {
    'Full Democracy': '#2E8B57',      # 진한 녹색
    'Flawed Democracy': '#FFD700',    # 노란색
    'Hybrid Regime': '#FF8C00',       # 주황색
    'Authoritarian': '#DC143C'        # 빨간색
}

# 지도 시각화 함수
def create_democracy_map():
    fig, ax = plt.subplots(figsize=(15, 10))
    
    # 세계 지도 배경 (간단한 사각형으로 표현)
    ax.add_patch(Rectangle((-180, -90), 360, 180, 
                          facecolor='lightblue', alpha=0.3))
    
    # 각 국가별 점 표시
    for democracy_type in df['democracy_type'].unique():
        subset = df[df['democracy_type'] == democracy_type]
        ax.scatter(subset['longitude'], subset['latitude'], 
                  c=color_map[democracy_type], 
                  s=100, alpha=0.7, 
                  label=democracy_type, 
                  edgecolors='black', linewidth=0.5)
    
    # 지도 설정
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.set_xlabel('Longitude', fontsize=12)
    ax.set_ylabel('Latitude', fontsize=12)
    ax.set_title('Democracy Index by Geographic Location (2023)', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1))
    
    # 일부 주요 국가 라벨 추가
    important_countries = ['United States', 'China', 'Russia', 'South Korea', 'Norway']
    for country in important_countries:
        if country in df['country'].values:
            row = df[df['country'] == country].iloc[0]
            ax.annotate(country, 
                       (row['longitude'], row['latitude']), 
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=8, ha='left')
    
    plt.tight_layout()
    return fig

# 민주주의 지수 분포 히스토그램
def create_democracy_histogram():
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 각 타입별로 히스토그램 생성
    for democracy_type in df['democracy_type'].unique():
        subset = df[df['democracy_type'] == democracy_type]
        ax.hist(subset['democracy_index'], 
               bins=20, alpha=0.7, 
               label=democracy_type, 
               color=color_map[democracy_type])
    
    ax.set_xlabel('Democracy Index Score', fontsize=12)
    ax.set_ylabel('Number of Countries', fontsize=12)
    ax.set_title('Distribution of Democracy Index Scores', fontsize=16, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

# 지역별 민주주의 분석
def analyze_by_region():
    # 위도를 기준으로 대략적인 지역 분류
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
    
    # 지역별 평균 민주주의 지수
    regional_avg = df.groupby('region')['democracy_index'].agg(['mean', 'count', 'std']).round(2)
    
    print("지역별 민주주의 지수 분석:")
    print("=" * 60)
    for region, data in regional_avg.iterrows():
        print(f"{region}:")
        print(f"  평균 민주주의 지수: {data['mean']}")
        print(f"  국가 수: {data['count']}")
        print(f"  표준편차: {data['std']}")
        print()

# 데이터 내보내기 함수
def export_data():
    # CSV 파일로 저장
    df.to_csv('democracy_geo_data.csv', index=False, encoding='utf-8')
    print("데이터가 'democracy_geo_data.csv' 파일로 저장되었습니다.")
    
    # JSON 형태로도 저장
    df.to_json('democracy_geo_data.json', orient='records', indent=2)
    print("데이터가 'democracy_geo_data.json' 파일로도 저장되었습니다.")

# 특정 국가 정보 검색 함수
def search_country(country_name):
    result = df[df['country'].str.contains(country_name, case=False, na=False)]
    if not result.empty:
        for _, row in result.iterrows():
            print(f"\n국가: {row['country']}")
            print(f"민주주의 지수: {row['democracy_index']}")
            print(f"민주주의 유형: {row['democracy_type']}")
            print(f"위도: {row['latitude']}")
            print(f"경도: {row['longitude']}")
    else:
        print(f"'{country_name}'과 일치하는 국가를 찾을 수 없습니다.")

# 메인 실행 함수
def main():
    print("민주주의 지수 지리적 분석 시스템")
    print("=" * 50)
    
    # 기본 통계 출력
    print(f"총 분석 국가 수: {len(df)}")
    print(f"평균 민주주의 지수: {df['democracy_index'].mean():.2f}")
    print(f"민주주의 지수 범위: {df['democracy_index'].min():.2f} - {df['democracy_index'].max():.2f}")
    print()
    
    # 민주주의 유형별 분포
    print("민주주의 유형별 분포:")
    type_counts = df['democracy_type'].value_counts()
    for democracy_type, count in type_counts.items():
        print(f"  {democracy_type}: {count}개국")
    print()
    
    # 지역별 분석
    analyze_by_region()
    
    # 시각화 생성
    print("시각화 생성 중...")
    map_fig = create_democracy_map()
    hist_fig = create_democracy_histogram()
    
    # 그래프 표시
    plt.show()
    
    # 데이터 내보내기
    export_data()
    
    # 상위/하위 5개국 출력
    print("\n민주주의 지수 상위 5개국:")
    top_5 = df.nlargest(5, 'democracy_index')[['country', 'democracy_index', 'democracy_type']]
    print(top_5.to_string(index=False))
    
    print("\n민주주의 지수 하위 5개국:")
    bottom_5 = df.nsmallest(5, 'democracy_index')[['country', 'democracy_index', 'democracy_type']]
    print(bottom_5.to_string(index=False))

# 실행
if __name__ == "__main__":
    main()
    
    # 예시: 특정 국가 검색
    print("\n" + "="*50)
    print("국가별 검색 예시:")
    search_country("Korea")
    search_country("United States")
    search_country("China")
