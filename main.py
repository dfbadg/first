import streamlit as st

# MBTI별 추천 직업 데이터
mbti_jobs = {
    "INTJ": ["전략 기획자", "소프트웨어 엔지니어", "데이터 과학자"],
    "INTP": ["연구원", "이론 물리학자", "UX 디자이너"],
    "ENTJ": ["경영 컨설턴트", "프로젝트 매니저", "변호사"],
    "ENTP": ["창업가", "광고 기획자", "기술 혁신 전문가"],
    "INFJ": ["심리상담사", "작가", "교육 컨설턴트"],
    "INFP": ["예술가", "카피라이터", "사회복지사"],
    "ENFJ": ["교육자", "HR 전문가", "정치가"],
    "ENFP": ["마케터", "기획자", "공익 활동가"],
    "ISTJ": ["회계사", "공무원", "재무 분석가"],
    "ISFJ": ["간호사", "교사", "행정직"],
    "ESTJ": ["운영 관리자", "군인", "현장 감독관"],
    "ESFJ": ["이벤트 플래너", "의료 서비스 매니저", "영업 관리자"],
    "ISTP": ["기계 엔지니어", "응급 구조사", "파일럿"],
    "ISFP": ["그래픽 디자이너", "사진작가", "플로리스트"],
    "ESTP": ["세일즈맨", "스포츠 코치", "기업가"],
    "ESFP": ["MC/연예인", "패션 디자이너", "홍보 담당자"],
}

# 웹앱 제목
st.title("💼 MBTI 직업 추천기")

# 사용자 입력 (MBTI 선택)
selected_mbti = st.selectbox("당신의 MBTI를 선택하세요:", list(mbti_jobs.keys()))

# 추천 직업 보여주기
if selected_mbti:
    st.subheader(f"🔍 {selected_mbti} 유형에게 추천하는 직업 3가지:")
    for job in mbti_jobs[selected_mbti]:
        st.write(f"👉 {job}")
