import streamlit as st
import sqlite3
from datetime import datetime

# 1. 설정 및 데이터베이스 초기화
st.set_page_config(page_title="윤슬의 정원 v7.8", layout="wide")
DB_FILE = "garden_data.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS plants
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, plant TEXT, fert TEXT)''')
    conn.commit()
    conn.close()

init_db()

# DB 데이터 로드 및 조작 함수
def load_plants():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name, category FROM plants")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "category": r[2]} for r in rows]

def add_plant(name, category):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO plants (name, category) VALUES (?, ?)", (name, category))
    conn.commit()
    conn.close()

def update_plant(plant_id, new_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE plants SET name=? WHERE id=?", (new_name, plant_id))
    conn.commit()
    conn.close()

def delete_plant(plant_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM plants WHERE id=?", (plant_id,))
    conn.commit()
    conn.close()

def add_log(date, plant, fert):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO logs (date, plant, fert) VALUES (?, ?, ?)", (date, plant, fert))
    conn.commit()
    conn.close()

# 2. 고정 데이터
CATEGORIES = ["옵투사사랑초", "사랑초", "스카푸", "베고니아", "아키메네스", "구근류", "수국", "파종 식물", "가든멈국화", "미니신닌기아", "팬지/비올라"]
# 오스모코트 추가 완료
FERTS = ["마감프K", "멀티코트", "오스모코트", "아그로믹파워", "잭스 Grow", "잭스 Bloom", "멀티미크로", "골드아이언", "토탈싹", "벅스킬"]
POTS = {"5호": 0.3, "9호": 0.8, "10호": 1.0, "15호": 2.5}

# 기존 레시피 유지
RECIPES = {
    "옵투사사랑초": {"바로커": 650, "산야초": 250, "훈탄": 100, "마감프K": 1.5, "멀티코트": 3, "아그로믹파워": 1, "토탈싹": 0.8},
    "사랑초": {"반에그먼트": 650, "산야초": 250, "훈탄": 100, "마감프K": 1.5, "멀티코트": 3, "아그로믹파워": 1, "토탈싹": 0.8},
    "스카푸": {"반에그먼트": 400, "산야초": 300, "질석": 200, "훈탄": 100, "멀티코트": 2, "마감프K": 1, "아그로믹파워": 1, "토탈싹": 0.8},
    "베고니아": {"반에그먼트": 500, "산야초": 300, "질석": 100, "훈탄": 100, "멀티코트": 2, "아그로믹파워": 1, "토탈싹": 0.8},
    "아키메네스": {"반에그먼트": 450, "산야초": 250, "질석": 200, "훈탄": 100, "멀티코트": 3, "아그로믹파워": 1, "토탈싹": 0.8},
    "미니신닌기아": {"반에그먼트": 400, "산야초": 250, "질석": 250, "훈탄": 100, "멀티코트": 3, "아그로믹파워": 1, "토탈싹": 0.8},
    "구근류": {"반에그먼트": 550, "산야초": 300, "질석": 50, "훈탄": 100, "멀티코트": 2, "토탈싹": 0.8},
    "수국": {"반에그먼트": 600, "산야초": 300, "질석": 0, "훈탄": 100, "멀티코트": 3, "아그로믹파워": 1, "토탈싹": 0.8},
    "가든멈국화": {"반에그먼트": 600, "산야초": 300, "질석": 0, "훈탄": 100, "멀티코트": 3, "아그로믹파워": 1, "토탈싹": 0.8}
}

st.title("🌿 윤슬의 정원 매니저 v7.8")

plants = load_plants()

tabs = st.tabs(["🏠 홈/할일", "🪴 식물 목록", "➕ 식물 추가", "💊 영양제기록", "⚖️ 분갈이계산"])

with tabs[0]:
    st.metric("총 식물 수", len(plants))
    month = datetime.now().month
    if month <= 7: st.info("🌼 가든멈 국화: 7월 중순까지 순집기!")

with tabs[1]:
    st.subheader("🪴 내 식물 목록 관리")
    for plant in plants:
        with st.expander(f"🌱 {plant['name']} ({plant['category']})"):
            new_n = st.text_input("이름 수정", plant['name'], key=f"n_{plant['id']}")
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("수정", key=f"e_{plant['id']}"):
                    update_plant(plant['id'], new_n)
                    st.rerun()
            with col2:
                if st.button("🗑️ 삭제", key=f"d_{plant['id']}"):
                    delete_plant(plant['id'])
                    st.rerun()

with tabs[2]:
    with st.form("add"):
        c = st.selectbox("품종", CATEGORIES)
        n = st.text_input("이름")
        if st.form_submit_button("추가") and n:
            add_plant(n, c)
            st.rerun()

with tabs[3]:
    if plants:
        p_list = [p['name'] for p in plants]
        sel_p = st.selectbox("대상 식물", p_list)
        # 다중 선택된 영양제들을 콤마로 연결해 DB에 깔끔하게 저장
        sel_f = st.multiselect("약제 선택", FERTS)
        if st.button("기록"):
            fert_str = ", ".join(sel_f)
            add_log(datetime.now().strftime("%Y-%m-%d"), sel_p, fert_str)
            st.success("기록됨")

with tabs[4]:
    st.subheader("⚖️ 분갈이 흙 계산기")
    sel_recipe = st.selectbox("식물 종류", list(RECIPES.keys()))
    sel_pot = st.selectbox("화분 크기", list(POTS.keys()))
    count = st.number_input("화분 개수", 1, 100, 1)
    
    if st.button("계산하기"):
        total_vol = POTS[sel_pot] * count
        st.success(f"필요한 총 흙의 양: **{total_vol:.1f} L**")
        st.write("---")
        for mat, ratio in RECIPES[sel_recipe].items():
            # 반에그먼트를 지우지 않고 유지하여 다른 식물들 계산도 정상 작동
            if mat in ["반에그먼트", "바로커", "산야초", "질석", "훈탄"]:
                st.write(f"📍 **{mat}**: {ratio * total_vol / 1000:.2f} L")
            else:
                st.write(f"💊 **{mat}**: {ratio * total_vol:.1f} g")
