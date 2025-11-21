import streamlit as st

# 기본 페이지 설정
st.set_page_config(
    page_title="MBTI 별 고전 추천",
    page_icon="📚",
    layout="wide",
)

# 간단한 커스텀 CSS (Streamlit 기본 기능만 활용)
st.markdown(
    """
    <style>
    /* 전체 배경 그라데이션 */
    .stApp {
        background: radial-gradient(circle at top left, #fdf2ff 0, #f4f9ff 40%, #f9fafb 100%);
    }

    /* 본문 폭 조금 줄이기 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    /* 제목 꾸미기 */
    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .main-subtitle {
        font-size: 1rem;
        color: #4b5563;
        margin-bottom: 1.5rem;
    }

    /* 칩 스타일 */
    .pill {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #e5e7eb;
        font-size: 0.8rem;
        margin-right: 0.3rem;
        margin-bottom: 0.3rem;
    }

    /* 책 카드 */
    .book-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        box-shadow:
            0 18px 40px rgba(15, 23, 42, 0.08),
            0 0 0 1px rgba(148, 163, 184, 0.18);
        display: flex;
        gap: 0.9rem;
        margin-bottom: 0.8rem;
        backdrop-filter: blur(10px);
    }
    .book-emoji {
        font-size: 1.9rem;
        line-height: 1;
    }
    .book-main h3 {
        font-size: 1.05rem;
        margin: 0;
        margin-bottom: 0.15rem;
    }
    .book-author {
        font-size: 0.85rem;
        color: #6b7280;
        margin-bottom: 0.2rem;
    }
    .book-reason {
        font-size: 0.9rem;
        color: #374151;
    }

    /* 작은 섹션 제목 */
    .section-label {
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        color: #9ca3af;
        margin-bottom: 0.1rem;
    }

    /* 푸터 */
    .footer {
        margin-top: 2rem;
        font-size: 0.8rem;
        color: #9ca3af;
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# MBTI → 대표 이모지
mbti_emoji = {
    "INTJ": "🧠",
    "INTP": "🧩",
    "ENTJ": "📈",
    "ENTP": "⚡",
    "INFJ": "🕊️",
    "INFP": "🌙",
    "ENFJ": "🌈",
    "ENFP": "🎈",
    "ISTJ": "📐",
    "ISFJ": "🧵",
    "ESTJ": "📋",
    "ESFJ": "🤝",
    "ISTP": "🛠️",
    "ISFP": "🎨",
    "ESTP": "🔥",
    "ESFP": "🎵",
}

# MBTI별 고전 추천 데이터
classic_recs = {
    "INFJ": [
        {
            "title": "죄와 벌(표도르 도스토예프스키)",
            "author": "표도르 도스토예프스키",
            "emoji": "⚖️",
            "reason": "도덕과 구원, 죄책감과 책임을 집요하게 묻는 작품으로, 가치와 신념을 깊이 탐구하는 INFJ의 사유와 잘 맞는다.",
        },
        {
            "title": "데미안(헤르만 헤세)",
            "author": "헤르만 헤세",
            "emoji": "🪞",
            "reason": "자기 탐색과 성장, ‘나만의 길’을 찾는 여정이 내적 세계가 풍부한 INFJ의 감수성과 잘 어울린다.",
        },
    ],
    "INFP": [
        {
            "title": "어린 왕자(앙투안 드 생텍쥐페리)",
            "author": "앙투안 드 생텍쥐페리",
            "emoji": "⭐",
            "reason": "순수함과 상상력, 본질에 대한 질문이 가득한 이야기로, 이상과 꿈을 중시하는 INFP의 마음을 잘 건드린다.",
        },
        {
            "title": "폭풍의 언덕(에밀리 브론테)",
            "author": "에밀리 브론테",
            "emoji": "🌪️",
            "reason": "격정적인 사랑과 감정의 깊이가, 내면의 정서를 섬세히 느끼는 INFP에게 강렬한 인상을 남긴다.",
        },
    ],
    "INTJ": [
        {
            "title": "군주론(니콜로 마키아벨리)",
            "author": "니콜로 마키아벨리",
            "emoji": "♟️",
            "reason": "권력과 전략을 냉철하게 분석하는 고전으로, 구조와 원리를 파악하는 INTJ의 분석력과 잘 어울린다.",
        },
        {
            "title": "칸트의 순수이성비판(임마누엘 칸트)",
            "author": "임마누엘 칸트",
            "emoji": "📚",
            "reason": "인식의 한계와 이성의 구조를 논리적으로 파고드는 철학서로, 추상적 사유를 좋아하는 INTJ에게 도전적인 텍스트이다.",
        },
    ],
    "INTP": [
        {
            "title": "소크라테스의 변명(플라톤)",
            "author": "플라톤",
            "emoji": "❓",
            "reason": "질문과 논박으로 진리를 탐구하는 태도가, 개념과 논리를 즐기는 INTP의 스타일과 잘 맞는다.",
        },
        {
            "title": "시간과 공간에 관한 프루스트의 에세이들(마르셀 프루스트)",
            "author": "마르셀 프루스트",
            "emoji": "⏳",
            "reason": "기억과 의식에 대한 섬세한 분석이, 사유의 미세한 결을 추적하는 INTP에게 흥미로운 장을 제공한다.",
        },
    ],
    "ENFJ": [
        {
            "title": "레 미제라블(빅토르 위고)",
            "author": "빅토르 위고",
            "emoji": "🕯️",
            "reason": "정의와 연대, 인간애가 응축된 서사로, 타인을 돕고 변화를 이끄는 ENFJ의 리더십과 잘 통한다.",
        },
        {
            "title": "토지(박경리)",
            "author": "박경리",
            "emoji": "🌾",
            "reason": "역사와 사람들의 삶이 촘촘하게 얽힌 대하소설로, 공동체와 관계를 중시하는 ENFJ에게 울림이 크다.",
        },
    ],
    "ENFP": [
        {
            "title": "허클베리 핀의 모험(마크 트웨인)",
            "author": "마크 트웨인",
            "emoji": "🛶",
            "reason": "자유로운 여행과 모험, 규범을 향한 장난기 있는 저항이 ENFP의 에너지와 잘 어울린다.",
        },
        {
            "title": "변신(프란츠 카프카)",
            "author": "프란츠 카프카",
            "emoji": "🦋",
            "reason": "일상의 갑작스러운 변화와 부조리가 담긴 이야기로, 상상력이 풍부한 ENFP에게 여러 해석을 열어 준다.",
        },
    ],
    "ENTJ": [
        {
            "title": "국가(플라톤)",
            "author": "플라톤",
            "emoji": "🏛️",
            "reason": "이상 국가와 정의, 통치에 대한 구상이, 구조를 설계하고 방향을 제시하는 ENTJ의 기질과 맞닿아 있다.",
        },
        {
            "title": "자본론(마르크스)",
            "author": "카를 마르크스",
            "emoji": "🏭",
            "reason": "경제 구조를 큰 틀에서 분석하고 재구성하는 시도가, 시스템을 장기적으로 보는 ENTJ에게 자극이 된다.",
        },
    ],
    "ENTP": [
        {
            "title": "돈키호테(세르반테스)",
            "author": "미겔 데 세르반테스",
            "emoji": "🗡️",
            "reason": "이상과 현실이 충돌하는 풍자적 모험담으로, 아이디어와 토론을 즐기는 ENTP의 유쾌한 도발과 닮아 있다.",
        },
        {
            "title": "수레바퀴 아래서(헤르만 헤세)",
            "author": "헤르만 헤세",
            "emoji": "🚃",
            "reason": "제도와 개인의 갈등을 다루며, 기존 틀을 비판적으로 바라보는 ENTP의 시선에 깊은 공감을 준다.",
        },
    ],
    "ISTJ": [
        {
            "title": "안나 카레니나(톨스토이)",
            "author": "레프 톨스토이",
            "emoji": "📏",
            "reason": "규범과 책임, 선택의 후폭풍을 세밀하게 그려, 원칙과 현실 사이의 균형을 중요시하는 ISTJ에게 생각거리를 준다.",
        },
        {
            "title": "삼국지연의(나관중)",
            "author": "나관중",
            "emoji": "🛡️",
            "reason": "충,의,질서, 전략이 뒤얽힌 고전으로, 체계와 전통을 중시하는 ISTJ에게 익숙하면서도 깊은 재미를 선사한다.",
        },
    ],
    "ISFJ": [
        {
            "title": "작은 아씨들(루이자 메이 올컷)",
            "author": "루이자 메이 올컷",
            "emoji": "🏡",
            "reason": "가족, 돌봄, 배려가 중심에 있는 이야기로, 헌신적인 ISFJ의 따뜻한 면모와 잘 어울린다.",
        },
        {
            "title": "현진건의 단편선(현진건)",
            "author": "현진건",
            "emoji": "🧺",
            "reason": "일상의 비애와 소시민의 마음을 담담히 그려, 사람을 세심하게 살피는 ISFJ의 정서와 잘 맞는다.",
        },
    ],
    "ESTJ": [
        {
            "title": "로마인 이야기(시오노 나나미)",
            "author": "시오노 나나미",
            "emoji": "🧱",
            "reason": "역사 속 조직과 리더십을 사례 중심으로 보여 주어, 현실적인 ESTJ에게 실용적인 통찰을 준다.",
        },
        {
            "title": "대한민국 현대사 관련 교양서 한 권",
            "author": "여러 저자",
            "emoji": "📊",
            "reason": "제도와 시스템이 어떻게 만들어졌는지를 아는 것은, 실제를 중시하는 ESTJ의 의사결정에 직접적인 도움이 된다.",
        },
    ],
    "ESFJ": [
        {
            "title": "톨스토이의 인생독본(레프 톨스토이)",
            "author": "레프 톨스토이",
            "emoji": "💌",
            "reason": "삶과 관계에 대한 짧은 성찰들이, 사람과 일상을 소중히 여기는 ESFJ에게 잔잔한 지침이 된다.",
        },
        {
            "title": "상실의 시대(무라카미 하루키)",
            "author": "무라카미 하루키",
            "emoji": "🍂",
            "reason": "사랑과 상실, 성장의 이야기가, 타인의 감정을 세심히 보살피는 ESFJ에게 공감의 창을 열어 준다.",
        },
    ],
    "ISTP": [
        {
            "title": "로빈슨 크루소(대니얼 디포)",
            "author": "대니얼 디포",
            "emoji": "🏝️",
            "reason": "생존과 문제 해결, 자급자족의 이야기로, 실용적인 해결책을 찾는 ISTP의 기질과 잘 맞는다.",
        },
        {
            "title": "노인과 바다(어니스트 헤밍웨이)",
            "author": "어니스트 헤밍웨이",
            "emoji": "🎣",
            "reason": "말수 적은 주인공의 행동과 태도를 통해, 묵묵히 해내는 ISTP의 고독한 집중력을 비춘다.",
        },
    ],
    "ISFP": [
        {
            "title": "데미안(헤르만 헤세)",
            "author": "헤르만 헤세",
            "emoji": "🎨",
            "reason": "자기만의 색을 찾는 성장 서사가, 미적 감수성이 풍부한 ISFP의 예술적 자아와 어울린다.",
        },
        {
            "title": "수필집 한 권(피천득, 법정 등)",
            "author": "여러 저자",
            "emoji": "🍃",
            "reason": "조용한 자연과 일상의 감각을 담은 수필은, 현재의 순간을 소중히 느끼는 ISFP에게 잘 맞는 형식이다.",
        },
    ],
    "ESTP": [
        {
            "title": "삼국지연의(나관중)",
            "author": "나관중",
            "emoji": "⚔️",
            "reason": "전투와 전략, 상황 판단이 쉴 틈없이 이어져, 현장감과 액션을 좋아하는 ESTP에게 몰입감을 준다.",
        },
        {
            "title": "오셀로(셰익스피어)",
            "author": "윌리엄 셰익스피어",
            "emoji": "🎭",
            "reason": "질투와 오해, 감정 폭발이 긴장감 있게 전개되어, 강렬한 드라마를 즐기는 ESTP에게 인상이 깊다.",
        },
    ],
    "ESFP": [
        {
            "title": "위대한 개츠비(프랜시스 스콧 피츠제럴드)",
            "author": "프랜시스 스콧 피츠제럴드",
            "emoji": "🎉",
            "reason": "화려한 파티와 사랑, 허무가 공존하는 이야기로, 경험과 감정을 중시하는 ESFP의 삶의 무대와 닮아 있다.",
        },
        {
            "title": "햄릿(셰익스피어)",
            "author": "윌리엄 셰익스피어",
            "emoji": "🎬",
            "reason": "비극적이지만 극적인 장면과 대사가 많아, 감정 표현이 풍부한 ESFP에게 연극 같은 몰입을 선사한다.",
        },
    ],
}

# ---- 사이드바 ----
with st.sidebar:
    st.markdown("### 🧭 MBTI 고전 나침반")
    st.markdown(
        """
        MBTI 유형을 고르고 나면  
        그 사람의 **기질과 잘 어울리는 고전**들을 추천해 줍니다.

        - 📚 어떤 클래식을 먼저 읽어야 할지 막막할 때  
        - ☕ 조용한 독서 시간에 분위기 맞는 책이 필요할 때  
        - 🎁 친구 MBTI에 맞춰 책 선물을 고르고 싶을 때

        아래에서 **당신의 MBTI**를 골라 보세요!
        """
    )

# ---- 메인 영역 ----
st.markdown(
    """
    <div class="main-title">
        <span>📚 MBTI 별 고전 추천 라운지</span>
    </div>
    <div class="main-subtitle">
        오늘의 기분과 잘 어울리는 고전을, 당신의 MBTI 감성에 맞춰 골라 드립니다.
    </div>
    """,
    unsafe_allow_html=True,
)

col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<div class="section-label">Step 1</div>', unsafe_allow_html=True)
    selected_mbti = st.selectbox(
        "당신의 MBTI를 선택해 주세요",
        list(mbti_emoji.keys()),
        index=list(mbti_emoji.keys()).index("INFJ") if "INFJ" in mbti_emoji else 0,
    )

with col_right:
    st.markdown('<div class="section-label">Tip</div>', unsafe_allow_html=True)
    st.markdown(
        """
        - 혹시 MBTI를 몰라도,  
          **느낌 가는 유형**을 하나 골라 보세요.  
        - 이 앱의 추천은 *가벼운 영감* 정도로 받아들이면 더 재밌습니다. 😄
        """
    )

st.markdown("---")

# 선택한 MBTI 정보 표시
emoji = mbti_emoji.get(selected_mbti, "📚")
st.markdown(
    f"""
    <div class="section-label">Recommendation</div>
    <h2>{emoji} {selected_mbti} 유형에게 어울리는 고전 목록</h2>
    """,
    unsafe_allow_html=True,
)

# 유형 분위기 태그
vibe_tags = {
    "N": "상상력",
    "S": "현실감",
    "T": "논리",
    "F": "감성",
    "J": "계획형",
    "P": "탐험형",
    "I": "내향",
    "E": "외향",
}
st.markdown(
    "".join(
        f'<span class="pill">{ch} · {vibe_tags.get(ch, "")}</span>'
        for ch in selected_mbti
    ),
    unsafe_allow_html=True,
)

st.markdown("")

# 책 카드 렌더링 함수
def render_book_card(book: dict):
    st.markdown(
        f"""
        <div class="book-card">
            <div class="book-emoji">{book.get("emoji", "📖")}</div>
            <div class="book-main">
                <h3>{book["title"]}</h3>
                <p class="book-author">✒️ {book["author"]}</p>
                <p class="book-reason">{book["reason"]}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


recs = classic_recs.get(selected_mbti, [])

if recs:
    for book in recs:
        render_book_card(book)
else:
    st.info("이 유형에 대한 추천이 아직 준비 중입니다. 다른 유형을 한 번 선택해 보세요! 🙂")

st.markdown(
    """
    <div class="footer">
        ✨ 이 웹앱은 MBTI와 고전을 가볍게 연결해 보는 놀이 공간입니다.<br>
        깊이 공감되는 책이 하나라도 생겼다면, 이미 성공이에요. 📚
    </div>
    """,
    unsafe_allow_html=True,
)
