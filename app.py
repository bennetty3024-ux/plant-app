import streamlit as st
from datetime import datetime, timedelta

# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="나만의 정원 매니저 v3.0", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f4f9f4; }
    .stButton>button { background-color: #4caf50; color: white; width: 100%; border-radius: 8px; }
    .stExpander { background-color: white; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 나만의 정원 매니저 v3.0")
st.caption("윤슬님의 소중한 정원을 위한 통합 관리 시스템")

# 세션 상태 초기화
if 'plants' not in st.session_state:
    st.session_state.plants = []

# 2. 고정 데이터 (2.0 버전 카테고리 복구)
PLANT_TYPES = ["사랑초(Oxalis)", "미니신닌기아", "베고니아", "금어초", "네메시아", "데모루", "수국", "기타"]
FERTILIZERS = ["마감프K", "하이파 멀티코트", "아그로믹파워", "잭스 프로페셔널(Bloom)", "잭스 프로페셔널(Grow)", "벅스킹", "골드아이언", "오스모코트"]

# 3. 입력 섹션
with st.form("plant_form", clear_on_submit=True):
    st.subheader("📝 새 기록 등록")
    
    col1, col2 = st.columns(2)
    with col1:
        plant_type = st.selectbox("식물 종류", PLANT_TYPES)
        name = st.text_input("상세 이름/번호", placeholder="예: 스카푸 1호")
    with col2:
        stage = st.selectbox("현재 단계", ["파종/잎꽂이", "정식(분갈이)", "성장기", "개화기", "휴면기"])
    
    # 3.0 핵심: 정식(분갈이) 다중 선택 기능
    pot_info = ""
    selected_ferts = []
    if stage == "정식(분갈이)":
        st.info("💡 스카푸/사랑초 전용 흙 레시피를 참고하여 정식을 기록하세요.")
        pot_info = st.text_input("사용 흙 배합", placeholder="예: 반에그먼트 7 : 야생화흙 2 : 훈탄 1")
        
        st.write("💊 투입 영양제 및 방제 (다중 선택)")
        cols = st.columns(3)
        for i, f in enumerate(FERTILIZERS):
            if cols[i % 3].checkbox(f):
                selected_ferts.append(f)
                
    note = st.text_area("개체별 특이사항 (메모)", placeholder="이 아이만의 특별한 상태를 적어주세요. (개별 저장됩니다)")
    
    submitted = st.form_submit_button("정원 일지에 저장하기")
    
    if submitted:
        if name:
            new_entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "type": plant_type,
                "name": name,
                "stage": stage,
                "pot": pot_info,
                "ferts": selected_ferts,
                "note": note
            }
            st.session_state.plants.insert(0, new_entry)
            st.success(f"'{name}' 기록이 안전하게 저장되었습니다!")
        else:
            st.error("상세 이름을 입력해주세요!")

# 4. 관리 일지 및 지능형 가이드
st.divider()
st.subheader("📋 나의 가드닝 히스토리")

if not st.session_state.plants:
    st.write("아직 기록이 없습니다. 오늘 분갈이한 아이부터 등록해보세요!")
else:
    for p in st.session_state.plants:
        with st.expander(f"{p['date']} | [{p['type']}] {p['name']} - {p['stage']}"):
            if p['pot']: st.write(f"**🪴 흙 배합:** {p['pot']}")
            if p['ferts']: st.write(f"**💊 사용 비료:** {', '.join(p['ferts'])}")
            st.write(f"**📝 개별 메모:** {p['note']}")
            
            # 맞춤형 꿀팁 (3.0 버전 로직)
            if "벅스킹" in p['ferts']:
                st.warning("⚠️ [주의] 벅스킹 농약 성분이 포함됨. 강아지가 화분 근처에 가지 않도록 주의!")
            if "아그로믹파워" in p['ferts']:
                st.info("💡 아그로믹파워 알약은 뿌리에 직접 닿지 않게 가장자리에 잘 넣어주셨죠?")
            if "정식" in p['stage']:
                st.success("✨ 분갈이 후 2-3일은 밝은 그늘에서 적응시켜주는 것, 잊지 마세요!")
            
            # 구글 캘린더 연동
            next_date = (datetime.now() + timedelta(days=7)).strftime("%Y%m%dT090000Z")
            cal_url = f"https://calendar.google.com/calendar/render?action=TEMPLATE&text={p['name']}+상태확인&dates={next_date}/{next_date}&details={p['name']} 정식 후 일주일 경과!"
            st.link_button("📅 7일 뒤 물주기 알림 추가", cal_url)

# 5. 레시피 참고 (2.0 버전 가이드 복구)
with st.sidebar:
    st.header("📚 가드닝 레시피")
    st.markdown("""
    **[스카푸 전용 레시피]**
    - 반에그먼트 500ml
    - 야생화흙 400ml
    - 훈탄 100ml
    
    **[9cm 화분 정식 표준]**
    - 마감프K 1.5g
    - 멀티코트 20알
    - 벅스킹 1g
    """)
