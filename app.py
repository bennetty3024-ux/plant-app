import streamlit as st
from datetime import datetime, timedelta
import json

st.set_page_config(
page_title="윤슬의 정원 매니저 v6.1",
layout="centered"
)

SAVE_FILE="garden_log.json"

# -------------------------
# 데이터 로드 (구버전 호환)
# -------------------------

def load_data():
    try:
        with open(SAVE_FILE,"r",encoding="utf-8") as f:
            data=json.load(f)

        # v5 데이터 구조 대응
        if isinstance(data,list):
            st.session_state.data={
                "plants":[],
                "logs":data
            }
        else:
            st.session_state.data=data

    except:
        st.session_state.data={
            "plants":[],
            "logs":[]
        }

def save_data():
    with open(SAVE_FILE,"w",encoding="utf-8") as f:
        json.dump(st.session_state.data,f,ensure_ascii=False)

if "data" not in st.session_state:
    load_data()

# -------------------------
# 기본 데이터
# -------------------------

PLANT_TYPES=[
"스카푸","동형종 사랑초","옵투사 사랑초",
"미니신닌기아","베고니아","일본수국",
"가든멈국화","팬지/비올라","네메시아",
"금어초","데모루","기타"
]

FERTS=[
"마감프K","멀티코트6개월","아그로믹파워",
"잭스 Grow","잭스 Bloom",
"멀티미크로","골드아이언",
"오스모코트","벅스킹"
]

WATER_RULE={
"일본수국":3,
"스카푸":4,
"동형종 사랑초":5,
"옵투사 사랑초":5,
"베고니아":4
}

# -------------------------
# 제목
# -------------------------

st.title("🌿 윤슬의 정원 매니저")
st.caption("정남향 3층 베란다 · 소나무 필터광")

# -------------------------
# 탭 UI
# -------------------------

tab1,tab2,tab3,tab4,tab5=st.tabs([
"📢 오늘관리",
"🌱 식물목록",
"➕ 기록",
"📋 관리일지",
"📊 통계"
])

# -------------------------
# 오늘관리
# -------------------------

with tab1:

    st.subheader("오늘 해야 할 관리")

    today=datetime.now().strftime("%m월 %d일")

    count=0

    for log in st.session_state.data["logs"]:

        if log.get("water")==today:

            count+=1

            st.warning(f"💧 {log.get('plant','식물')} 물주기")

    if count==0:
        st.success("오늘 예정된 관리 없음 🌿")

# -------------------------
# 식물 목록
# -------------------------

with tab2:

    st.subheader("우리집 식물")

    if st.session_state.data["plants"]:

        cols=st.columns(2)

        for i,p in enumerate(st.session_state.data["plants"]):

            with cols[i%2]:
                st.info(f"🌱 {p}")

    newplant=st.text_input("새 식물 추가")

    if st.button("식물 추가"):

        if newplant!="":

            st.session_state.data["plants"].append(newplant)

            save_data()

            st.rerun()

# -------------------------
# 기록 입력
# -------------------------

with tab3:

    st.subheader("관리 기록")

    plants=st.session_state.data["plants"]

    if not plants:

        st.warning("먼저 식물 목록에 식물을 추가하세요")

    else:

        with st.form("logform"):

            plant=st.selectbox("식물 선택",plants)

            ptype=st.selectbox("식물 종류",PLANT_TYPES)

            stage=st.selectbox(
            "상태",
            ["파종","정식","성장","꽃봉오리","개화","휴면"]
            )

            fert=st.multiselect("비료",FERTS)

            memo=st.text_area("메모")

            submit=st.form_submit_button("기록 저장")

            if submit:

                now=datetime.now()

                water=WATER_RULE.get(ptype,5)

                waterday=(now+timedelta(days=water)).strftime("%m월 %d일")

                log={
                "date":now.strftime("%Y-%m-%d"),
                "plant":plant,
                "type":ptype,
                "stage":stage,
                "fert":fert,
                "memo":memo,
                "water":waterday
                }

                st.session_state.data["logs"].insert(0,log)

                save_data()

                st.success("기록 저장 완료 🌿")

# -------------------------
# 관리일지
# -------------------------

with tab4:

    st.subheader("관리 기록")

    logs=st.session_state.data["logs"]

    if not logs:
        st.info("기록이 없습니다")

    for i,log in enumerate(logs):

        with st.expander(f"{log.get('date')} | {log.get('plant')}"):

            st.write("🌱 상태:",log.get("stage"))

            ferts=log.get("fert",[])

            if ferts:
                st.write("💊 비료:",", ".join(ferts))
            else:
                st.write("💊 비료 없음")

            st.write("📝 메모:",log.get("memo",""))

            st.info(f"💧 다음 물주기 {log.get('water')}")

            if st.button("삭제",key=i):

                st.session_state.data["logs"].remove(log)

                save_data()

                st.rerun()

# -------------------------
# 통계
# -------------------------

with tab5:

    st.subheader("정원 통계")

    plants=len(st.session_state.data["plants"])

    logs=len(st.session_state.data["logs"])

    st.metric("총 식물 수",plants)

    st.metric("관리 기록 수",logs)

    fert_count={}

    for log in st.session_state.data["logs"]:

        for f in log.get("fert",[]):

            fert_count[f]=fert_count.get(f,0)+1

    st.write("비료 사용 통계")

    st.json(fert_count)
