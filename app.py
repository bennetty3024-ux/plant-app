import streamlit as st
import json
import os
from datetime import datetime, timedelta

DATA_FILE = "garden_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="윤슬의 정원 매니저 v8.7", layout="wide", page_icon="🌿")
st.title("🌿 윤슬의 정원 매니저 v8.7")
st.caption("자동 저장 | 시비 D-Day | 가든멈 국화 및 품종별 순집기 가이드")

if 'plants' not in st.session_state:
    st.session_state.plants = load_data()

tab1, tab2, tab3, tab4 = st.tabs(["🆕 새 식물 등록", "🪴 내 식물 관리", "📅 할 일 & 시비 알림", "🧪 표준 흙 레시피"])

# --- 탭 1: 새 식물 등록 ---
with tab1:
    st.subheader("새로운 식물 등록")
    with st.form("add_plant_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("식물 이름")
            species = st.selectbox("품종", ["사랑초(일반)", "사랑초(옵투사)", "베고니아", "미니 신닌기아", "스트렙토카르푸스", "아키메네스", "애기부용", "가든멈(국화)", "기타"])
        with col2:
            plant_date = st.date_input("식재일", datetime.now())
            fertilizer_type = st.selectbox("투입된 비료", ["하이파 멀티코트(6개월)", "오스모코트(3~4개월)", "마감프 K(1년)", "없음"])
        
        if st.form_submit_button("등록 및 자동 저장"):
            if name:
                new_plant = {"id": str(datetime.now().timestamp()), "name": name, "species": species, "date": str(plant_date), "fertilizer": fertilizer_type}
                st.session_state.plants.append(new_plant)
                save_data(st.session_state.plants)
                st.success(f"'{name}' 저장 완료!")

# --- 탭 3: 할 일 & 시비 알림 ---
with tab3:
    st.subheader("📅 맞춤형 케어 가이드")
    if not st.session_state.plants:
        st.info("식물을 등록하면 관리 일정이 생성됩니다.")
    else:
        for plant in st.session_state.plants:
            st.markdown(f"#### **[{plant['name']}]**")
            p_date = datetime.strptime(plant['date'], '%Y-%m-%d')
            days_passed = (datetime.now() - p_date).days
            sp = plant['species']

            # 1. 가든멈 국화 특화 로직
            if sp == "가든멈(국화)":
                current_month = datetime.now().month
                if current_month < 7 or (current_month == 7 and datetime.now().day <= 15):
                    st.success("✂️ **순집기 집중기:** 줄기가 10cm 정도 자랄 때마다 끝순을 따주세요. 가지가 많아질수록 가을에 꽃폭탄을 봅니다!")
                else:
                    st.error("⚠️ **순집기 종료:** 지금부터는 순집기를 멈춰야 꽃눈이 형성됩니다. 지금 따면 꽃을 못 볼 수 있어요!")
                st.info("💧 **영양:** 꽃봉오리가 보이기 시작하면 '잭스 블룸'을 10일 간격으로 관수하세요.")

            # 2. 애기부용 토피어리 로직
            elif sp == "애기부용":
                st.warning("✂️ **수형 관리:** 20cm 토피어리 목표! 외목대 곁순은 수시로 제거하고, 정점 순집기로 머리를 풍성하게 만드세요.")

            # 3. 아키메네스 로직
            elif sp == "아키메네스":
                if days_passed < 60:
                    st.success("✂️ **순집기:** 초기 성장이 중요합니다. 2~3회 반복해서 풍성한 기본 골격을 만드세요.")
                else:
                    st.error("⚠️ **순집기 마감:** 이제 꽃눈이 나올 차례입니다. 순집기를 중단하세요.")

            # 4. 비료 D-Day
            f_type = plant.get('fertilizer', '없음')
            if "하이파" in f_type:
                st.write(f"🔹 **비료:** 하이파 재투입까지 {180 - days_passed}일 남음")
            elif "오스모코트" in f_type:
                st.write(f"🔹 **비료:** 오스모코트 재투입까지 {100 - days_passed}일 남음")
            st.divider()

# --- 탭 4: 표준 흙 레시피 ---
with tab4:
    st.subheader("🧪 10리터 기준 정밀 배합표")
    recipe = st.radio("식물군 선택", ["사랑초(일반)", "사랑초(옵투사)", "베고니아/신닌기아", "국화/기타"])
    if recipe == "국화/기타":
        st.markdown("### 🌼 국화/일반 식물 (배수 중심)\n- **반에그먼트 상토:** 7L\n- **마사 또는 펄라이트:** 2L\n- **훈탄:** 1L\n- **영양:** 하이파 멀티코트 30g")
    else:
        st.write("상단 메뉴에서 다른 배합표를 확인하세요.")
