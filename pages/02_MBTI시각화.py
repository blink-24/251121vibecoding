import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="MBTI 국가별 분포",
    page_icon="🌍",
    layout="wide",
)

@st.cache_data
def load_data():
    # 같은 폴더에 있는 CSV 파일을 읽어옵니다.
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()

st.title("🌍 MBTI 유형별 국가 분포 대시보드")
st.write("MBTI 유형을 선택하면, 해당 유형 비율이 **가장 높은 10개 국가**와 **가장 낮은 10개 국가**를 볼 수 있습니다.")

# MBTI 열 목록 추출 (Country 제외)
mbti_types = [col for col in df.columns if col != "Country"]

selected_type = st.selectbox(
    "🔎 MBTI 유형을 선택하세요",
    mbti_types,
    index=mbti_types.index("INFJ") if "INFJ" in mbti_types else 0
)

col_name = selected_type

# 선택한 MBTI 열만 사용
df_selected = df[["Country", col_name]].dropna()

# 상위 10개 국가
top10 = df_selected.sort_values(col_name, ascending=False).head(10)

# 하위 10개 국가
bottom10 = df_selected.sort_values(col_name, ascending=True).head(10)

# ===== 상위 10개 그래프 =====
st.subheader(f"📈 {col_name} 비율이 높은 국가 Top 10")

fig_top = px.bar(
    top10,
    x="Country",
    y=col_name,
    title=f"{col_name} 비율 상위 10개 국가",
    labels={"Country": "국가", col_name: "비율"},
)
fig_top.update_layout(
    xaxis_tickangle=-45,
    yaxis_tickformat=".1%"
)

st.plotly_chart(fig_top, use_container_width=True)

# 구분선
st.markdown("---")

# ===== 하위 10개 그래프 =====
st.subheader(f"📉 {col_name} 비율이 낮은 국가 Top 10")

fig_bottom = px.bar(
    bottom10,
    x="Country",
    y=col_name,
    title=f"{col_name} 비율 하위 10개 국가",
    labels={"Country": "국가", col_name: "비율"},
)
fig_bottom.update_layout(
    xaxis_tickangle=-45,
    yaxis_tickformat=".1%"
)

st.plotly_chart(fig_bottom, use_container_width=True)
