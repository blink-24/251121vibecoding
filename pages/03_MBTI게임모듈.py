import random

import pandas as pd
import streamlit as st


# --------------------
# 데이터 로드 함수
# --------------------
@st.cache_data
def load_data():
    # 같은 폴더에 있는 CSV 파일 사용
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df


# --------------------
# 문제 생성 로직
# --------------------
def make_question(df, mbti_type: str):
    """
    특정 MBTI 유형에 대해
    - 전 세계에서 해당 유형 비율이 가장 높은 국가 1개를 정답으로 잡고
    - 나머지 3개 국가는 무작위 오답으로 뽑아
    - 총 4지선다 선택지를 반환
    """
    # 해당 MBTI 열 기준으로 내림차순 정렬
    sorted_df = df.sort_values(by=mbti_type, ascending=False)

    # 정답: 해당 유형 비율이 가장 높은 국가 1개
    answer_row = sorted_df.iloc[0]
    answer_country = answer_row["Country"]

    # 오답 후보: 상위권 말고, 중간 이후에서 무작위로 뽑기 (난이도 조절용)
    # 예: 20위 이후에서 랜덤 추출
    wrong_pool = sorted_df.iloc[20:]

    # 국가 수가 적은 경우 대비
    if len(wrong_pool) < 3:
        wrong_pool = sorted_df.iloc[1:]

    wrong_countries = (
        wrong_pool["Country"]
        .drop_duplicates()
        .sample(3, replace=False, random_state=random.randint(0, 10_000))
        .tolist()
    )

    options = wrong_countries + [answer_country]
    random.shuffle(options)

    return {
        "mbti": mbti_type,
        "answer": answer_country,
        "options": options,
    }


# --------------------
# 세션 상태 초기화
# --------------------
def init_session_state():
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "total" not in st.session_state:
        st.session_state.total = 0
    if "streak" not in st.session_state:
        st.session_state.streak = 0
    if "question" not in st.session_state:
        st.session_state.question = None
    if "last_feedback" not in st.session_state:
        st.session_state.last_feedback = ""
    if "last_correct" not in st.session_state:
        st.session_state.last_correct = None
    if "selected_mbti" not in st.session_state:
        st.session_state.selected_mbti = None


# --------------------
# 메인 앱
# --------------------
def main():
    st.set_page_config(
        page_title="MBTI 세계 정복 퀴즈 🌎",
        page_icon="🧠",
        layout="centered",
    )

    df = load_data()
    init_session_state()

    # MBTI 타입 목록 (Country 열 제외)
    mbti_types = df.columns.tolist()[1:]

    # -------------
    # 사이드바 설정
    # -------------
    st.sidebar.title("⚙️ 게임 설정")
    mbti_choice = st.sidebar.selectbox(
        "어떤 MBTI로 풀까요?",
        ["랜덤 선택"] + mbti_types,
    )

    if st.sidebar.button("새 게임 시작 🔄"):
        st.session_state.score = 0
        st.session_state.total = 0
        st.session_state.streak = 0
        st.session_state.question = None
        st.session_state.last_feedback = ""
        st.session_state.last_correct = None

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Tip**: 스트릭을 길게 이어서 최고 점수에 도전해 보세요! 🔥")

    # -------------
    # 상단 헤더 & 점수판
    # -------------
    st.title("🌍 MBTI 국가 맞추기 게임")
    st.caption("“이 MBTI가 제일 많은 나라는 어디일까?” 추리해 보는 데이터 퀴즈 🎮")

    col1, col2, col3 = st.columns(3)
    col1.metric("점수", f"{st.session_state.score}")
    col2.metric("문제 수", f"{st.session_state.total}")
    col3.metric("연속 정답(스트릭)", f"{st.session_state.streak} 🔥")

    if st.session_state.total > 0:
        st.progress(min(st.session_state.streak / 10, 1.0))

    st.markdown("---")

    # -------------
    # 문제 생성
    # -------------
    if st.session_state.question is None:
        # 이번 라운드 MBTI 선택
        if mbti_choice == "랜덤 선택":
            chosen_mbti = random.choice(mbti_types)
        else:
            chosen_mbti = mbti_choice

        st.session_state.selected_mbti = chosen_mbti
        st.session_state.question = make_question(df, chosen_mbti)

    q = st.session_state.question
    chosen_mbti = q["mbti"]

    # -------------
    # 문제 보여주기
    # -------------
    st.subheader(f"🧩 문제 {st.session_state.total + 1}번")

    st.markdown(
        f"""
**Q. `{chosen_mbti}` 유형이 가장 많은 나라는 어디일까요?**  
아래 4개 나라 중에서 골라 보세요! 🌟
"""
    )

    user_answer = st.radio(
        "정답이라고 생각하는 국가를 선택하세요 👇",
        q["options"],
        key=f"q_options_{st.session_state.total}",
    )

    if st.button("정답 제출 🚀"):
        st.session_state.total += 1
        correct = q["answer"]

        if user_answer == correct:
            st.session_state.score += 1
            st.session_state.streak += 1
            st.session_state.last_feedback = "정답입니다! 🎉 대단한데요?"
            st.session_state.last_correct = correct
            st.balloons()
        else:
            st.session_state.streak = 0
            st.session_state.last_feedback = (
                f"아쉽네요… 😅 정답은 **{correct}** 입니다."
            )
            st.session_state.last_correct = correct

        # 다음 문제 준비
        st.session_state.question = None

    # -------------
    # 피드백 및 부가 정보
    # -------------
    if st.session_state.last_feedback:
        st.markdown("---")
        st.markdown(f"### 📣 피드백")
        st.info(st.session_state.last_feedback)

        # 선택했던 MBTI에 대한 상위 국가 정보 간단히 보여주기
        if st.session_state.last_correct is not None:
            mbti_col = st.session_state.selected_mbti
            sorted_df = df.sort_values(by=mbti_col, ascending=False)
            top5 = sorted_df[["Country", mbti_col]].head(5)

            st.markdown(
                f"**📊 `{mbti_col}` 유형 비율 상위 5개 국가** (데이터 기준)"
            )
            st.dataframe(top5.reset_index(drop=True))


if __name__ == "__main__":
    main()
