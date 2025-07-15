@st.cache_data
def load_data():
    democracy_data = {
        'country': [
            'Norway', 'Sweden', 'New Zealand', 'United States', 'India'
        ],
        'democracy_index': [
            9.81, 9.26, 9.25, 7.85, 7.04
        ],
        'latitude': [
            60.472, 60.128, -40.900, 37.090, 20.593
        ],
        'longitude': [
            8.468, 18.643, 174.885, -95.712, 78.962
        ]
    }

    df = pd.DataFrame(democracy_data)

    # ✅ 민주주의 유형 분류 함수 정의
    def classify_democracy(score):
        if score >= 8.0:
            return 'Full Democracy'
        elif score >= 6.0:
            return 'Flawed Democracy'
        elif score >= 4.0:
            return 'Hybrid Regime'
        else:
            return 'Authoritarian'

    # ✅ 적용
    df['democracy_type'] = df['democracy_index'].apply(classify_democracy)

    # ✅ 지역 분류
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
