import streamlit as st
import json
from datetime import datetime, timedelta

# 1. 설정 및 데이터 로드
st.set_page_config(page_title="윤슬의 정원 v7.7 통합본", layout="wide")
DATA_FILE = "garden_data.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"plants":[], "logs":[]}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.data, f, ensure_ascii=False)

if "data" not in st.session_state:
    st.session_state.data = load_data()

# 2. 카테고리 및 레시피 (윤슬님 7.7버전 그대로)
CATEGORIES = ["옵투사사랑초", "사랑초", "스카푸", "베고니아", "아키메네스", "구근류", "수국", "파종 식물", "가든멈국화", "미니신닌기아", "팬지/비올라"]
FERTS = ["마감프K", "멀티코트", "아그로믹파워", "잭스 Grow", "잭스 Bloom", "멀티미크로", "골드아이언", "토탈싹", "벅스킬"]
REAPPLY_DAYS = {"마감프K": 180, "멀티코트": 180, "아그로믹파워": 90, "잭스 Grow": 14, "잭스 Bloom": 14, "멀티미크로": 30, "골드아이언": 30, "토탈싹": 30, "벅스킬": 14}
POTS = {"5호": 0.3, "9호": 0.8, "10호": 1.0, "15호": 2.5}

RECIPES = {
    "옵투사사랑초": {"바로커": 650, "산야초": 250, "질석": 0, "훈탄": 100, "마감프K": 1.5, "멀티코트": 3, "아그로믹파워": 1, "토탈싹": 0.8},
    "사랑초": {"반에그먼트": 650, "산야초": 250, "질석": 0, "훈탄": 100, "마감프K": 1.5, "멀티코트": 3, "아그로믹파워": 1, "토탈싹": 0.8},
    "스카푸": {"반에그먼트": 400, "산야초": 300, "질석": 200, "훈탄": 100, "멀티코트": 2, "마감프K": 1, "아그로믹파워": 1, "토탈싹": 0.8},
    "베고니아": {"반에그먼트": 500, "산야초": 300, "질석": 100, "훈탄": 100, "멀티코트": 2, "아그로믹파워": 1, "토탈싹": 0.8},
    "아키메네스": {"반에그먼트": 450, "산야초": 250, "질석": 200, "훈탄": 100, "멀티코트": 3, "아그로믹파워": 1, "토탈싹": 0.8},
    "미니신닌기아": {"반에그먼트": 400, "산야초": 250, "질석": 250, "훈탄": 100, "멀티코트": 3, "아그로믹파워": 1, "토탈싹": 0.8},
    "구근류": {"반에그먼트": 550, "산야초": 300, "질석": 50, "훈탄": 100, "멀티코트": 2, "토탈싹": 0.8},
    "수국": {"반에그먼트": 600, "산야초": 300, "질석": 0, "훈탄": 100, "멀티코트": 3, "아그로믹파워": 1, "토탈싹": 0.8},
    "가든멈국화": {"반에그먼트": 600, "산야초": 300, "질석": 0, "훈탄": 100, "멀티코트": 3, "아그로믹파워": 1, "토탈싹": 0.8}
}

st.title("🌿 윤슬의 정원 매니저 v7.7 통합")

tabs = st.tabs(["🏠 홈", "📋 할 일", "🪴 식물관리", "💊 영양제기록", "⚖️ 분갈이계산기", "🧪 흙배합"])

# --- 홈 & 할 일 ---
with tabs[0]:
    st.metric("총 식물 수", len(st.session_state.data["plants"]))

with tabs[1]:
    st.subheader("📋 순집기 및 시비 알림")
    month = datetime.now().month
    if month <= 7:
        st.info("🌼 **가든멈 국화:** 7월 중순까지 순집기를 반복해야 가을에 풍성해집니다!")
    else:
        st.warning("⚠️ **가든멈 국화:** 이제 순집기를 멈춰야 꽃눈이 생깁니다.")
    
    # 영양제 D-Day 알림 로직 (7.7 기반)
    today = datetime.now()
    for log in st.session_state.data.get("logs", []):
        log_date = datetime.strptime(log["date"], "%Y-%m-%d")
        for fert in log.get("fert", []):
            if fert in REAPPLY_DAYS:
                next_date = log_date + timedelta(days=REAPPLY_DAYS[fert])
                if next_date <= today:
                    st.warning(f"**{log['plant']}** : {fert} 재투입 필요!")

# --- 식물관리 & 영양제기록 ---
with tabs[2]:
    st.subheader("식물 추가")
    c1, c2 = st.columns(2)
    with c1: category = st.selectbox("품종", CATEGORIES)
    with c2: name = st.text_input("이름")
    if st.button("추가") and name:
        st.session_state.data["plants"].append({"name": name, "category": category})
        save_data(); st.rerun()

with tabs[3]:
    st.subheader("영양제 기록")
    if st.session_state.data["plants"]:
        plant_list = [p["name"] for p in st.session_state.data["plants"]]
        sel_plant = st.selectbox("대상 식물", plant_list)
        sel_fert = st.multiselect("투입 약제/비료", FERTS)
        if st.button("기록 저장"):
            log = {"date": today.strftime("%Y-%m-%d"), "plant": sel_plant, "fert": sel_fert}
            st.session_state.data["logs"].append(log)
            save_data(); st.success("저장되었습니다.")

# --- 분갈이 계산기 (윤슬님이 찾으시던 것!) ---
with tabs[4]:
    st.subheader("⚖️ 분갈이 흙 양 계산")
    c_p = st.selectbox("식물 종류 선택", list(RECIPES.keys()))
    c_h = st.selectbox("화분 크기", list(POTS.keys()))
    num = st.number_input("화분 개수", 1, 100)
    if st.button("계산하기"):
        vol = POTS[c_h] * num
        st.success(f"필요한 총 흙의 양: {vol:.1f} L")
        for k, v in RECIPES[c_p].items():
            if k in ["반에그먼트", "바로커", "산야초", "질석", "훈탄"]:
                st.write(f"📍 {k}: {v*vol/1000:.2f} L")
            else:
                st.write(f"💊 {k}: {v*vol:.1f} g")

with tabs[5]:
    st.subheader("🧪 1L 기준 표준 배합비")
    s_p = st.selectbox("레시피 확인", list(RECIPES.keys()), key="recipe_sel")
    for k, v in RECIPES[s_p].items():
        unit = "ml" if k in ["반에그먼트", "바로커", "산야초", "질석", "훈탄"] else "g"
        st.write(f"{k} : {v} {unit}")
