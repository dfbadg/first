import streamlit as st

# MBTI별 어울리는 포켓몬 추천
mbti_pokemon = {
    "INTJ": ["뮤츠", "메타몽", "루기아"],
    "INTP": ["프테라", "야도킹", "로토무"],
    "ENTJ": ["리자몽", "헬가", "보만다"],
    "ENTP": ["에몽가", "라이츄", "드래펄트"],
    "INFJ": ["세레비", "아르세우스", "브리무음"],
    "INFP": ["이브이", "피카츄", "치코리타"],
    "ENFJ": ["루카리오", "니드퀸", "요가램"],
    "ENFP": ["피츄", "토게키스", "마릴리"],
    "ISTJ": ["코일", "갸라도스", "딱구리"],
    "ISFJ": ["해피너스", "라프라스", "에브이"],
    "ESTJ": ["강챙이", "괴력몬", "철화구야"],
    "ESFJ": ["푸린", "파치리스", "분떠도리"],
    "ISTP": ["펄기아", "크로뱃", "너트령"],
    "ISFP": ["부스터", "델빌", "치코리타"],
    "ESTP": ["전룡", "핫삼", "번치코"],
    "ESFP": ["피카츄", "쁘사이저", "님피아"],
}

# 웹앱 제목
st.title("🔮 MBTI x 포켓몬 추천기")

# 사용자 입력
selected_mbti = st.selectbox("당신의 MBTI를 선택하세요:", list(mbti_pokemon.keys()))

# 추천 결과 출력
if selected_mbti:
    st.subheader(f"🎴 {selected_mbti} 유형에게 어울리는 포켓몬 3마리:")
    for pokemon in mbti_pokemon[selected_mbti]:
        st.write(f"👉 {pokemon}")
