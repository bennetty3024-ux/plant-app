import streamlit as st
from datetime import datetime, timedelta
import json

st.set_page_config(page_title="윤슬의 정원 매니저 v4", layout="wide")

SAVE_FILE = "garden_log.json"

# 저장 함수
def save_log():
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.garden_log, f, ensure_ascii=False)

# 불러오기
def load_log():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            st.session_state.garden_log = json.load(f)
    except:
        st.session_state.garden_log = []

# 최초 실행
if "garden_log" not in st.session_state:
    load_log()

# 식물 리스트
MY_PLANTS = [
"스카푸","동형종 사랑초","옵투사 사랑초","미니신닌기아",
"베고니아","일본수국","가든멈국화","팬지/비올라",
"네메시아","금어초","데모루","기타"
]

# 비료 리스트
MY_FERTS = [
"마감프K","하이파 멀티코트(6개월)","아그로믹파워",
"잭스 Bloom","잭스 Grow","멀티미크로 콤비",
"골드아이언","오스모코트","벅스킹(살충제)"
]

# 물주기 규칙
WATER_RULE = {
"일본수국":3,
"스카푸":4,
"동형종 사랑초":5,
"옵투사 사랑초":5,
"베고니아":4
}

st.title("🌿 윤슬의 정원 매니저 v4")
st.caption("정남향 3층 베란다 (소나무 필터광 환경 최적화)")

# 오늘 할 일
st.subheader("📢 오늘 해야 할 관리")

today = datetime.now().strftime("%m월 %d일")

for entry in st.session_state.garden_log:
    if entry["water"] == today:
        st.warning(f"💧 {entry['name']} 물주기 추천")

# 입력 영역
col1,col2 = st.columns([2,1])

with col1:

    with st.form("plant_form", clear_on_submit=True):

        st.subheader("🌱 식물 관리 기록")

        c1,c2 = st.columns(2)

        with c1:
            category = st.selectbox("식물 종류",MY_PLANTS)
            name = st.text_input("개체 이름",max_chars=30)

        with c2:
            stage = st.selectbox("상태",
            ["파종","정식","성장기","꽃봉오리","개화","휴면"])

        st.write("💊 사용한 비료")

        ferts=[]
        cols=st.columns(3)

        for i,f in enumerate(MY_FERTS):
            if cols[i%3].checkbox(f):
                ferts.append(f)

        notes = st.text_area("메모",max_chars=200)

        photo = st.file_uploader("식물 사진",type=["jpg","png"])

        if st.form_submit_button("기록 저장"):

            now=datetime.now()

            water_days=WATER_RULE.get(category,5)

            water_day=(now+timedelta(days=water_days)).strftime("%m월 %d일")

            entry={
            "date":now.strftime("%Y-%m-%d %H:%M"),
            "category":category,
            "name":name,
            "stage":stage,
            "ferts":ferts,
            "notes":notes,
            "water":water_day
            }

            st.session_state.garden_log.insert(0,entry)

            save_log()

            st.success("기록 저장 완료 🌿")

# 검색
st.divider()

st.subheader("🔍 식물 기록 검색")

search=st.text_input("이름 검색")

if search:
    logs=[e for e in st.session_state.garden_log if search.lower() in e["name"].lower()]
else:
    logs=st.session_state.garden_log

# 기록 표시
st.subheader("📋 정원 관리 기록")

for i,entry in enumerate(logs):

    with st.expander(f"{entry['date']} | {entry['name']} ({entry['category']})"):

        st.write("🌱 상태:",entry["stage"])

        st.write("💊 비료:",", ".join(entry["ferts"]) if entry["ferts"] else "없음")

        st.write("📝 메모:",entry["notes"])

        st.info(f"💧 다음 물주기 추천 : {entry['water']}")

        if "벅스킹(살충제)" in entry["ferts"]:
            st.warning("⚠️ 반려견 접근 주의")

        if st.button("🗑 기록 삭제",key=i):

            st.session_state.garden_log.remove(entry)

            save_log()

            st.rerun()

with col2:

    st.header("📚 우리집 배합 레시피")

    with st.expander("스카푸"):
        st.write("반에그 5 : 야생화흙 4 : 훈탄 1")

    with st.expander("수국 / 사랑초"):
        st.write("반에그 7 : 야생화흙 2 : 훈탄 1")

    with st.expander("비료 기준 (9cm)"):
        st.write("마감프K 1.5g")
        st.write("멀티코트 20알")
        st.write("벅스킹 1g")
