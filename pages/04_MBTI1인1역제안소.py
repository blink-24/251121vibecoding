import streamlit as st
import pandas as pd

# -----------------------
# 기본 설정
# -----------------------
st.set_page_config(
    page_title="MBTI 기반 1인1역 추천",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 MBTI 기반 1인1역 추천 웹앱")
st.write("MBTI 성향을 바탕으로, 학급에서 어울리는 1인1역을 추천해주는 간단한 도우미입니다.")

# -----------------------
# 데이터 불러오기 (나라별 MBTI 분포 CSV)
# - 선택한 MBTI가 많은 나라 TOP 5를 보여주는 용도
# -----------------------
@st.cache_data
def load_mbti_country_data():
    try:
        df = pd.read_csv("countriesMBTI_16types.csv")
        return df
    except FileNotFoundError:
        return None

country_df = load_mbti_country_data()

# -----------------------
# 1인1역 체계 정의
# -----------------------

ROLES = [
    {
        "id": "admin_audit",
        "department": "행정부",
        "icon": "🏛️",
        "name": "감사원",
        "tagline": "의사소통 및 공동체 역량 강화 담당",
        "bullet_points": [
            "학급 규칙을 잘 숙지하고 솔선수범하여 적용한다.",
            "1인1역 수행 상황을 중간 점검하고 담임에게 보고한다.",
            "위급 상황 발생 시 즉시 담임에게 알린다.",
            "반장·부반장과 함께 학급 행사를 기획하고 준비한다.",
            "학급 회의에서 건의 사항이 있을 경우 학급 구성원을 대변한다.",
            "[공동체 의식 함양 캠페인] 봉사활동 최대 12시간 (활동 내역에 따라 차등 지급)"
        ],
        "highlight": "행동특성 및 종합의견에 의사소통·공동체 역량으로 반영 가능",
    },
    {
        "id": "study_helper",
        "department": "교과학습부",
        "icon": "📚",
        "name": "면학도우미",
        "tagline": "수업 분위기와 학습 몰입을 이끄는 역할",
        "bullet_points": [
            "솔선수범하는 수업 태도로 친구들에게 좋은 본보기가 된다.",
            "특별 활동 시간 포함, 수업 참여를 적극적으로 독려한다.",
            "수업 시작 시 잠들어 있는 친구들을 깨워 수업에 참여하도록 돕는다.",
        ],
        "highlight": "수업 태도와 학습 참여도 향상에 기여",
    },
    {
        "id": "env_door",
        "department": "환경안전부",
        "icon": "🚪",
        "name": "문단속 및 이동 수업 관리",
        "tagline": "안전하고 정돈된 교실을 책임지는 수호자",
        "bullet_points": [
            "이동 수업 및 하교 시 교실 문단속을 철저히 확인한다.",
            "교실 복귀 전 두고 간 물건이 없는지 확인한다.",
        ],
        "highlight": "책임감과 꼼꼼함을 드러낼 수 있는 역할",
    },
    {
        "id": "env_locker",
        "department": "환경안전부",
        "icon": "🔑",
        "name": "사물함 담당자",
        "tagline": "사물함 관리 및 문제 해결 1차 창구",
        "bullet_points": [
            "사물함 열쇠를 안전하게 보관·관리한다.",
            "사물함 관련 간단한 문제는 1차적으로 해결하고, 필요 시 담임에게 도움을 요청한다.",
        ],
        "highlight": "신뢰성과 성실함을 보여줄 수 있는 역할",
    },
    {
        "id": "env_ventilation",
        "department": "환경안전부",
        "icon": "🌬️",
        "name": "교실 환기 담당",
        "tagline": "쾌적한 공기 질을 책임지는 공기 관리자",
        "bullet_points": [
            "공기가 답답할 때 적절한 시점에 창문을 열어 환기한다.",
            "체육 시간 후, 점심 시간 중 교실을 환기하여 쾌적한 환경을 유지한다.",
        ],
        "highlight": "친구들의 건강과 학습 집중도를 돕는 역할",
    },
    {
        "id": "env_power",
        "department": "환경안전부",
        "icon": "💡",
        "name": "전원 관리 담당",
        "tagline": "전기·전원 관리로 에너지 절약을 실천",
        "bullet_points": [
            "공기청정기, 에어컨, 전등 등의 전원을 상황에 맞게 관리한다.",
            "이동 수업 시 교실의 전원을 꼼꼼히 끄고, 수업 종료 후 적절히 켜기·끄기를 관리한다.",
        ],
        "highlight": "책임감과 세심함을 보여줄 수 있는 역할",
    },
    {
        "id": "env_attendance",
        "department": "환경안전부",
        "icon": "📝",
        "name": "출석부 관리",
        "tagline": "출결 기록을 꼼꼼하게 챙기는 기록 담당",
        "bullet_points": [
            "담임 지시에 따라 출석부를 관리하고 필요한 사항을 정확히 기록한다.",
            "이동 수업 전후 출석 상황을 점검하는 데 협조한다.",
        ],
        "highlight": "정확성과 성실성이 드러나는 역할",
    },
    {
        "id": "board_manager",
        "department": "과기정통부",
        "icon": "🧽",
        "name": "칠판 담당 (월~금)",
        "tagline": "칠판과 필기 환경을 책임지는 보이지 않는 조력자",
        "bullet_points": [
            "수업 전·후 칠판을 깨끗하게 정리한다.",
            "칠판 지우개가 더러워졌을 때 털어 깨끗하게 관리한다.",
            "사용이 어려운 분필을 정리하고, 네 가지 색 분필을 항상 채워 둔다.",
        ],
        "highlight": "수업 환경을 안정적으로 유지하는데 기여",
    },
    {
        "id": "notice_manager",
        "department": "과기정통부",
        "icon": "📌",
        "name": "공지사항·게시판·시간표 관리",
        "tagline": "우리 반 정보 허브를 관리하는 안내 담당",
        "bullet_points": [
            "오늘의 급식 식단을 칠판 구석에 업데이트한다.",
            "교과 공지 사항, 가정통신문 여분을 학급 게시판에 정리해 부착한다.",
            "날짜가 지난 안내물은 회수하여 깔끔한 게시판을 유지한다.",
            "시간표 변동 사항을 반 친구들에게 안내한다.",
        ],
        "highlight": "정보 전달과 정리 능력을 활용하는 역할",
    },
    {
        "id": "equipment_manager",
        "department": "과기정통부",
        "icon": "🖥️",
        "name": "비품 관리",
        "tagline": "학급 공용 물품과 디지털 기기를 책임지는 관리자",
        "bullet_points": [
            "학급 비품(볼펜, 물티슈 등) 수요를 파악하고 소진 시 교무실에서 받아온다.",
            "TV, 컴퓨터 등 기본적인 문제 상황을 1차 점검한다.",
            "리모컨과 케이블 상태(청결, 건전지)를 확인·관리한다.",
            "디벗 충전함을 정리·관리하여 기기가 안전하게 보관되도록 한다.",
        ],
        "highlight": "디지털 기기에 관심이 많거나 꼼꼼한 학생에게 적합",
    },
]

# MBTI 유형 목록 (16가지)
MBTI_TYPES = [
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISFJ", "ESFJ", "ISTJ", "ESTJ",
    "INTJ", "INTP", "ENTJ", "ENTP",
    "ISFP", "INFP", "ESFP", "ESTP"
]

# 중복 제거 (위에서 INFP를 두 번 넣었으므로 정리)
MBTI_TYPES = sorted(list(set(MBTI_TYPES)))

# -----------------------
# MBTI → 추천 역할 매핑 로직
# - 아주 단순한 규칙 기반 추천 (필요하면 이후 승준쌤이 수정해서 사용)
# -----------------------

def recommend_roles(mbti: str):
    mbti = mbti.upper()

    # 4가지 기질 그룹으로 나누어 대략적인 성향 반영
    is_n = "N" in mbti
    is_s = "S" in mbti
    is_f = "F" in mbti
    is_t = "T" in mbti
    is_j = "J" in mbti
    is_p = "P" in mbti
    is_e = "E" in mbti
    is_i = "I" in mbti

    recommended_ids = []

    # 1) 사람을 챙기고 조정하는 NF, EJ 계열 → 행정부 / 감사원, 공지·게시판
    if is_f and (is_n or is_e):
        recommended_ids.extend(["admin_audit", "notice_manager"])

    # 2) 꼼꼼·성실한 SJ, TJ 계열 → 문단속, 전원 관리, 출석부, 사물함
    if is_s and is_j:
        recommended_ids.extend(["env_door", "env_power", "env_attendance", "env_locker"])

    # 3) 조용히 뒷정리·환경 관리 좋아할 법한 I + P/S 계열 → 환기, 칠판, 비품
    if is_i and is_p:
        recommended_ids.extend(["env_ventilation", "board_manager"])

    # 4) 수업 태도 모범 / 학습 리더십 → N/T/F 조합 일부
    if is_f or (is_n and is_j):
        recommended_ids.append("study_helper")

    # 5) 디지털·장비 관심 있을 법한 NT, TP 계열 → 비품 관리, 공지 관리
    if is_t and (is_n or is_p):
        recommended_ids.append("equipment_manager")

    # 중복 제거 후, 실제 존재하는 id만 필터링
    valid_ids = {r["id"] for r in ROLES}
    unique_ids = []
    for rid in recommended_ids:
        if rid in valid_ids and rid not in unique_ids:
            unique_ids.append(rid)

    # 혹시라도 비어 있으면 기본 추천
    if not unique_ids:
        unique_ids = ["study_helper", "env_door"]

    # id → role dict로 변환
    id_to_role = {r["id"]: r for r in ROLES}
    return [id_to_role[rid] for rid in unique_ids]


# -----------------------
# 사이드바: MBTI 선택
# -----------------------
st.sidebar.header("⚙️ 설정")
selected_mbti = st.sidebar.selectbox("내 MBTI 선택", MBTI_TYPES, index=0)
st.sidebar.write(f"선택한 유형: **{selected_mbti}**")

st.write("---")

# -----------------------
# 메인 영역: 추천 결과 보여주기
# -----------------------
st.subheader(f"✨ {selected_mbti} 유형을 위한 1인1역 추천")

roles = recommend_roles(selected_mbti)

cols = st.columns(2)

for i, role in enumerate(roles):
    col = cols[i % 2]
    with col:
        st.markdown(
            f"""
            <div style="
                border-radius: 18px;
                padding: 1rem 1.2rem;
                margin-bottom: 1rem;
                border: 1px solid rgba(200,200,200,0.5);
                background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(245,247,250,0.9));
            ">
                <h3 style="margin-bottom: 0.2rem;">{role['icon']} {role['department']} · {role['name']}</h3>
                <p style="margin-top: 0; color: #555;">{role['tagline']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander("📋 역할 세부 내용 보기", expanded=False):
            for bullet in role["bullet_points"]:
                st.markdown(f"- {bullet}")
            if role.get("highlight"):
                st.markdown(f"➡️ **포인트:** {role['highlight']}")

st.write("---")

# -----------------------
# (옵션) 선택한 MBTI가 많은 나라 TOP 5
# -----------------------
st.subheader("🌍 내 MBTI가 많은 나라 TOP 5 (참고용)")

if country_df is None:
    st.info("`countriesMBTI_16types.csv` 파일을 찾지 못했습니다. 같은 폴더에 CSV 파일을 두면 나라별 통계가 표시됩니다.")
else:
    if selected_mbti not in country_df.columns:
        st.info(f"CSV 파일에 `{selected_mbti}` 컬럼이 없습니다. 컬럼명을 한 번 확인해 주세요.")
    else:
        top5 = (
            country_df[["Country", selected_mbti]]
            .sort_values(by=selected_mbti, ascending=False)
            .head(5)
        )
        top5 = top5.rename(columns={
            "Country": "나라",
            selected_mbti: "비율(0~1)"
        })
        st.table(top5.reset_index(drop=True))
        st.caption("※ 출처: 업로드한 MBTI-국가 분포 데이터 (수치는 참고용 비율입니다.)")
