import streamlit as st
from datetime import datetime, timedelta

# 상단 흙 배합 고정 메모
SOIL_MEMO = """
📏 **표준 흙 배합 (1리터 기준)**
* 반에그먼트 흙: 600ml
* 야생화초 흙: 300ml
* 훈탄: 100ml
* 마감프K(중소립): 2g
"""

st.set_page_config(page_title="식물 집사 앱", page_icon="🌿")
st.title("🌿 식물 돌보기 매니저")

with st.expander("📋 한눈에 보는 흙 배합 메모", expanded=True):
    st.markdown(SOIL_MEMO)

category = st.selectbox("🌱 관리할 식물", 
    ["미니신닌기아", "동형종 사랑초", "옵투사 사랑초", "가든멈국화", "베고니아", "데모루", "일본수국", "팬지비올라"])

repot_date = st.date_input("📅 분갈이 한 날짜", datetime.now())

if st.button("🚀 일정 자동 생성"):
    st.success(f"{category}의 일정이 등록되었습니다!")
    
    # 기본 2주 뒤 영양제, 4주 뒤 가지치기 설정 (식물별 커스텀 가능)
    fert_next = repot_date + timedelta(days=14)
    prune_next = repot_date + timedelta(days=30)
    
    col1, col2 = st.columns(2)
    col1.info(f"📅 **영양제 시기**\n\n{fert_next}")
    col2.error(f"✂️ **가지치기 시기**\n\n{prune_next}")

st.divider()
st.caption("2026 식물 집사 전용 앱")
