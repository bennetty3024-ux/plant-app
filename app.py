import streamlit as st
from datetime import datetime, timedelta

# 1. 페이지 설정
st.set_page_config(page_title="윤슬의 정원 매니저 v3.1", layout="wide")

# [보유 비료 및 식물 통합 리스트]
MY_FERTS = ["마감프K", "하이파 멀티코트 (6개월)", "아그로믹파워", "잭스 프로페셔널 Bloom", "잭스 프로페셔널 Grow", "하이파 멀티미크로 콤비", "골드아이언", "오스모코트", "벅스킹(살충제)"]
MY_PLANTS = ["스카푸", "동형종 사랑초", "옵투사 사랑초", "미니신닌기아", "베고니아", "일본수국", "가든멈국화", "팬지/비올라", "네메시아", "금어초", "데모루", "기타 파종이"]

if 'garden_log' not in st.session_state:
    st.session_state.garden_log = []

st.title("🌿 윤슬의 빛이 머무는 정원 v3.1")
st.info("📍 정남향 3층 베란다 (소나무 필터광) 환경 맞춤형 통합 버전")

col_input, col_guide = st.columns([2, 1])

with col_input:
    with st.form("main_form", clear_on_submit=True):
        st.subheader("📝 관리 및 정식 기록")
        c1, c2 = st.columns(2)
        with c1:
            category = st.selectbox("식물 종류", MY_PLANTS)
            name = st.text_input("상세 이름", placeholder="예: 스카푸 1호, 미카의 물떼새 등")
        with c2:
            stage = st.selectbox("단계", ["파종/발아", "정식(분갈이)", "성장기", "꽃봉오리", "개화", "방제/휴면"])
            
        st.write("💊 **영양제/방제 선택 (다중 선택 가능)**")
        selected_ferts = []
        f_cols = st.columns(3)
        for i, f in enumerate(MY_FERTS):
            if f_cols[i % 3].checkbox(f):
                selected_ferts.append(f)
        
        notes = st.text_area("메모 (개체별 독립 기록)", placeholder="흙 배합이나 특이사항을 적어주세요.")
        
        if st.form_submit_button("🌱 정원 일지에 기록 저장"):
            if name:
                now = datetime.now()
                # [추천 로직] 수국은 물마름이 빠르므로 3일, 일반은 5일 기준
                water_days = 3 if category == "일본수국" else 5
                water_day = (now + timedelta(days=water_days)).strftime("%m월 %d일")
                fermet_day = (now + timedelta(days=90)).strftime("%Y년 %m월")
                pruning_day = (now + timedelta(days=30)).strftime("%m월 %d일")

                new_entry = {
                    "date": now.strftime("%Y-%m-%d %H:%M"),
                    "category": category, "name": name, "stage": stage,
                    "ferts": selected_ferts, "notes": notes,
                    "recommends": {"water": water_day, "fermet": fermet_day, "pruning": pruning_day}
                }
                st.session_state.garden_log.insert(0, new_entry)
                st.success(f"'{name}' 기록이 저장되었습니다!")

# 하단 일지 리스트
st.divider()
st.subheader("📋 우리집 정원 일지 (저장된 목록)")
for entry in st.session_state.garden_log:
    with st.expander(f"✅ {entry['date']} | [{entry['category']}] {entry['name']} - {entry['stage']}", expanded=True):
        col_info, col_rec = st.columns([1, 1])
        with col_info:
            st.write(f"**💊 투입:** {', '.join(entry['ferts']) if entry['ferts'] else '없음'}")
            st.write(f"**📝 메모:** {entry['notes']}")
            if "벅스킹(살충제)" in entry['ferts']:
                st.warning("⚠️ **강아지 주의:** 벅스킹 성분이 있으니 반려견 접근 금지!")
            if entry['category'] == "일본수국":
                st.info("💡 **수국 팁:** 7월 중순 이후 가지치기는 내년 꽃눈 형성을 방해하니 주의!")
        
        with col_rec:
            st.markdown(f"""
            **📢 다음 관리 추천 시기**
            - 💧 **물주기 체크:** 약 {entry['recommends']['water']} 경
            - ✂️ **가지치기 체크:** {entry['recommends']['pruning']} 경
            - 💉 **비료 재투여:** {entry['recommends']['fermet']} 경
            """)
            cal_url = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={entry['name']}+관리"
            st.link_button("📅 구글 알람 예약", cal_url)

# 사이드바 레시피 (완벽 복구)
with col_guide:
    st.header("📚 우리집 레시피")
    with st.expander("🌱 스카푸 전용 (반에그 5:4:1)", expanded=True):
        st.write("반에그 500ml : 야생화흙 400ml : 훈탄 100ml")
    with st.expander("🌸 수국/사랑초 (반에그 7:2:1)"):
        st.write("반에그 700ml : 야생화흙 200ml : 훈탄 100ml")
    with st.expander("⚖️ 비료 정량 (9cm 기준)"):
        st.write("마감프K 1.5g / 멀티코트 20알 / 벅스킹 1g")
