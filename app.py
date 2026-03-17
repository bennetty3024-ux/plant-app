import streamlit as st
from datetime import datetime, timedelta
import json

st.set_page_config(page_title="윤슬의 정원 매니저 v6.2",layout="centered")

SAVE_FILE="garden_log.json"

def load_data():
    try:
        with open(SAVE_FILE,"r",encoding="utf-8") as f:
            data=json.load(f)

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

PLANT_TYPES=[
"스카푸","동형종 사랑초","옵투사 사랑초",
"미니신닌기아","베고니아","일본수국",
"가든멈국화","팬지/비올라","네메시아",
"금어초","데모루","기타"
]

SOIL_RECIPES={
"스카푸":"반에그5 : 산야초4 : 훈탄1",
"동형종 사랑초":"반에그6 : 산야초3 : 훈탄1",
"옵투사 사랑초":"반에그7 : 산야초2 : 훈탄1",
"미니신닌기아":"반에그6 : 산야초3 : 훈탄1",
"베고니아":"반에그6 : 산야초3 : 훈탄1",
"일본수국":"반에그7 : 산야초2 : 훈탄1"
}

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

st.title("🌿 윤슬의 정원 매니저")

tab1,tab2,tab3,tab4,tab5,tab6=st.tabs([
"📢 오늘관리",
"🌱 식물목록",
"➕ 기록",
"📋 관리일지",
"🪴 흙배합",
"📊 통계"
])

# 오늘관리
with tab1:

    today=datetime.now().strftime("%m월 %d일")

    for log in st.session_state.data["logs"]:

        if log.get("water")==today:

            st.warning(f"💧 {log.get('plant')} 물주기")

# 식물목록
with tab2:

    for i,p in enumerate(st.session_state.data["plants"]):

        col1,col2=st.columns([4,1])

        with col1:
            st.info(f"🌱 {p}")

        with col2:

            if st.button("삭제",key=f"plant_del_{i}"):

                used=False

                for log in st.session_state.data["logs"]:
                    if log["plant"]==p:
                        used=True

                if used:
                    st.warning("기록이 있어 삭제할 수 없습니다")
                else:
                    st.session_state.data["plants"].remove(p)
                    save_data()
                    st.rerun()

    newplant=st.text_input("식물 추가")

    if st.button("추가"):

        if newplant!="":
            st.session_state.data["plants"].append(newplant)
            save_data()
            st.rerun()

# 기록
with tab3:

    plants=st.session_state.data["plants"]

    if plants:

        with st.form("logform"):

            plant=st.selectbox("식물",plants)

            ptype=st.selectbox("종류",PLANT_TYPES)

            stage=st.selectbox("상태",["파종","성장","개화","휴면"])

            fert=st.multiselect("비료",FERTS)

            memo=st.text_area("메모")

            submit=st.form_submit_button("저장")

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

                st.success("기록 저장")

# 관리일지
with tab4:

    for i,log in enumerate(st.session_state.data["logs"]):

        with st.expander(f"{log['date']} | {log['plant']}"):

            st.write("상태:",log["stage"])

            st.write("비료:",", ".join(log["fert"]))

            st.write("메모:",log["memo"])

            st.info(f"다음 물주기 {log['water']}")

            if st.button("삭제",key=f"log{i}"):

                st.session_state.data["logs"].remove(log)

                save_data()

                st.rerun()

# 흙배합
with tab5:

    st.subheader("우리집 흙 배합")

    for plant,recipe in SOIL_RECIPES.items():

        st.success(f"{plant}")

        st.write(recipe)

# 통계
with tab6:

    st.metric("식물 수",len(st.session_state.data["plants"]))

    st.metric("관리 기록",len(st.session_state.data["logs"]))
