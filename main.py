import streamlit as st

# ----- 기본 세팅 -----
st.set_page_config(
    page_title="MBTI 진로 상담실",
    page_icon="🎓",
    layout="centered"
)

# ----- 간단한 스타일 커스터마이징 (기본 기능만 사용) -----
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        text-align: center;
        color: #666666;
        margin-bottom: 1.5rem;
    }
    .result-card {
        border-radius: 16px;
        padding: 1.1rem 1.2rem;
        margin-top: 0.8rem;
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid #eeeeee;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.08);
    }
    .result-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .pill {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 999px;
        font-size: 0.78rem;
        margin-right: 0.25rem;
        margin-top: 0.2rem;
        background: #f3f4ff;
        color: #4f46e5;
        border: 1px solid #e0e7ff;
    }
    .footer {
        text-align: center;
        font-size: 0.8rem;
        color: #9ca3af;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----- 데이터 정의: MBTI별 추천 진로 -----
mbti_career_map = {
    "INTJ": {
        "label": "전략가 🧠",
        "keywords": ["분석적", "장기 계획", "독립적"],
        "careers": [
            ("연구원", "새로운 이론과 지식을 설계하고 검증하는 역할"),
            ("데이터 분석가", "숫자 속에서 패턴을 찾아 전략을 제안하는 직무"),
            ("전략 컨설턴트", "기업의 장기 로드맵을 설계하고 문제를 구조화하는 역할")
        ]
    },
    "INTP": {
        "label": "사색가 🧩",
        "keywords": ["논리적", "아이디어", "탐구심"],
        "careers": [
            ("소프트웨어 개발자", "문제를 구조화하고 알고리즘으로 해결하는 일"),
            ("UX 리서처", "사용자 행동을 분석해 더 나은 경험을 설계"),
            ("학술 연구자", "관심 분야를 깊게 파고드는 연구 중심 직무")
        ]
    },
    "ENTJ": {
        "label": "지휘관 🏁",
        "keywords": ["리더십", "목표 지향", "결단력"],
        "careers": [
            ("프로덕트 매니저", "팀을 이끌어 제품의 방향을 결정하는 역할"),
            ("경영 컨설턴트", "조직 구조와 전략을 진단하고 개선"),
            ("사업가(창업자)", "아이디어를 바탕으로 비즈니스를 만들어 가는 직무")
        ]
    },
    "ENTP": {
        "label": "발명가 🚀",
        "keywords": ["창의적", "도전", "토론"],
        "careers": [
            ("스타트업 기획자", "새로운 서비스와 비즈니스 모델을 기획"),
            ("마케팅 전략가", "트렌드를 읽고 새로운 캠페인을 설계"),
            ("콘텐츠 크리에이터", "자신만의 관점으로 콘텐츠를 기획·제작")
        ]
    },
    "INFJ": {
        "label": "옹호자 🕊️",
        "keywords": ["가치지향", "공감", "비전"],
        "careers": [
            ("교사·교육자", "학생의 성장을 돕고 학습 경험을 설계"),
            ("상담사", "개인의 고민을 듣고 심리적 성장을 지원"),
            ("사회 정책 기획자", "더 나은 사회 시스템을 설계하는 역할")
        ]
    },
    "INFP": {
        "label": "중재자 🌿",
        "keywords": ["이상주의", "창작", "공감"],
        "careers": [
            ("작가·에디터", "이야기와 글로 메시지를 전하는 직무"),
            ("브랜드 스토리텔러", "브랜드에 스토리를 입히는 역할"),
            ("예술·문화 기획자", "공연·전시 등 문화 콘텐츠를 기획")
        ]
    },
    "ENFJ": {
        "label": "선도자 🌈",
        "keywords": ["리더십", "소통", "조정"],
        "careers": [
            ("HRD 전문가", "교육·코칭을 통해 구성원의 성장을 지원"),
            ("프로젝트 매니저", "여러 사람을 조율해 목표를 달성"),
            ("학교·교육 행정가", "교육 현장을 시스템으로 관리·운영")
        ]
    },
    "ENFP": {
        "label": "활동가 🔥",
        "keywords": ["열정", "아이디어", "사람 중심"],
        "careers": [
            ("광고·브랜드 마케터", "감성과 스토리로 브랜드를 알리는 역할"),
            ("행사·이벤트 플래너", "사람이 모이는 장을 기획하는 직무"),
            ("사회혁신 활동가", "사회 문제를 창의적으로 해결하는 일")
        ]
    },
    "ISTJ": {
        "label": "현실주의자 📊",
        "keywords": ["성실", "정확성", "책임감"],
        "careers": [
            ("공무원", "정책과 행정을 안정적으로 운영"),
            ("회계사·재무 담당자", "숫자와 규정을 엄밀하게 다루는 직무"),
            ("품질 관리 전문가", "제품·서비스의 기준을 관리하고 점검")
        ]
    },
    "ISFJ": {
        "label": "수호자 🛡️",
        "keywords": ["헌신", "배려", "안정"],
        "careers": [
            ("간호사·보건 전문가", "사람의 건강을 세심하게 돌보는 역할"),
            ("학교 행정·교육 지원", "현장을 안정적으로 뒷받침하는 직무"),
            ("사회복지사", "취약 계층을 지원하고 생활을 돕는 일")
        ]
    },
    "ESTJ": {
        "label": "관리자 🧱",
        "keywords": ["조직력", "실행력", "관리"],
        "careers": [
            ("현장 관리·생산관리", "프로세스를 계획하고 실행을 관리"),
            ("팀 리더·매니저", "사람과 업무를 동시에 관리하는 역할"),
            ("인사·노무 담당자", "조직의 규정과 사람을 함께 다루는 직무")
        ]
    },
    "ESFJ": {
        "label": "사교적 조정자 🤝",
        "keywords": ["배려", "협력", "서비스"],
        "careers": [
            ("교사·학급담임", "학생과의 관계를 중심으로 교육하는 직무"),
            ("서비스 기획·CS 매니저", "고객 경험을 설계·관리하는 역할"),
            ("병원 코디네이터", "의료진과 환자 사이를 조율하는 직무")
        ]
    },
    "ISTP": {
        "label": "장인 🛠️",
        "keywords": ["실용적", "문제 해결", "손재주"],
        "careers": [
            ("엔지니어·기술직", "기계·시스템을 직접 다루고 개선"),
            ("UX 엔지니어", "제품을 실제 사용자 관점에서 다듬는 역할"),
            ("안전·설비 관리자", "현장의 문제를 즉각적으로 해결하는 직무")
        ]
    },
    "ISFP": {
        "label": "예술가 🎨",
        "keywords": ["감성", "미적 감각", "자유로움"],
        "careers": [
            ("디자이너(그래픽·패션 등)", "시각적인 아름다움을 설계"),
            ("포토그래퍼·영상 편집자", "이미지와 영상으로 감정을 기록"),
            ("공예·핸드메이드 아티스트", "손으로 만드는 작품 활동")
        ]
    },
    "ESTP": {
        "label": "도전자 ⚡",
        "keywords": ["즉흥적", "실전형", "에너지"],
        "careers": [
            ("영업·세일즈 전문가", "사람을 만나 설득하고 성과를 만드는 직무"),
            ("스포츠·피트니스 코치", "현장에서 몸으로 가르치는 역할"),
            ("이벤트·공연 운영자", "빠르게 상황을 파악하고 대처하는 직무")
        ]
    },
    "ESFP": {
        "label": "엔터테이너 🎉",
        "keywords": ["사교적", "분위기 메이커", "현장 중심"],
        "careers": [
            ("방송·MC·크리에이터", "무대와 화면에서 사람들과 소통"),
            ("공연·축제 기획자", "즐거운 순간을 연출하는 직무"),
            ("홍보·PR 담당자", "브랜드와 사람을 연결하는 역할")
        ]
    },
}

mbti_types = list(mbti_career_map.keys())

# ----- 레이아웃 -----
with st.sidebar:
    st.markdown("### 🎯 사용 방법")
    st.markdown(
        """
        1. **MBTI 유형**을 선택해 주세요.  
        2. 버튼을 누르면 해당 유형에 어울리는  
           **진로 3가지**가 추천됩니다.  
        3. 마음에 드는 진로를 저장해 두고,  
           나중에 다시 비교해 보세요. ✨
        """
    )
    st.divider()
    st.markdown("#### 📌 TIP")
    st.markdown(
        "- 결과는 **참고용 가이드**입니다.\n"
        "- 관심, 성향, 가치관을 함께 고려해 보세요."
    )

# 제목 영역
st.markdown('<div class="main-title">MBTI 진로 상담실 🎓</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">내 성향에 어울리는 진로를 가볍게 탐색해 보는 미니 상담실입니다.</div>',
    unsafe_allow_html=True
)

# 입력 영역
col1, col2 = st.columns([1.2, 1])

with col1:
    selected_mbti = st.selectbox(
        "MBTI 유형을 선택해 주세요 ✋",
        mbti_types,
        index=mbti_types.index("INFJ") if "INFJ" in mbti_types else 0,
        help="본인 또는 학생의 MBTI 유형을 선택해 주세요."
    )

with col2:
    user_name = st.text_input("이름(또는 별명) ✨", placeholder="선택 사항")

st.write("")  # 간격 조정
go = st.button("진로 추천 받기 🔍")

# ----- 결과 영역 -----
if go:
    data = mbti_career_map[selected_mbti]

    # 상단 카드
    header_text = f"{user_name}님의 MBTI는 **{selected_mbti}** 유형, **{data['label']}** 입니다." if user_name else \
                  f"선택한 MBTI는 **{selected_mbti}** 유형, **{data['label']}** 입니다."

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-title">추천 진로 🎯</div>
            <p>{header_text}</p>
            <div>
                {"".join(f'<span class="pill">#{kw}</span>' for kw in data["keywords"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 추천 진로 3가지
    for idx, (job, desc) in enumerate(data["careers"], start=1):
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-title">
                    <span>#{idx}</span> <span>{job}</span>
                </div>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="footer">
            🎓 이 결과를 캡처해서 담임 선생님이나 상담 선생님과 함께<br/>
            더 깊은 진로 상담으로 이어가 보세요.
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.info("왼쪽 옵션에서 MBTI를 선택하고 **진로 추천 받기 🔍** 버튼을 눌러 주세요.")


