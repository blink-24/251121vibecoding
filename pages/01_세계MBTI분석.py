import streamlit as st
import pandas as pd
import altair as alt

# 데이터 불러오기
@st.cache_data
def load_data():
    # 같은 폴더에 있는 CSV 파일 이름
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()

# ----------------- 페이지 기본 설정 -----------------
st.set_page_config(
    page_title="MBTI별 국가 분포",
    layout="centered"
)

st.title("🌍 MBTI 유형별 국가 분포 대시보드")
st.markdown(
    """
MBTI 유형을 선택하면,  
해당 유형 비율이 **가장 높은 10개 나라**와 **가장 낮은 10개 나라**를  
Altair 기반 **인터랙티브 막대 그래프**로 보여줍니다.
"""
)

# ----------------- MBTI 선택 UI -----------------
mbti_types = [col for col in df.columns if col != "Country"]
default_index = mbti_types.index("INFJ") if "INFJ" in mbti_types else 0

selected_mbti = st.selectbox(
    "MBTI 유형을 선택하세요",
    mbti_types,
    index=default_index
)

# ----------------- 상·하위 10개국 계산 -----------------
# 선택한 MBTI 비율 기준으로 상위 10개 / 하위 10개 추출
top10 = df.nlargest(10, selected_mbti).copy()
bottom10 = df.nsmallest(10, selected_mbti).copy()

# 보기 좋게 오름차순 정렬 (막대가 아래로 갈수록 커지도록)
top10 = top10.sort_values(selected_mbti, ascending=True)
bottom10 = bottom10.sort_values(selected_mbti, ascending=True)

# 퍼센트(%) 보기 좋게 변환
top10["ratio_pct"] = top10[selected_mbti] * 100
bottom10["ratio_pct"] = bottom10[selected_mbti] * 100

# ----------------- Altair 그래프: 상위 10개국 -----------------
st.subheader(f"🔺 {selected_mbti} 비율이 높은 상위 10개 국가")

chart_top = (
    alt.Chart(top10)
    .mark_bar()
    .encode(
        x=alt.X(
            "ratio_pct:Q",
            title=f"{selected_mbti} 비율(%)"
        ),
        y=alt.Y(
            "Country:N",
            sort="-x",
            title="국가"
        ),
        tooltip=[
            alt.Tooltip("Country:N", title="국가"),
            alt.Tooltip("ratio_pct:Q", title="비율(%)", format=".2f")
        ]
    )
    .properties(
        height=400
    )
    .interactive()
)

st.altair_chart(chart_top, use_container_width=True)

# ----------------- Altair 그래프: 하위 10개국 -----------------
st.subheader(f"🔻 {selected_mbti} 비율이 낮은 하위 10개 국가")

chart_bottom = (
    alt.Chart(bottom10)
    .mark_bar()
    .encode(
        x=alt.X(
            "ratio_pct:Q",
            title=f"{selected_mbti} 비율(%)"
        ),
        y=alt.Y(
            "Country:N",
            sort="-x",
            title="국가"
        ),
        tooltip=[
            alt.Tooltip("Country:N", title="국가"),
            alt.Tooltip("ratio_pct:Q", title="비율(%)", format=".2f")
        ]
    )
    .properties(
        height=400
    )
    .interactive()
)

st.altair_chart(chart_bottom, use_container_width=True)
