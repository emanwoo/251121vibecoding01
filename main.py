import streamlit as st

# 1. 페이지 기본 설정 (탭 제목, 아이콘, 레이아웃)
st.set_page_config(
    page_title="학생 진로 나침반",
    page_icon="🧭",
    layout="centered"
)

# 2. MBTI 데이터베이스 (딕셔너리 활용 - 별도 DB 없이 구현)
mbti_data = {
    "ISTJ": {
        "alias": "청렴결백한 논리주의자",
        "desc": "책임감이 강하고 현실적이며 매사에 철저한 당신!",
        "careers": ["🏛️ 공무원/행정가", "📊 회계사", "💻 시스템 관리자"],
        "color": "blue"
    },
    "ISFJ": {
        "alias": "용감한 수호자",
        "desc": "차분하고 헌신적이며 성실하게 주변을 챙기는 당신!",
        "careers": ["🏥 간호사/의료계열", "🏫 초등교사", "📚 사서"],
        "color": "blue"
    },
    "INFJ": {
        "alias": "통찰력 있는 선지자",
        "desc": "사람에 대한 깊은 통찰력과 확고한 신념을 가진 당신!",
        "careers": ["🧠 심리 상담가", "✍️ 작가/시나리오 작가", "🎨 예술 치료사"],
        "color": "green"
    },
    "INTJ": {
        "alias": "용의주도한 전략가",
        "desc": "상상력이 풍부하며 철두철미한 계획을 세우는 당신!",
        "careers": ["🔬 과학자/연구원", "⚖️ 변호사/판사", "📈 전략 기획자"],
        "color": "purple"
    },
    "ISTP": {
        "alias": "만능 재주꾼",
        "desc": "대담하고 현실적이며 도구 사용에 능숙한 당신!",
        "careers": ["👮 경찰/소방관", "✈️ 파일럿/항공", "🛠️ 엔지니어"],
        "color": "yellow"
    },
    "ISFP": {
        "alias": "호기심 많은 예술가",
        "desc": "항상 새로운 것을 찾아 시도하는 융통성 있는 당신!",
        "careers": ["👗 패션 디자이너", "🍳 셰프/요리사", "📷 사진작가"],
        "color": "yellow"
    },
    "INFP": {
        "alias": "열정적인 중재자",
        "desc": "상냥한 성격과 이타주의적인 마음을 가진 낭만적인 당신!",
        "careers": ["📢 사회복지사", "📝 편집자/에디터", "🎨 그래픽 디자이너"],
        "color": "green"
    },
    "INTP": {
        "alias": "논리적인 사색가",
        "desc": "끊임없이 새로운 지식에 목말라하는 혁신적인 당신!",
        "careers": ["💻 프로그래머", "🧪 물리학자", "💸 금융 분석가"],
        "color": "purple"
    },
    "ESTP": {
        "alias": "모험을 즐기는 사업가",
        "desc": "직관적이고 에너지가 넘치며 스릴을 즐기는 당신!",
        "careers": ["🕵️ 탐정/조사관", "🏗️ 건축 현장 관리", "💹 펀드 매니저"],
        "color": "yellow"
    },
    "ESFP": {
        "alias": "자유로운 영혼의 연예인",
        "desc": "주위에 있으면 인생이 지루할 틈이 없는 즉흥적인 당신!",
        "careers": ["🎤 연예인/엔터테이너", "✈️ 승무원", "🎉 이벤트 플래너"],
        "color": "yellow"
    },
    "ENFP": {
        "alias": "재기발랄한 활동가",
        "desc": "창의적이며 항상 웃을 거리를 찾아내는 긍정적인 당신!",
        "careers": ["📺 PD/크리에이터", "📣 홍보/마케터", "🗣️ 전문 강사"],
        "color": "green"
    },
    "ENTP": {
        "alias": "뜨거운 논쟁을 즐기는 변론가",
        "desc": "지적인 도전을 두려워하지 않는 똑똑한 호기심 대장인 당신!",
        "careers": ["💡 창업가/CEO", "🎤 정치인", "🎬 영화 감독"],
        "color": "purple"
    },
    "ESTJ": {
        "alias": "엄격한 관리자",
        "desc": "사물과 사람을 관리하는 데 타의 추종을 불허하는 당신!",
        "careers": ["🏢 경영 컨설턴트", "💊 약사", "👮 군 장교/지휘관"],
        "color": "blue"
    },
    "ESFJ": {
        "alias": "사교적인 외교관",
        "desc": "타인을 향한 세심한 관심과 사교적인 성향을 가진 당신!",
        "careers": ["🏫 학교 행정가", "🏨 호텔리어", "🩺 물리치료사"],
        "color": "blue"
    },
    "ENFJ": {
        "alias": "정의로운 사회운동가",
        "desc": "청중을 사로잡고 이끄는 카리스마 넘치는 당신!",
        "careers": ["🎤 아나운서/리포터", "👥 인사(HR) 담당자", "🎓 교육 컨설턴트"],
        "color": "green"
    },
    "ENTJ": {
        "alias": "대담한 통솔자",
        "desc": "대담하고 상상력이 풍부하며 강한 의지를 가진 당신!",
        "careers": ["🏛️ 변호사", "👔 경영인/임원", "🏗️ 도시 계획가"],
        "color": "purple"
    }
}

# 3. UI 구성

# 헤더 섹션
st.title("🧭 학생 진로 나침반")
st.markdown("### 당신의 **MBTI**를 선택하면 미래의 직업을 추천해 드려요! ✨")
st.markdown("---")

# 사이드바 구성 (옵션 선택)
with st.sidebar:
    st.header("🔎 설정")
    selected_mbti = st.selectbox(
        "본인의 MBTI 유형을 선택하세요:",
        list(mbti_data.keys()),
        index=None,
        placeholder="MBTI 선택..."
    )
    st.write("---")
    st.write("Developed with ❤️ using Streamlit")

# 메인 콘텐츠 영역
if selected_mbti:
    # 선택된 데이터 가져오기
    data = mbti_data[selected_mbti]
    
    # 결과 화면 애니메이션 효과 (스피너)
    with st.spinner(f"{selected_mbti} 유형을 분석 중입니다... 🔮"):
        # 약간의 딜레이 효과를 주어 분석하는 느낌 (실제 연산은 없음)
        import time
        time.sleep(0.8)
    
    # 1. 유형 소개
    st.header(f"당신은 **[{selected_mbti}]** 유형이군요!")
    st.subheader(f"✨ {data['alias']}")
    st.info(data['desc'], icon="ℹ️")
    
    st.markdown("### 🚀 추천 진로 Top 3")
    
    # 2. 진로 카드 배치 (3열 구성)
    col1, col2, col3 = st.columns(3)
    
    # 카드 스타일링을 위한 헬퍼 함수 대신 기본 컨테이너 활용
    with col1:
        st.container(border=True).markdown(f"#### 1순위\n\n### {data['careers'][0]}")
        
    with col2:
        st.container(border=True).markdown(f"#### 2순위\n\n### {data['careers'][1]}")
        
    with col3:
        st.container(border=True).markdown(f"#### 3순위\n\n### {data['careers'][2]}")

    # 마무리 멘트
    st.markdown("---")
    st.success("💡 이 결과는 재미로 보는 참고용입니다. 당신의 가능성은 무한합니다! 🌈")

else:
    # 선택 전 초기 화면
    st.image("https://cdn.pixabay.com/photo/2017/01/26/09/46/compass-2010549_1280.jpg", caption="당신의 꿈을 향해 나아가세요!", use_column_width=True)
    st.info("👈 왼쪽 사이드바에서 당신의 **MBTI**를 선택해주세요!")
