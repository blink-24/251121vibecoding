import datetime
from io import StringIO

import pandas as pd
import streamlit as st


# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="MBTI 심리 상담실",
    page_icon="🧠",
    layout="centered",
)

st.title("🧠 MBTI 기반 간단 심리 상담실")
st.write(
    """
MBTI를 선택하고, 요즘 고민을 적어 주면  
당신의 성향을 바탕으로 간단한 피드백지를 만들어 드립니다.
"""
)

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_mbti_countries():
    # 같은 폴더에 있는 CSV 파일명 사용
    return pd.read_csv("countriesMBTI_16types.csv")

df_countries = load_mbti_countries()


# -----------------------------
# MBTI 정보 사전
# -----------------------------
MBTI_TYPES = [
    "INFJ", "ISFJ", "INTP", "ISFP",
    "ENTP", "INFP", "ENTJ", "ISTP",
    "INTJ", "ESFP", "ESTJ", "ENFP",
    "ESTP", "ISTJ", "ENFJ", "ESFJ",
]

MBTI_INFO = {
    "INFJ": {
        "title": "INFJ - 통찰력 있는 이상주의자",
        "strengths": [
            "타인의 감정과 분위기를 잘 읽어낸다.",
            "깊이 있는 대화를 선호하고 진정성을 중시한다.",
        ],
        "risks": [
            "스스로에 대한 기준이 높아 쉽게 지칠 수 있다.",
            "갈등 상황을 피하려다 속으로만 고민을 쌓아두기 쉽다.",
        ],
    },
    "INFP": {
        "title": "INFP - 가치지향적인 중재자",
        "strengths": [
            "자신만의 신념과 가치를 굳게 지킨다.",
            "타인의 상처를 잘 공감하고 위로하는 능력이 있다.",
        ],
        "risks": [
            "현실적인 문제 해결보다 감정에 머물 때가 있다.",
            "자신의 감정을 표현하지 못하고 눌러두기 쉽다.",
        ],
    },
    "INTP": {
        "title": "INTP - 분석적인 사색가",
        "strengths": [
            "복잡한 문제를 구조적으로 분석하는 데 강하다.",
            "아이디어와 가능성을 탐구하는 것을 좋아한다.",
        ],
        "risks": [
            "감정 표현이 서툴러 오해를 살 수 있다.",
            "실행보다 생각 단계에 오래 머무를 수 있다.",
        ],
    },
    "INTJ": {
        "title": "INTJ - 전략적인 계획가",
        "strengths": [
            "장기적인 그림을 그리고 체계적으로 계획한다.",
            "효율과 논리를 중시하며 개선점을 잘 찾는다.",
        ],
        "risks": [
            "비효율적이라고 느끼는 상황에 예민해질 수 있다.",
            "감정적인 공감보다 해결책 제시에만 집중할 수 있다.",
        ],
    },
    "ISFJ": {
        "title": "ISFJ - 성실한 보호자",
        "strengths": [
            "주어진 역할을 책임감 있게 끝까지 수행한다.",
            "주변 사람을 세심하게 돌보는 편이다.",
        ],
        "risks": [
            "자신의 필요를 뒤로 미루고 남을 먼저 챙기기 쉽다.",
            "‘거절’을 잘 못해 부담을 떠안을 수 있다.",
        ],
    },
    "ISFP": {
        "title": "ISFP - 따뜻한 예술가",
        "strengths": [
            "감각적이고 섬세한 표현에 강점이 있다.",
            "타인의 자유와 개성을 존중한다.",
        ],
        "risks": [
            "갈등을 피하려다 중요한 말도 삼킬 수 있다.",
            "계획보다는 즉흥에 치우쳐 불안해질 수 있다.",
        ],
    },
    "ISTJ": {
        "title": "ISTJ - 책임감 있는 관리자",
        "strengths": [
            "규칙과 원칙을 잘 지키고 신뢰를 준다.",
            "디테일을 꼼꼼히 챙기며 실수를 줄인다.",
        ],
        "risks": [
            "변화가 잦은 상황에서 스트레스를 많이 받을 수 있다.",
            "감정보다 사실과 논리에만 집중할 수 있다.",
        ],
    },
    "ISTP": {
        "title": "ISTP - 유연한 문제 해결자",
        "strengths": [
            "문제를 실용적으로 해결하는 데 능숙하다.",
            "위기 상황에서도 침착하게 판단한다.",
        ],
        "risks": [
            "감정 표현을 최소화해 거리감이 느껴질 수 있다.",
            "반복적이고 규칙적인 일에 쉽게 지루해한다.",
        ],
    },
    "ENFJ": {
        "title": "ENFJ - 사람을 이끄는 조언자",
        "strengths": [
            "타인의 잠재력을 발견하고 격려하는 데 능하다.",
            "조직 내 분위기를 조율하고 이끄는 힘이 있다.",
        ],
        "risks": [
            "남을 챙기느라 자기 관리를 놓칠 수 있다.",
            "모두를 만족시키려다 부담을 크게 느낄 수 있다.",
        ],
    },
    "ENFP": {
        "title": "ENFP - 에너지 넘치는 아이디어 메이커",
        "strengths": [
            "새로운 가능성을 떠올리고 사람들을 연결하는 데 강하다.",
            "자유롭고 따뜻한 분위기를 만든다.",
        ],
        "risks": [
            "시작은 많은데 끝까지 가져가는 데 어려움을 느낄 수 있다.",
            "기분 변화가 클 때 스스로도 방향을 잃을 수 있다.",
        ],
    },
    "ENTJ": {
        "title": "ENTJ - 추진력 있는 리더",
        "strengths": [
            "목표를 정하고 조직을 이끌어 가는 능력이 뛰어나다.",
            "비효율을 빠르게 찾아 개선하려 한다.",
        ],
        "risks": [
            "감정보다 성과를 우선해 주변이 부담을 느낄 수 있다.",
            "통제할 수 없는 상황에 큰 스트레스를 받을 수 있다.",
        ],
    },
    "ENTP": {
        "title": "ENTP - 도전적인 발명가",
        "strengths": [
            "토론과 새로운 시도를 즐긴다.",
            "정형화되지 않은 문제에 창의적으로 접근한다.",
        ],
        "risks": [
            "논쟁을 즐기다 관계가 소모될 수 있다.",
            "지루함을 견디기 어려워 한 가지를 오래 유지하기 힘들 수 있다.",
        ],
    },
    "ESFJ": {
        "title": "ESFJ - 다정한 조직가",
        "strengths": [
            "주변 사람의 필요를 잘 파악하고 도와준다.",
            "분위기를 배려하며 조화롭게 이끌려고 한다.",
        ],
        "risks": [
            "타인의 시선과 평가에 예민해질 수 있다.",
            "갈등을 피하려다 자기 의견을 숨길 수 있다.",
        ],
    },
    "ESFP": {
        "title": "ESFP - 밝은 분위기 메이커",
        "strengths": [
            "현재의 즐거움을 잘 찾고 주변에 전파한다.",
            "사람들과 자연스럽게 어울리는 능력이 있다.",
        ],
        "risks": [
            "불편한 감정은 피하려다 나중에 한꺼번에 터질 수 있다.",
            "장기적인 계획이 느슨해져 불안감을 느낄 수 있다.",
        ],
    },
    "ESTJ": {
        "title": "ESTJ - 현실적인 책임자",
        "strengths": [
            "현실적인 기준으로 일을 효율적으로 진행한다.",
            "조직 내에서 역할과 규칙을 명확하게 정한다.",
        ],
        "risks": [
            "융통성이 부족하다는 인상을 줄 수 있다.",
            "감정적인 부분을 간과해 주변이 서운함을 느낄 수 있다.",
        ],
    },
    "ESTP": {
        "title": "ESTP - 즉각적인 실행가",
        "strengths": [
            "상황 판단이 빠르고 행동력 있다.",
            "위기 상황에서도 유연하게 대처한다.",
        ],
        "risks": [
            "충동적으로 행동했다가 뒤늦게 부담을 느낄 수 있다.",
            "장기적인 리스크 관리가 부족할 수 있다.",
        ],
    },
}


ISSUE_SUGGESTIONS = {
    "연애/대인관계": [
        "오늘 하루, 한 사람에게 ‘고마웠던 점 한 가지’를 구체적으로 표현해 보기.",
        "관계를 힘들게 하는 말·행동을 하나 정하고, 이번 주에는 그 빈도를 의식적으로 줄여 보기.",
        "상대에게 요구하기 전에, 내가 먼저 해 줄 수 있는 행동을 한 가지 실천해 보기.",
    ],
    "진로/학업": [
        "지금 가장 중요한 과제·목표 한 가지를 정하고, 오늘 안에 할 수 있는 최소 행동을 정해 실행해 보기.",
        "하고 싶은 일·하기 싫은 일을 각각 3가지 적고, 공통된 키워드를 찾아보기.",
        "‘1년 뒤의 나’에게 편지를 쓴다는 마음으로, 이루고 싶은 모습을 간단히 적어 보기.",
    ],
    "가족/생활": [
        "가족 혹은 가까운 사람과 10분 정도만이라도 방해 없이 대화하는 시간을 가져 보기.",
        "하루 루틴에서 나를 가장 지치게 하는 일을 하나 골라, 조금이라도 단축할 방법을 생각해 보기.",
        "집/방 안에서 내가 편안함을 느끼는 공간을 하나 만들거나 정돈해 보기.",
    ],
    "자기이해/감정": [
        "오늘 느꼈던 감정을 세 단어로 적고, 각 감정의 이유를 한 줄씩 써 보기.",
        "‘지금 나에게 가장 필요한 한 마디 위로’를 스스로에게 적어 보기.",
        "감정이 올라올 때 숨을 세 번 깊게 쉬고, 몸의 감각(심장 박동, 어깨 긴장)을 한번 살펴보기.",
    ],
}


# -----------------------------
# 사이드바: MBTI 선택
# -----------------------------
st.sidebar.header("🧩 MBTI 선택")
selected_mbti = st.sidebar.selectbox("당신의 MBTI를 선택해 주세요.", MBTI_TYPES, index=0)

st.sidebar.markdown("---")
st.sidebar.caption("※ 실제 전문 상담을 대체하지 않는, 가벼운 자기 점검 도구입니다.")


# -----------------------------
# MBTI 요약 정보 & 국가 정보
# -----------------------------
info = MBTI_INFO.get(
    selected_mbti,
    {
        "title": f"{selected_mbti}",
        "strengths": [],
        "risks": [],
    },
)

st.subheader("① 나의 MBTI 간단 프로필")

st.markdown(f"**{info['title']}**")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**강점으로 보이는 부분**")
    for s in info["strengths"]:
        st.markdown(f"- {s}")

    st.markdown("**주의하면 좋은 부분**")
    for r in info["risks"]:
        st.markdown(f"- {r}")

with col2:
    st.markdown("**이 MBTI가 많은 나라 TOP 3 (데이터 기준)**")
    if selected_mbti in df_countries.columns:
        top3 = (
            df_countries[["Country", selected_mbti]]
            .sort_values(by=selected_mbti, ascending=False)
            .head(3)
        )
        for _, row in top3.iterrows():
            st.markdown(f"- {row['Country']}")
    else:
        st.write("데이터에 해당 MBTI 정보가 없습니다.")


# -----------------------------
# 현재 상태 입력
# -----------------------------
st.subheader("② 지금 마음 상태를 알려 주세요")

name = st.text_input("이름 또는 닉네임 (선택 사항)", "")

issue = st.selectbox(
    "요즘 가장 신경 쓰이는 영역은 무엇인가요?",
    list(ISSUE_SUGGESTIONS.keys()),
)

mood = st.radio(
    "요즘 전반적인 기분에 가장 가까운 것은?",
    ["대체로 안정적이다", "불안하고 예민하다", "무기력하고 아무것도 하기 싫다", "들뜨거나 기분 변화가 크다"],
)

stress = st.slider("요즘 스트레스 수준은 어느 정도인가요?", 1, 10, 5)

concern = st.text_area(
    "요즘 가장 고민되는 점을 편하게 적어 주세요.",
    placeholder="예) 사람들과 있을 땐 괜찮은데, 혼자 있으면 괜히 불안해져요...",
    height=150,
)


# -----------------------------
# 피드백지 생성 함수
# -----------------------------
def build_feedback_text(
    name: str,
    mbti: str,
    issue: str,
    mood: str,
    stress: int,
    concern: str,
) -> str:
    display_name = name if name.strip() else "내담자"
    today = datetime.date.today().strftime("%Y-%m-%d")

    # 국가 정보 요약
    if mbti in df_countries.columns:
        top3 = (
            df_countries[["Country", mbti]]
            .sort_values(by=mbti, ascending=False)
            .head(3)
        )
        country_text = ", ".join(top3["Country"].tolist())
    else:
        country_text = "데이터 없음"

    strengths = MBTI_INFO.get(mbti, {}).get("strengths", [])
    risks = MBTI_INFO.get(mbti, {}).get("risks", [])

    strengths_text = "\n".join([f"- {s}" for s in strengths]) if strengths else "- (정보 없음)"
    risks_text = "\n".join([f"- {r}" for r in risks]) if risks else "- (정보 없음)"

    # 고민 요약 (너무 길면 앞부분만 사용)
    clean_concern = concern.strip()
    if len(clean_concern) > 300:
        concern_summary = clean_concern[:300] + "..."
    else:
        concern_summary = clean_concern if clean_concern else "별도로 적힌 고민 내용은 없었습니다."

    # 실천 과제
    suggestions = ISSUE_SUGGESTIONS.get(issue, [])
    if not suggestions:
        action_text = "- (준비된 제안 없음)"
    else:
        action_text = "\n".join([f"{idx+1}. {s}" for idx, s in enumerate(suggestions)])

    feedback = f"""[MBTI 간단 상담 피드백지]

■ 기본 정보
- 이름(닉네임): {display_name}
- MBTI: {mbti}
- 상담 날짜: {today}
- 주요 고민 영역: {issue}
- 전반적인 기분: {mood}
- 자가 보고 스트레스 수준(1~10): {stress}

■ MBTI 특징 정리
[강점으로 보이는 부분]
{strengths_text}

[주의하면 좋은 부분]
{risks_text}

※ 이 MBTI 비율이 상대적으로 높은 나라(데이터 기준): {country_text}

■ 현재 고민 요약
{concern_summary}

■ MBTI 관점에서의 이해
- {mbti} 유형인 {display_name}님은, 위와 같은 상황에서도 자신의 가치와 기준을 지키고자 하는 경향이 있습니다.
- 동시에 주변의 기대나 관계, 성과에 대한 압박을 혼자 떠안으며 스트레스를 키울 수 있습니다.
- 이번 고민을 통해, ‘지금 당장 바꿀 수 있는 한 가지’와 ‘당장은 바꾸기 어렵지만 인정해야 할 부분’을 나누어 보는 것이 도움이 될 수 있습니다.

■ 앞으로 1주일 동안의 작은 실천 과제
{action_text}

■ 스스로에게 남기는 한 줄 메모
- 오늘 이 피드백지를 읽으며 떠오른 생각이나 다짐을 한 줄로 적어 보세요.
"""

    return feedback


# -----------------------------
# 상담 완료 버튼
# -----------------------------
st.subheader("③ 상담 완료 및 피드백지 받기")

if st.button("✅ 상담 완료"):
    feedback_text = build_feedback_text(
        name=name,
        mbti=selected_mbti,
        issue=issue,
        mood=mood,
        stress=stress,
        concern=concern,
    )

    st.success("상담이 완료되었습니다. 아래에서 피드백지를 확인하고 다운로드할 수 있습니다.")

    st.markdown("### ✉️ 나만의 피드백지 미리보기")
    # 줄바꿈 유지
    st.markdown(feedback_text.replace("\n", "  \n"))

    st.download_button(
        label="📝 피드백지 다운로드 (.txt)",
        data=feedback_text,
        file_name=f"{(name or '내담자')}_{selected_mbti}_피드백지.txt",
        mime="text/plain",
    )
else:
    st.info("MBTI를 선택하고 고민을 적은 뒤, **‘상담 완료’ 버튼**을 눌러 피드백지를 받아 보세요.")
