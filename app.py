import streamlit as st
import json
from datetime import datetime, timedelta

st.set_page_config(page_title="윤슬의 정원 v7.6", layout="wide")

DATA_FILE="garden_data.json"

# ---------------------
# 데이터 로드 / 저장
# ---------------------

def load_data():
    try:
        with open(DATA_FILE,"r") as f:
            return json.load(f)
    except:
        return {"plants":[], "logs":[]}

def save_data():
    with open(DATA_FILE,"w") as f:
        json.dump(st.session_state.data,f)

if "data" not in st.session_state:
    st.session_state.data=load_data()

# ---------------------
# 기본 설정
# ---------------------

CATEGORIES=[
"사랑초","스카푸","베고니아","구근류",
"수국","파종 식물","가든멈국화",
"미니신닌기아","팬지/비올라"
]

FERTS=[
"마감프K","멀티코트","아그로믹파워",
"잭스 Grow","잭스 Bloom","멀티미크로",
"골드아이언","토탈싹", "벅스킬"
]

# 영양제/약제별 재투입 주기 (일 단위)
REAPPLY_DAYS = {
    "마감프K": 180,       
    "멀티코트": 180,       
    "아그로믹파워": 90,     
    "잭스 Grow": 14,      
    "잭스 Bloom": 14,     
    "멀티미크로": 30,      
    "골드아이언": 30,      
    "토탈싹": 30,         
    "벅스킬": 14          
}

POTS={
"5호":0.3,
"9호":0.8,
"10호":1.0,
"15호":2.5
}

# ---------------------
# 흙배합 레시피
# ---------------------

RECIPES={

"사랑초":{"바로커":650,"산야초":250,"질석":0,"훈탄":100,
"마감프K":1.5,"멀티코트":3,"아그로믹파워":1,"토탈싹":0.8},

"스카푸":{"바로커":450,"산야초":350,"질석":100,"훈탄":100,
"멀티코트":2,"마감프K":1,"아그로믹파워":1,"토탈싹":0.8},

"베고니아":{"바로커":500,"산야초":300,"질석":100,"훈탄":100,
"멀티코트":2,"아그로믹파워":1,"토탈싹":0.8},

"미니신닌기아":{"바로커":400,"산야초":350,"질석":150,"훈탄":100,
"멀티코트":3,"아그로믹파워":1,"토탈싹":0.8},

"구근류":{"바로커":550,"산야초":300,"질석":50,"훈탄":100,
"멀티코트":2,"토탈싹":0.8},

"수국":{"바로커":600,"산야초":300,"질석":0,"훈탄":100,
"멀티코트":3,"아그로믹파워":1,"토탈싹":0.8},

"팬지/비올라":{"바로커":600,"산야초":300,"질석":0,"훈탄":100,
"멀티코트":2,"토탈싹":0.8},

"가든멈국화":{"바로커":600,"산야초":300,"질석":0,"훈탄":100,
"멀티코트":3,"토탈싹":0.8},

"파종 식물":{"바로커":500,"산야초":300,"질석":200,"훈탄":0,
"멀티코트":1,"토탈싹":0.5}
}

# ---------------------
# 타이틀
# ---------------------

st.title("🌿 윤슬의 정원 매니저 v7.6")

tabs=st.tabs([
"홈","할일목록","식물관리","영양제기록",
"분갈이계산기","흙배합","식물등"
])

# ---------------------
# 홈
# ---------------------

with tabs[0]:

    total=len(st.session_state.data["plants"])

    st.metric("총 식물 수",total)

    category_count={}

    for p in st.session_state.data["plants"]:
        category_count[p["category"]]=category_count.get(p["category"],0)+1

    for k,v in category_count.items():
        st.write(f"{k} : {v}")

# ---------------------
# 할일목록
# ---------------------

with tabs[1]:
    st.subheader("📋 오늘의 정원 할 일")
    st.caption("과거 기록을 바탕으로 영양제와 병충해 약 투입 시기를 알려줍니다.")
    
    today = datetime.now()
    todo_list = []
    
    for log in st.session_state.data.get("logs", []):
        log_date = datetime.strptime(log["date"], "%Y-%m-%d")
        plant_name = log["plant"]
        
        for fert in log.get("fert", []):
            if fert in REAPPLY_DAYS:
                next_date = log_date + timedelta(days=REAPPLY_DAYS[fert])
                
                if next_date <= today:
                    days_passed = (today - log_date).days
                    todo_list.append({
                        "plant": plant_name,
                        "fert": fert,
                        "last_date": log["date"],
                        "days_passed": days_passed
                    })
    
    if todo_list:
        for item in todo_list:
            st.warning(f"💧 **{item['plant']}** : **{item['fert']}** 재투입이 필요해! (마지막 투입일: {item['last_date']} / {item['days_passed']}일 경과)")
    else:
        st.success("🎉 오늘은 투입할 약제나 영양제가 없어. 식물들과 평화로운 하루를 보내!")

# ---------------------
# 식물관리 (수정 기능 추가됨)
# ---------------------

with tabs[2]:

    st.subheader("식물 추가")

    col1,col2=st.columns(2)

    with col1:
        category=st.selectbox("카테고리",CATEGORIES)

    with col2:
        name=st.text_input("식물 이름")

    if st.button("추가") and name:

        st.session_state.data["plants"].append({
            "name":name,
            "category":category
        })

        save_data()
        st.rerun()

    st.divider()

    search=st.text_input("🔍 식물 검색")

    plants=st.session_state.data["plants"]

    if search:
        plants=[p for p in plants if search.lower() in p["name"].lower()]

    for i,p in enumerate(plants):

        # 레이아웃을 3칸으로 나누어 수정/삭제 버튼 배치
        col1, col2, col3 = st.columns([6, 1, 1])

        with col1:
            st.write(f"🌱 {p['category']} - {p['name']}")

        with col2:
            # 상태 관리를 통해 수정 창을 열고 닫음
            if st.button("수정", key=f"edit_btn_{i}"):
                st.session_state[f"edit_mode_{i}"] = not st.session_state.get(f"edit_mode_{i}", False)

        with col3:
            if st.button("삭제", key=f"del_{i}"):
                st.session_state.data["plants"].remove(p)
                save_data()
                st.rerun()

        # 수정 버튼을 눌렀을 때 나타나는 입력창
        if st.session_state.get(f"edit_mode_{i}", False):
            with st.expander("📝 식물 정보 수정", expanded=True):
                new_category = st.selectbox(
                    "새 카테고리", 
                    CATEGORIES, 
                    index=CATEGORIES.index(p['category']) if p['category'] in CATEGORIES else 0,
                    key=f"new_cat_{i}"
                )
                new_name = st.text_input("새 식물 이름", value=p['name'], key=f"new_name_{i}")
                
                if st.button("저장", key=f"save_btn_{i}"):
                    p['category'] = new_category
                    p['name'] = new_name
                    st.session_state[f"edit_mode_{i}"] = False
                    save_data()
                    st.rerun()

# ---------------------
# 영양제 기록
# ---------------------

with tabs[3]:

    if st.session_state.data["plants"]:

        plant_names=[p["name"] for p in st.session_state.data["plants"]]

        plant=st.selectbox("식물 선택",plant_names)

        fert=st.multiselect("영양제 및 약제",FERTS)

        note=st.text_input("메모")

        if st.button("기록 저장"):

            log={
            "date":datetime.now().strftime("%Y-%m-%d"),
            "plant":plant,
            "fert":fert,
            "note":note
            }

            st.session_state.data["logs"].append(log)

            save_data()

            st.success("기록 저장 완료")

    st.divider()

    for log in st.session_state.data["logs"][::-1]:

        st.info(
        f"{log['date']} | {log['plant']} | {','.join(log['fert'])}"
        )

# ---------------------
# 분갈이 계산기
# ---------------------

with tabs[4]:

    plant=st.selectbox("식물 종류",list(RECIPES.keys()))

    pot=st.selectbox("화분 크기",list(POTS.keys()))

    count=st.number_input("개수",1,200)

    if st.button("계산"):

        volume=POTS[pot]*count

        st.write(f"총 흙 : {volume} L")

        recipe=RECIPES[plant]

        for k,v in recipe.items():

            if k in ["바로커","산야초","질석","훈탄"]:
                st.write(f"{k} : {v*volume/1000:.2f} L")

            else:
                st.write(f"{k} : {v*volume:.1f} g")

# ---------------------
# 흙배합
# ---------------------

with tabs[5]:

    plant=st.selectbox("식물",list(RECIPES.keys()))

    recipe=RECIPES[plant]

    st.write("1L 기준")

    for k,v in recipe.items():

        if k in ["바로커","산야초","질석","훈탄"]:
            st.write(f"{k} : {v} ml")

        else:
            st.write(f"{k} : {v} g")

# ---------------------
# 식물등
# ---------------------

with tabs[6]:

    month=datetime.now().month

    if month in [3,4,5]:
        light="봄 : 식물등 6시간"

    elif month in [6,7,8]:
        light="여름 : 식물등 4~5시간"

    elif month in [9,10,11]:
        light="가을 : 식물등 6시간"

    else:
        light="겨울 : 식물등 9~10시간"

    st.info(light)

    st.write("환경 : 정남향 베란다 + 소나무 차광")
