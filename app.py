import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
from datetime import datetime

# 1. 설정 및 구글 시트 연결
st.set_page_config(page_title="윤슬의 정원 v8.0", layout="wide")

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

st.title("🌿 윤슬의 정원 매니저 v8.0 (통합 완료!)")

plants = load_plants()

# 탭을 9개로 확장하여 기존 기능과 새 기능 모두 유지
tabs = st.tabs([
    "🏠 홈/스마트 팁", "🪴 식물 목록", "➕ 식물 추가", "💊 영양제기록", 
    "⚖️ 화분 계산기", "🌷 구근 라자냐", "🧪 10L 정밀배합", "☀️ 식물등 스케줄", "📸 감성 포토존"
])

# --- 기존 탭 0~4 유지 ---
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
    st.subheader("⚖️ 분갈이 흙 계산기 (화분 기준)")
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

# --- 새로운 탭 5~8 추가 ---
with tabs[5]:
    st.subheader("🌷 추식구근 3단 라자냐 시뮬레이터")
    st.info("화분 깊이에 따라 튤립, 수선화, 무스카리 등 개화 시기와 높이가 다른 구근을 배치해 보세요.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**하단 (대형 구근)**")
        bottom_layer = st.multiselect("하단 구근 선택", ["튤립 (카니발 드 니스 등)", "수선화", "알리움", "히아신스 (스칼렛 펄 등)"])
    with col2:
        st.markdown("**중단 (중간 구근)**")
        middle_layer = st.multiselect("중단 구근 선택", ["원종 튤립", "히아신스", "미니 수선화"])
    with col3:
        st.markdown("**상단 (소형 구근)**")
        top_layer = st.multiselect("상단 구근 선택", ["무스카리", "크로커스", "스노우드롭", "사랑초 (옵투사 등)"])
        
    st.markdown("---")
    
    # 선택한 구근들을 하나의 텍스트로 묶기
    bottom_str = ', '.join(bottom_layer) if bottom_layer else '비어있음'
    middle_str = ', '.join(middle_layer) if middle_layer else '비어있음'
    top_str = ', '.join(top_layer) if top_layer else '비어있음'
    
    combo_text = f"하단: {bottom_str} / 중단: {middle_str} / 상단: {top_str}"
    
    st.success(f"**현재 조합 미리보기**\n\n{combo_text}")
    
    # 구글 시트에 저장하는 버튼
    if st.button("☁️ 이 조합을 구글 시트에 기록하기"):
        if not bottom_layer and not middle_layer and not top_layer:
            st.warning("구근을 하나 이상 선택해주세요!")
        else:
            # 기존 영양제 기록 함수를 재활용하여 logs 시트에 저장
            add_log(datetime.now().strftime("%Y-%m-%d"), "추식구근(라자냐)", combo_text)
            st.balloons()  # 성공 시 풍선 애니메이션 효과!
            st.success("올해의 구근 라자냐 조합이 구글 시트에 안전하게 기록되었습니다! 🌷")

with tabs[6]:
    st.subheader("🧪 10L 기준 정밀 흙/비료 대용량 배합 (바로커 7:3)")
    st.write("대용량 흙 배합이 필요할 때 사용하는 정확한 기준점입니다. (유기질 30 : 무기질 70)")
    
    base_volume = st.number_input("전체 배합량 기준 (리터)", min_value=1.0, value=10.0, step=1.0)
    
    # 7:3 바로커/무기질 공식
    baroker_vol = base_volume * 0.3
    inorganic_vol = base_volume * 0.7
    
    # 10L 기준 추가 부자재 권장량
    huntan = base_volume * 0.1
    magamp_k = base_volume * 3
    osmocote = base_volume * 2
    
    st.markdown("### 📊 정밀 배합 레시피")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="바로커 상토 (30%)", value=f"{baroker_vol:.1f} L")
        st.metric(label="산야초 등 무기질 (70%)", value=f"{inorganic_vol:.1f} L")
    with col_b:
        st.metric(label="훈탄 (약 10% 추가)", value=f"{huntan:.1f} L")
        st.metric(label="마감프K (중소립)", value=f"{magamp_k:.0f} g")
        st.metric(label="오스모코트", value=f"{osmocote:.0f} g")

with tabs[7]:
    st.subheader("☀️ 계절별 채광 및 식물등 스케줄러")
    st.write("소나무 그림자가 지는 정남향 3층 베란다 환경 맞춤 스케줄입니다.")
    
    season = st.selectbox("현재 계절 확인", ["봄", "여름", "가을", "겨울"])
    
    if season in ["봄", "가을"]:
        st.info("💡 **식물등 가동:** 오전 9시 ~ 오후 6시\n\n(소나무 그림자가 길어지는 시간대에 빛을 집중 보완해 주세요.)")
    elif season == "여름":
        st.info("💡 **식물등 가동:** 오전 10시 ~ 오후 4시\n\n(해가 높아 베란다 안쪽까지 빛이 덜 들어오는 시간 위주, 흐린 날은 연장 필수)")
    else:
        st.info("💡 **식물등 가동:** 오전 8시 ~ 오후 5시\n\n(전체 일조 시간이 짧아 식물등 의존도가 가장 높은 시기입니다.)")

with tabs[8]:
    st.subheader("📸 거실 베란다창가 포토존 & 장비 메모")
    
    photo_season = st.radio("포토존 베스트 햇살 타임", ["봄/가을", "여름", "겨울"], horizontal=True)
    if photo_season == "봄/가을":
        st.success("✨ **추천 시간대:** 오전 10:30 ~ 12:00 (부드럽고 따뜻한 감성 무드)")
    elif photo_season == "여름":
        st.success("✨ **추천 시간대:** 오전 9:00 ~ 10:30 (빛이 강해지기 전 맑고 투명한 느낌)")
    else:
        st.success("✨ **추천 시간대:** 오후 12:00 ~ 2:00 (베고니아 솜털이 빛나는 드라마틱한 햇살)")
        
    st.markdown("---")
    st.markdown("### 📷 감성 접사 장비 세팅")
    st.text_area("현재 장비 셋업 및 메모", 
"""- Camera: Nikon D5300
- Lens: AF-S DX Micro NIKKOR 40mm f/2.8G
- Flash: Godox TT350-N 
- 플래시 바운스/광량 메모: 
- 포커스 & 조리개 메모: 
""", height=150)
