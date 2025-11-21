 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/main.py b/main.py
index fd087aac373056996d40e60ed8d354d7c2c2fd73..95ee1b99abd8aa6ab2b33d3ba0db93df616d3868 100644
--- a/main.py
+++ b/main.py
@@ -1,4 +1,83 @@
 import streamlit as st
-st.title('나의 첫 웹앱!')
-st.write('☆Hello World☆')
-st.write('251121 Vibecoding Project')
+
+st.set_page_config(
+    page_title="MBTI 진로 상담실",
+    page_icon="🎓",
+    layout="centered",
+)
+
+st.title("🎨 MBTI 진로 아틀리에")
+st.caption("학생의 성향에 딱 맞는 진로를 3가지씩 추천해주는 미니 상담실 ✨")
+
+st.markdown(
+    """
+    당신의 성향을 선택하면, 맞춤형 진로 아이디어가 눈앞에 펼쳐집니다.
+    부담 없이 눌러보고, 마음에 드는 꿈을 찾아보세요! 💫
+    """
+)
+
+mbti_options = [
+    "ISTJ", "ISFJ", "INFJ", "INTJ",
+    "ISTP", "ISFP", "INFP", "INTP",
+    "ESTP", "ESFP", "ENFP", "ENTP",
+    "ESTJ", "ESFJ", "ENFJ", "ENTJ",
+]
+
+career_map = {
+    "ISTJ": ["📊 회계사", "🏛️ 공무원", "🛠️ 품질관리 엔지니어"],
+    "ISFJ": ["👩‍⚕️ 간호사", "🏫 초등 교사", "🎭 예술 행정가"],
+    "INFJ": ["🧭 상담가", "📖 작가", "🌿 사회혁신 기획자"],
+    "INTJ": ["🛰️ 데이터 사이언티스트", "🏗️ 도시 계획가", "🧪 연구원"],
+    "ISTP": ["🔧 메카닉", "🚁 드론 파일럿", "🧱 건축 기술자"],
+    "ISFP": ["🎨 그래픽 디자이너", "🎵 음악 프로듀서", "🌱 플로리스트"],
+    "INFP": ["📚 소설가", "🕊️ NGO 활동가", "🎬 시나리오 작가"],
+    "INTP": ["🧩 알고리즘 엔지니어", "🔬 연구 분석가", "📐 UX 리서처"],
+    "ESTP": ["🚀 스타트업 마케터", "🏟️ 스포츠 에이전트", "🛰️ 현장 기술 컨설턴트"],
+    "ESFP": ["🎤 MC/아나운서", "💄 뷰티 크리에이터", "🎪 이벤트 플래너"],
+    "ENFP": ["🌈 브랜드 디자이너", "🌍 글로벌 봉사 코디네이터", "🎥 영상 콘텐츠 디렉터"],
+    "ENTP": ["🧠 전략 컨설턴트", "🤝 벤처 캐피털리스트", "📰 미디어 기획자"],
+    "ESTJ": ["🏢 프로젝트 매니저", "⚖️ 법률 사무관", "🚚 물류 운영 관리자"],
+    "ESFJ": ["🎓 교육 코디네이터", "🏥 병원 코디네이터", "🍽️ F&B 매니저"],
+    "ENFJ": ["🌟 커뮤니티 매니저", "🎬 프로듀서", "📢 PR 스페셜리스트"],
+    "ENTJ": ["💼 비즈니스 디렉터", "📈 투자 애널리스트", "🧭 조직 전략가"],
+}
+
+with st.container(border=True):
+    st.subheader("MBTI 선택하기")
+    selected_mbti = st.selectbox(
+        "나의 성향을 골라주세요",
+        options=mbti_options,
+        index=mbti_options.index("ENFP"),
+        help="16가지 MBTI 유형 중 하나를 선택해요",
+    )
+    st.write("✨ 선택한 유형:", f"**{selected_mbti}**")
+
+st.divider()
+
+st.subheader("추천 진로 3가지 💡")
+recommendations = career_map.get(selected_mbti, [])
+
+if recommendations:
+    cols = st.columns(3)
+    for col, career in zip(cols, recommendations):
+        with col:
+            st.markdown(
+                f"""
+                <div style='padding: 16px; border-radius: 14px; background: linear-gradient(135deg, #f7f9fc 0%, #eef2ff 100%); box-shadow: 0 8px 24px rgba(0,0,0,0.06);'>
+                    <h3 style='text-align:center; margin-bottom: 8px;'>{career}</h3>
+                    <p style='text-align:center; color:#4b5563;'>✨ 이 유형과 잘 맞는 진로예요.</p>
+                </div>
+                """,
+                unsafe_allow_html=True,
+            )
+else:
+    st.info("해당 MBTI에 대한 추천을 준비 중이에요! 😊")
+
+st.divider()
+
+st.markdown(
+    """
+    🧭 **Tip.** 진로를 고민할 때는 *흥미*, *가치관*, *강점*을 함께 생각해보세요. 
+    당신의 MBTI는 출발점일 뿐, 선택의 주인공은 언제나 당신입니다! 🚀
+    """
+)
 
EOF
)
