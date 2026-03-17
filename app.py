import streamlit as st
from datetime import datetime, timedelta

# 1. 페이지 설정
st.set_page_config(page_title="윤슬의 빛이 머무는 정원 v3.0", layout="wide")

# [데이터 복구] 보유 비료 및 식물 리스트
MY_FERTS = ["마감프K", "하이파 멀티코트", "아그로믹파워", "잭스 프로페셔널 Bloom", "잭스 프로페셔널 Grow", "하이파 멀티미크로 콤비", "골드아이언", "오스모코트", "벅스킹(살충제)"]
MY_PLANTS = ["스카푸", "사랑초(Oxalis)", "미니신닌기아", "베고니아", "네메시아", "데모루", "기타 파종이"]

# 기록 저장소 초기화
if 'garden_log' not in st.session_state:
    st.session_state.garden_log = []

st.title("🌿 윤슬의 빛이 머무는 정원 v3.0")
st.info("📍 정남향 3층 베란다 환경 맞춤형 매니저")

# 메인 레이아웃 (좌측: 입력 / 우측: 실시간 가이드 및 레시피)
col_input, col_guide = st.columns([2, 1])

with col_input:
    with st.form("main_form", clear_on_submit=True):
        st.subheader("📝 식물 관리 및 정식 기록")
        
        c1, c2 = st.columns(2)
        with c1:
            category = st.selectbox("식물 종류", MY_PLANTS)
            name = st.text_input("상세 이름 (예: 스카푸 1호)", placeholder="개체명을 입력하세요.")
        with c2:
            stage = st.selectbox("현재 단계", ["파종/발아", "정식(분갈이)", "성장기", "꽃봉오리", "개화", "방제/휴면"])
            
        st.write("💊 **영양제/방제 선택 (다중 선택 가능)**")
        selected_ferts = []
        f_cols = st.columns(3)
        for i, f in enumerate(MY_FERTS):
            if f_cols[i % 3].checkbox(f):
                selected_ferts.append(f)
        
        notes = st.text_area("메모 (개체별 독립 기록)", placeholder="흙 배합이나 특이사항을 적어주세요.")
        
        submitted = st.form_submit_button("🌱 정원 일지에 기록 저장")
        
        if submitted:
            if name:
                # [추천 로직] 날짜 계산
                now = datetime.now()
                # 물주기: 남향 베란다/소나무 그늘 감안하여 약 5일 뒤 추천
                water_day = (now + timedelta(days=5)).strftime("%m월 %d일")
                # 비료 재투여: 대부분의 비료가 3~6개월이므로 90일 뒤 추천
                fermet_day = (now + timedelta(days=90)).strftime("%Y년 %m월")
                # 가지치기: 성장기/개화 후 약 30일 뒤 체크
                pruning_day = (now + timedelta(days=30)).strftime("%m월 %d일")

                new_entry = {
                    "date": now.strftime("%Y-%m-%d %H:%M"),
                    "category": category, "name": name, "stage": stage,
                    "ferts": selected_ferts, "notes": notes,
                    "recommends": {
                        "water": water_day, "fermet": fermet_day, "pruning": pruning_day
                    }
                }
                st.session_state.garden_log.insert(0, new_entry)
                st.success(f"'{name}' 기록이 아래 일지에 저장되었습니다!")
            else:
                st.error("식물 이름을 적어주셔야 기록이 됩니다!")

# 하단 리스트: 저장된 기록이 보이는 곳
st.divider()
st.subheader("📋 우리집 정원 일지 (저장된 기록)")
if not st.session_state.garden_log:
    st.write("아직 저장된 기록이 없습니다.")
else:
    for entry in st.session_state.garden_log:
        with st.expander(f"✅ {entry['date']} | [{entry['category']}] {entry['name']} - {entry['stage']}", expanded=True):
            col_info, col_rec = st.columns([1, 1])
            with col_info:
                st.write(f"**💊 투입 영양제:** {', '.join(entry['ferts']) if entry['ferts'] else '없음'}")
                st.write(f"**📝 개별 메모:** {entry['notes']}")
                if "벅스킹(살충제)" in entry['ferts']:
                    st.warning("⚠️ **강아지 주의:** 벅스킹을 사용했습니다. 반려견이 닿지 않게 해주세요!")
            
            with col_rec:
                st.markdown(f"""
                **📢 다음 관리 추천 시기**
                - 💧 **다음 물주는 날:** 약 {entry['recommends']['water']} 경
                - ✂️ **가지치기 체크:** {entry['recommends']['pruning']} 경
                - 💉 **영양제 재투여:** {entry['recommends']['fermet']} 경
                """)
                # 구글 캘린더 연동
                cal_date = (datetime.now() + timedelta(days=7)).strftime("%Y%m%dT090000Z")
                cal_url = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={entry['name']}+물체크&dates={cal_date}/{cal_date}"
                st.link_button("📅 구글 캘린더 알람 예약", cal_url)

# 사이드바 가이드 (2.0 레시피 완벽 복구)
with col_guide:
    st.header("📚 우리집 레시피")
    with st.expander("🌱 스카푸 전용 (반에그먼트)", expanded=True):
        st.write("1L 기준: 반에그 500ml : 야생화흙 400ml : 훈탄 100ml")
    with st.expander("🌸 일반 정식 (바로커 표준)"):
        st.write("1L 기준: 바로커 700ml : 야생화흙 200ml : 훈탄 100ml")
    with st.expander("⚖️ 비료 정량 (9cm 화분)"):
        st.write("- 마감프K: 1.5g / 멀티코트: 20알")
        st.write("- 벅스킹: 1g / 아그로믹파워: 1알")
