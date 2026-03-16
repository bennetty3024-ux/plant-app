import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="나만의 정원 매니저", page_icon="🌿", layout="wide")

st.title("🌿 나만의 베란다 정원 매니저")

# 1. 고정 메모: 환경 및 흙 배합 가이드
with st.expander("📋 우리집 맞춤 흙 배합 & 환경 가이드 (터치해서 열기/닫기)", expanded=False):
    st.markdown("""
    **🏡 베란다 환경 참고:**
    * 남향 3층, 소나무 그늘로 인한 반양지. 해가 완전히 다 들지 않으므로 과습 주의 및 통풍 철저!

    **📏 기본 흙 배합 (1리터 기준)**
    * 반에그먼트 흙: 600ml
    * 야생화초 흙: 300ml
    * 훈탄: 100ml
    * 마감프K(중소립): 2g

    **🌸 사랑초 전용 흙 배합 (1리터 기준)**
    * 바로커 흙: 600ml
    * 야생화초 흙: 300ml
    * 훈탄: 100ml
    * 마감프K(중소립): 2g
    """)

# 2. 관리할 식물 및 영양제 리스트 데이터
PLANTS = [
    "미니신닌기아", "베고니아", "사랑초 (동형/옵투사)", "스트렙토카르푸스", 
    "파종 모종 (금어초, 네메시아, 데모루 등)", "가든멈국화", 
    "일본수국 (치쿠노카제, 미카노미즈토세 등)", "애기부용", "구근류 (튤립 등)", "기타"
]

FERTILIZERS = [
    "주지 않음 (물만 줌)",
    "잭스 프로페셔널 그로우",
    "잭스 프로페셔널 블룸",
    "하이파 멀티-마이크로 콤비",
    "하이파 멀티코트 (6개월)",
    "마감프K (중소립)",
    "골드 아이언",
    "오스모코트 (3-4개월)"
]

st.divider()

# 3. 식물 관리 기록 입력 섹션
st.subheader("📝 오늘의 식물 관리 기록")

col1, col2 = st.columns(2)
with col1:
    category = st.selectbox("🌱 식물 종류", PLANTS)
    plant_name = st.text_input("🏷️ 개체 이름 (예: 애플블라썸 금어초 1호, 20cm 토피어리 애기부용)")
    action_date = st.date_input("📅 관리 날짜", datetime.now())

with col2:
    action_type = st.selectbox("🛠️ 관리 내용", ["분갈이/가식", "파종", "가지치기/순지르기", "물/영양제 주기", "구근 수확", "잎꽂이/삽목"])
    selected_fert = st.selectbox("💊 사용한 비료/영양제", FERTILIZERS)
    fert_amount = st.text_input("💧 정확한 사용량 (예: 물 1리터에 1g, 화분 위 1티스푼)")

notes = st.text_area("✍️ 특이사항 메모 (예: 본잎이 3쌍 나옴, 뿌리가 화분에 꽉 참)")

# 4. 스마트 일정 계산 및 알람
if st.button("🚀 기록 저장 및 다음 일정 자동 계산"):
    st.success(f"'{plant_name if plant_name else category}'의 관리가 기록되었습니다!")
    
    st.subheader("💡 다음 관리 추천 일정 & 팁")
    
    # 알람 날짜 계산
    next_water = action_date + timedelta(days=5) # 보수적인 흙 마름 확인일
    next_fert = action_date + timedelta(days=14)
    
    c1, c2, c3 = st.columns(3)
    
    # 관수 알람
    c1.info(f"💧 **흙 마름 확인**\n\n{next_water.strftime('%Y-%m-%d')} 경\n\n(반양지 환경이므로 겉흙이 충분히 말랐는지 확인 후 관수하세요.)")
    
    # 영양제 알람 (알비료와 액비 구분)
    if selected_fert != "주지 않음 (물만 줌)" and "코트" not in selected_fert and "마감프" not in selected_fert:
        c2.warning(f"💊 **다음 액비 투여**\n\n{next_fert.strftime('%Y-%m-%d')} 경\n\n(식물 상태를 보고 농도를 조절하세요.)")
    else:
        c2.warning("💊 **알비료 효과 지속 중**\n\n(서서히 녹는 비료가 적용 중입니다. 과비료에 주의하세요.)")
        
    # 식물별 맞춤 팁 자동 생성
    tip = ""
    if category == "미니신닌기아" and action_type == "분갈이/가식":
        tip = "새 촉이 올라올 때 액비(잭스 그로우)를 연하게 타서 주면 성장에 매우 좋습니다."
    elif category == "사랑초 (동형/옵투사)":
        tip = "가을 파종 후 싹이 틀 때 골드 아이언을 챙겨주시면 잎 색이 선명해지고 구근 성장에 큰 도움이 됩니다."
    elif "파종" in category and action_type == "분갈이/가식":
        tip = "새 흙에 뿌리가 자리 잡을 수 있도록 2~3일은 강광을 피해주세요. 안정이 되면 순지르기를 통해 곁가지를 풍성하게 유도하세요."
    elif category == "애기부용":
        tip = "목표하시는 20cm 토피어리 수형을 잡기 위해 아래쪽 곁가지는 수시로 다듬고, 꼭대기 생장점만 남겨 위로 키워주세요."
    elif category == "스트렙토카르푸스" and action_type == "잎꽂이/삽목":
        tip = "새순이 어느 정도 자라면 무름병 방지를 위해 흙 배수가 잘 되는 화분으로 정식해 주세요."
    elif category == "가든멈국화":
        tip = "가을에 풍성한 꽃을 보려면 늦여름(8월 말)부터 개화촉진제(잭스 블룸)를 투여하는 것이 좋습니다."
    else:
        tip = "소나무 그늘로 인해 일조량이 부족할 수 있으니, 각 식물 특성에 맞춰 가장 해가 잘 드는 명당 자리를 찾아주세요!"
        
    c3.error(f"✨ **스마트 케어 팁**\n\n{tip}")

st.divider()
st.caption("2026 베란다 정원 스마트 매니저 v2.0")

