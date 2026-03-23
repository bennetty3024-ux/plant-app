import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
from datetime import datetime

# 1. 설정 및 구글 시트 연결
st.set_page_config(page_title="윤슬의 정원 v7.8", layout="wide")

@st.cache_resource
def init_connection():
    # Streamlit Secrets에서 GCP 열쇠 불러오기
    key_dict = json.loads(st.secrets["gcp_key"])
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(key_dict, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open("정원매니저DB")

try:
    doc = init_connection()
    plants_sheet = doc.worksheet("plants")
    logs_sheet = doc.worksheet("logs")
except Exception as e:
    st.error("데이터베이스 연결 실패! 시트 이름이나 공유 권한을 다시 확인해주세요.")
    st.stop()

# DB 데이터 로드 및 조작 함수
def load_plants():
    records = plants_sheet.get_all_records()
    return records

def add_plant(name, category):
    records = plants_sheet.get_all_records()
    new_id = 1 if not records else max([int(str(r['id'])) for r in records if str(r['id']).isdigit()] + [0]) + 1
    plants_sheet.append_row([new_id, name, category])

def update_plant(plant_id, new_name):
    cell = plants_sheet.find(str(plant_id), in_column=1)
    if cell:
        plants_sheet.update_cell(cell.row, 2, new_name)

def delete_plant(plant_id):
    cell = plants_sheet.find(str(plant_id), in_column=1)
    if cell:
        plants_sheet.delete_rows(cell.row)

def add_log(date, plant, fert):
    records = logs_sheet.get_all_records()
    new_id = 1 if not records else max([int(str(r['id'])) for r in records if str(r['id']).isdigit()] + [0]) + 1
    logs_sheet.append_row([new_id, date, plant, fert])

# 2. 고정 데이터
CATEGORIES = [
    "옵투사사랑초", "사랑초", "베고니아", "미니신닌기아", "아키메네스", "구근류", "수국", 
    "파종 식물", "가든멈국화", "팬지/비올라", "페츄니아", "호주깨동백"
]
FERTS = ["마감프K", "멀티코트", "오스모코트", "잭스 Grow", "잭스 Bloom", "멀티미크로", "골드아이언", "토탈싹", "벅스킬"]
POTS = {"5호": 0.3, "9호": 0.8, "10호": 1.0, "15호": 2.5}

RECIPES = {
    "옵투사사랑초": {"바로커": 650, "산야초": 250, "훈탄": 100, "마감프K": 1.5, "멀티코트": 3, "토탈싹": 0.8},
    "베고니아": {"바로커": 500, "산야초": 300, "질석": 100, "훈탄": 100, "멀티코트": 2, "토탈싹": 0.8},
    "미니신닌기아": {"바로커": 400, "산야초": 250, "질석": 250, "훈탄": 100, "멀티코트": 3, "토탈싹": 0.8},
    "구근류": {"바로커": 550, "산야초": 300, "질석": 50, "훈탄": 100, "멀티코트": 2, "토탈싹": 0.8},
    "초화류(페츄니아등)": {"바로커": 600, "산야초": 300, "훈탄": 100, "멀티코트": 3, "토탈싹": 0.8}
}

st.title("🌿 윤슬의 정원 매니저 v7.8 (클라우드 연동됨!)")

plants = load_plants()

tabs = st.tabs(["🏠 홈/스마트 팁", "🪴 식물 목록", "➕ 식물 추가", "💊 영양제기록", "⚖️ 분갈이계산"])

with tabs[0]:
    st.metric("총 식물 수", len(plants))
    st.divider()
    
    current_month = datetime.now().month
    st.subheader(f"💡 {current_month}월의 베란다 정원 관리 팁")
    
    st.info("**🌺 호주깨동백 가지치기**\n\n봄꽃이 다 진 직후가 가지치기 적기입니다. 전체 길이의 1/3 정도를 잘라내어 수형을 둥글게 잡아주세요.")
    st.info("**🧅 사랑초 & 구근류 영양 관리**\n\n꽃이 지고 잎이 구근을 키우는 시기입니다. **잭스 Grow**나 **골드아이언**을 물 1L당 1g (1000배액) 비율로 희석해서 관주해주세요.")

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
        sel_f = st.multiselect("약제 선택", FERTS)
        if st.button("기록"):
            fert_str = ", ".join(sel_f)
            add_log(datetime.now().strftime("%Y-%m-%d"), sel_p, fert_str)
            st.success("구글 시트에 안전하게 기록되었습니다! ☁️")

with tabs[4]:
    st.subheader("⚖️ 분갈이 흙 계산기")
    sel_recipe = st.selectbox("식물 종류", list(RECIPES.keys()))
    sel_pot = st.selectbox("화분 크기", list(POTS.keys()))
    count = st.number_input("화분 개수", 1, 100, 1)
    
    if st.button("계산하기"):
        total_vol = POTS[sel_pot] * count
        st.success(f"기준점: 전체 흙 {total_vol:.1f}L 배합 비율 (기본 상토: 바로커)")
        st.write("---")
        for mat, ratio in RECIPES[sel_recipe].items():
            if mat in ["바로커", "산야초", "질석", "훈탄"]:
                st.write(f"📍 **{mat}**: {ratio * total_vol / 1000:.2f} L")
            else:
                st.write(f"💊 **{mat}**: {ratio * total_vol:.1f} g")
