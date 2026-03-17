import streamlit as st
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="윤슬의 빛이 머무는 정원 v3.0", layout="wide")

# [보유 비료 리스트] - 실제 가지고 계신 제품들로 구성
MY_FERTS = [
    "마감프K (중소립)", "하이파 멀티코트 (6개월)", "아그로믹파워", 
    "잭스 프로페셔널 Bloom", "잭스 프로페셔널 Grow", 
    "하이파 멀티미크로 콤비", "골드아이언", "오스모코트", "벅스킹(살충제)"
]

# [식물 카테고리] - 가장 많이 키우시는 품종 위주
MY_PLANTS = ["스카푸", "사랑초(Oxalis)", "미니신닌기아", "베고니아", "네메시아", "금어초", "기타 파종이"]

if 'garden_log' not in st.session_state:
    st.session_state.garden_log = []

st.title("🌿 윤슬의 빛이 머무는 정원 v3.0")
st.info("📍 정남향 3층 베란다 (소나무 필터광 환경)")

col_input, col_guide = st.columns([2, 1])

with col_input:
    with st.form("main_form", clear_on_submit=True):
        st.subheader("📝 개체별 정식 및 관리 기록")
        
        c1, c2 = st.columns(2)
        with c1:
            category = st.selectbox("식물 종류", MY_PLANTS)
            name = st.text_input("상세 이름 (예: 스카푸 1호)", placeholder="개체명을 적어주세요.")
        with c2:
            stage = st.selectbox("단계", ["파종/발아", "정식(분갈이)", "성장기", "꽃봉오리", "개화", "방제/휴면"])
            
        st.write("💊 **영양제/방제 다중 선택**")
        selected_ferts = []
        f_cols = st.columns(3)
        for i, f in enumerate(MY_FERTS):
            if f_cols[i % 3].checkbox(f):
                selected_ferts.append(f)
        
        notes = st.text_area("메모 (개체별 독립 저장)", placeholder="이 아이만의 특징이나 흙 배합 등을 적어주세요.")
        
        if st.form_submit_button("기록 저장하기"):
            if name:
                new_entry = {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "category": category, "name": name, "stage": stage,
                    "ferts": selected_ferts, "notes": notes
                }
                st.session_state.garden_log.insert(0, new_entry)
                st.success(f"'{name}' 기록이 완료되었습니다!")

# 관리 일지 리스트
st.divider()
st.subheader("📋 우리집 정원 일지")
for entry in st.session_state.garden_log:
    with st.expander(f"{entry['date']} | [{entry['category']}] {entry['name']} - {entry['stage']}"):
        if entry['ferts']:
            st.write(f"**💉 처방:** {', '.join(entry['ferts'])}")
            # [지능형 꿀팁] - 환경 및 비료 맞춤형 가이드
            if "벅스킹(살충제)" in entry['ferts']:
                st.warning("⚠️ **강아지 주의:** 벅스킹 성분이 있으니 반려견이 흙을 만지지 않게 주의하세요!")
            if "정식" in entry['stage']:
                st.info("💡 **빛 관리:** 소나무 그늘이 있는 위치에서 2~3일간 안정기를 가져주세요.")
        st.write(f"**📝 메모:** {entry['notes']}")
        
        cal_date = (datetime.now() + timedelta(days=7)).strftime("%Y%m%dT090000Z")
        cal_url = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={entry['name']}+물체크&dates={cal_date}/{cal_date}"
        st.link_button("📅 7일 뒤 물주기 알람 추가", cal_url)

# [사이드바] - 윤슬님 전용 레시피 저장소
with col_guide:
    st.header("📚 우리집 레시피")
    with st.expander("🌱 스카푸 전용 (반에그먼트)", expanded=True):
        st.write("- 반에그먼트 상토: 500ml")
        st.write("- 야생화 흙: 400ml")
        st.write("- 훈탄: 100ml")
    with st.expander("🌸 일반 정식 (바로커 표준)"):
        st.write("- 바로커 상토: 700ml")
        st.write("- 야생화 흙: 200ml")
        st.write("- 훈탄: 100ml")
    with st.expander("⚖️ 비료 정량 (9cm 기준)"):
        st.write("- 마감프K: 1.5g")
        st.write("- 하이파 멀티코트: 20알")
        st.write("- 아그로믹파워: 1알 (가장자리)")
