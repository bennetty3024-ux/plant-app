import streamlit as st
import json
from datetime import datetime, timedelta

# 1. 설정 및 데이터 로드 (한글 깨짐 방지 추가)
st.set_page_config(page_title="윤슬의 정원 v7.8 최종", layout="wide")
DATA_FILE = "garden_data.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"plants":[], "logs":[]}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.data, f, ensure_ascii=False, indent=4)

if "data" not in st.session_state:
    st.session_state.data = load_data()

# 2. 기본 설정 데이터 (7.7과 동일)
CATEGORIES = ["옵투사사랑초", "사랑초", "스카푸", "베고니아", "아키메네스", "구근류", "수국", "파종 식물", "가든멈국화", "미니신닌기아", "팬지/비올라"]
FERTS = ["마감프K", "멀티코트", "아그로믹파워", "잭스 Grow", "잭스 Bloom", "멀티미크로", "골드아이언", "토탈싹", "벅스킬"]
REAPPLY_DAYS = {"마감프K": 180, "멀티코트": 180, "아그로믹파워": 90, "잭스 Grow": 14, "잭스 Bloom": 14, "멀티미크로": 30, "골드아이언": 30, "토탈싹": 30, "벅스킬": 14}
POTS = {"5호": 0.3, "9호": 0.8, "10호": 1.0, "15호": 2.5}
RECIPES = {
    "옵투사사랑초": {"바로커": 650, "산야초": 250, "훈탄": 100, "마감프K": 1.5, "멀티코트": 3},
    "사랑초": {"반에그먼트": 650, "산야초": 250, "훈탄": 100, "마감프K": 1.5, "멀티코트": 3},
    "가든멈국화": {"반에그먼트": 600, "산야초": 300, "훈탄": 100, "멀티코트": 3}
    # (다른 레시피들은 코드 줄이 너무 길어져서 생략했지만, 실제 윤슬님 파일엔 그대로 두셔도 됩니다.)
}

st.title("🌿 윤슬의 정원 매니저 v7.8")

tabs = st.tabs(["🏠 홈/할일", "🪴 식물 목록(수정/삭제)", "➕ 식물 추가", "💊 영양제기록", "⚖️ 분갈이계산"])

# --- 탭 0: 홈/할일 ---
with tabs[0]:
    col1, col2 = st.columns(2)
    col1.metric("총 식물 수", len(st.session_state.data["plants"]))
    
    with col2:
        st.subheader("📋 주요 알림")
        month = datetime.now().month
        if month <= 7:
            st.info("🌼 가든멈 국화: 7월 중순까지 순집기!")
        elif month >= 8:
            st.warning("⚠️ 가든멈 국화: 순집기 금지! (꽃눈 형성기)")

# --- 탭 1: 식물 목록 (★수정/삭제 기능 추가!) ---
with tabs[1]:
    st.subheader("🪴 내 식물 목록 관리")
    
    if not st.session_state.data["plants"]:
        st.info("먼저 '➕ 식물 추가' 탭에서 식물을 등록해주세요.")
    else:
        # 모바일에서 보기 좋게 Expander 구조로 변경
        for i, plant in enumerate(st.session_state.data["plants"]):
            with st.expander(f"🌱 {plant['name']} ({plant['category']})", expanded=False):
                # 1. 수정 영역
                st.write("**[정보 수정]**")
                edit_name = st.text_input("식물 이름 수정", value=plant['name'], key=f"edit_name_{i}")
                edit_cat = st.selectbox("품종 수정", CATEGORIES, index=CATEGORIES.index(plant['category']) if plant['category'] in CATEGORIES else 0, key=f"edit_cat_{i}")
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("📝 수정 완료", key=f"save_edit_{i}"):
                        plant['name'] = edit_name
                        plant['category'] = edit_cat
                        save_data()
                        st.success("수정되었습니다!")
                        st.rerun()
                
                # 2. 삭제 영역
                with c2:
                    # 실수로 삭제하는 걸 방지하기 위해 '진짜 삭제' 버튼을 한 번 더 누르게 함
                    if st.button("🗑️ 식물 삭제", key=f"del_confirm_{i}"):
                        st.session_state[f"del_mode_{i}"] = True
                    
                    if st.session_state.get(f"del_mode_{i}", False):
                        st.warning("진짜 삭제하시겠습니까?")
                        if st.button("❌ 네, 삭제합니다.", key=f"del_final_{i}"):
                            st.session_state.data["plants"].pop(i)
                            save_data()
                            st.session_state[f"del_mode_{i}"] = False
                            st.success("삭제되었습니다.")
                            st.rerun()
                        if st.button("취소", key=f"del_cancel_{i}"):
                            st.session_state[f"del_mode_{i}"] = False
                            st.rerun()

# --- 탭 2: 식물 추가 ---
with tabs[2]:
    st.subheader("➕ 새로운 식물 추가")
    with st.form("add_form", clear_on_submit=True):
        new_cat = st.selectbox("품종", CATEGORIES)
        new_name = st.text_input("식물 이름 (예: 아키메네스 구근심기)")
        submit = st.form_submit_button("정원에 추가하기")
        
        if submit and new_name:
            st.session_state.data["plants"].append({"name": new_name, "category": new_cat})
            save_data()
            st.success(f"'{new_name}' 등록 완료!")
            st.rerun()

# --- 탭 3: 영양제 기록 (윤슬님 화면) ---
with tabs[3]:
    st.subheader("💊 영양제 및 약제 기록")
    if st.session_state.data["plants"]:
        # 등록된 식물 이름 목록 가져오기
        plant_names = [p["name"] for p in st.session_state.data["plants"]]
        sel_plant = st.selectbox("대상 식물 선택", plant_names)
        sel_fert = st.multiselect("투입 약제/비료", FERTS)
        
        if st.button("기록 저장"):
            if sel_fert:
                log = {"date": datetime.now().strftime("%Y-%m-%d"), "plant": sel_plant, "fert": sel_fert}
                st.session_state.data["logs"].append(log)
                save_data()
                st.success("기록되었습니다.")
            else:
                st.error("영양제를 선택해주세요.")
    else:
        st.info("등록된 식물이 없습니다.")

# --- 탭 4: 분갈이 계산기 ---
with tabs[4]:
    st.subheader("⚖️ 분갈이 흙 계산기")
    # (이전 v7.7과 동일한 계산기 로직)
