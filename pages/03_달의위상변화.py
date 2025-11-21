import streamlit as st
import ephem
import math
import datetime
import numpy as np
import plotly.graph_objects as go

# --- 페이지 설정 ---
st.set_page_config(page_title="달의 위상 변화 학습", layout="wide", page_icon="🌖")

# --- 상수 및 설정 ---
KST_OFFSET = datetime.timedelta(hours=9)
SEOUL_LAT = '37.5665'
SEOUL_LON = '126.9780'

def get_moon_info(target_date):
    """
    날짜에 따른 달의 정보 및 태양-달-지구 각도 계산
    """
    observer = ephem.Observer()
    observer.lat = SEOUL_LAT
    observer.lon = SEOUL_LON
    observer.date = target_date - datetime.timedelta(hours=9)
    
    moon = ephem.Moon()
    sun = ephem.Sun()
    moon.compute(observer)
    sun.compute(observer)
    
    illumination = moon.phase 
    
    # 달과 태양의 황경 차이 (0~360도) -> 이것이 곧 위치 관계 각도
    lon_diff = (moon.hlon - sun.hlon) % (2 * math.pi)
    degrees = math.degrees(lon_diff) # 0(삭) -> 90(상현) -> 180(망) -> 270(하현)
    
    is_waxing = 0 <= degrees < 180
    
    # 뜨고 지는 시각
    try:
        rise_time = observer.next_rising(moon).datetime() + KST_OFFSET
        set_time = observer.next_setting(moon).datetime() + KST_OFFSET
        rise_str = rise_time.strftime("%H시 %M분")
        set_str = set_time.strftime("%H시 %M분")
    except:
        rise_str = "--:--"
        set_str = "--:--"

    phase_name = ""
    if illumination < 2: phase_name = "삭 (New Moon)"
    elif illumination > 98: phase_name = "보름달/망 (Full Moon)"
    elif is_waxing:
        if illumination < 45: phase_name = "초승달"
        elif illumination < 55: phase_name = "상현달"
        else: phase_name = "차오르는 달"
    else:
        if illumination < 45: phase_name = "그믐달"
        elif illumination < 55: phase_name = "하현달"
        else: phase_name = "기우는 달"

    return {
        "illumination": illumination,
        "angle_rad": lon_diff, # 라디안 값 (궤도 그리기에 필요)
        "degrees": degrees,
        "is_waxing": is_waxing,
        "rise_str": rise_str,
        "set_str": set_str,
        "phase_name": phase_name
    }

def draw_moon_phase(illumination, is_waxing):
    """[지구 관점] 달의 위상(모양) 그리기"""
    r = 10 
    fig = go.Figure()
    
    # 1. 배경 원
    fig.add_shape(type="circle", x0=-r, y0=-r, x1=r, y1=r, fillcolor="black", line_color="gray")

    # 2. 위상 계산
    t = np.linspace(0, np.pi, 100)
    x_edge = r * np.cos(t)
    y_edge = r * np.sin(t)
    p = illumination / 100.0
    offset = -r * (2 * p - 1)

    if is_waxing:
        theta = np.linspace(-np.pi/2, np.pi/2, 100)
        x_outer = r * np.cos(theta)
        y_outer = r * np.sin(theta)
        x_inner = offset * np.cos(theta)
        x_poly = np.concatenate([x_outer, x_inner[::-1]])
        y_poly = np.concatenate([y_outer, y_outer[::-1]])
    else:
        theta = np.linspace(np.pi/2, 3*np.pi/2, 100)
        x_outer = r * np.cos(theta)
        y_outer = r * np.sin(theta)
        x_inner = offset * np.cos(theta)
        x_poly = np.concatenate([x_outer, x_inner[::-1]])
        y_poly = np.concatenate([y_outer, y_outer[::-1]])

    fig.add_trace(go.Scatter(x=x_poly, y=y_poly, fill="toself", fillcolor="#F4F6F0", line_width=0, hoverinfo="skip"))

    fig.update_layout(
        title="<b>[지구 관점]</b> 오늘 밤 달의 모양",
        xaxis=dict(visible=False, range=[-12, 12]),
        yaxis=dict(visible=False, range=[-12, 12]),
        width=300, height=300,
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def draw_orbit_diagram(angle_rad):
    """[우주 관점] 태양-지구-달 위치 관계 그리기"""
    fig = go.Figure()
    
    # 좌표 설정 (지구=원점, 태양=오른쪽 멀리)
    earth_pos = (0, 0)
    sun_pos = (5, 0) # 시각적 편의를 위해 거리 축소
    orbit_radius = 2.5
    
    # 달의 위치 계산
    moon_x = orbit_radius * math.cos(angle_rad)
    moon_y = orbit_radius * math.sin(angle_rad)
    
    # 1. 궤도 그리기 (점선)
    theta = np.linspace(0, 2*np.pi, 100)
    fig.add_trace(go.Scatter(
        x=orbit_radius * np.cos(theta), y=orbit_radius * np.sin(theta),
        mode='lines', line=dict(color='gray', dash='dot'), hoverinfo='skip'
    ))

    # 2. 태양 그리기 (고정)
    fig.add_trace(go.Scatter(
        x=[sun_pos[0]], y=[sun_pos[1]],
        mode='markers+text',
        marker=dict(size=40, color='orange', symbol='circle'),
        text=["☀️ 태양"], textposition="top center",
        name="Sun"
    ))
    
    # [수정된 부분] 태양 빛 화살표
    # arrowheads -> arrowhead (수정), opacity 제거 (수정)
    fig.add_annotation(
        x=2, y=0, ax=4, ay=0, 
        showarrow=True, 
        arrowhead=2,    # 여기가 수정되었습니다 (s 제거)
        arrowsize=1, 
        arrowcolor="orange" # opacity 옵션은 제거했습니다
    )

    # 3. 지구 그리기 (고정)
    fig.add_trace(go.Scatter(
        x=[earth_pos[0]], y=[earth_pos[1]],
        mode='markers+text',
        marker=dict(size=20, color='blue', line=dict(color='white', width=1)),
        text=["🌍 지구"], textposition="bottom center",
        name="Earth"
    ))

    # 4. 달 그리기 (변화)
    fig.add_trace(go.Scatter(
        x=[moon_x], y=[moon_y],
        mode='markers+text',
        marker=dict(size=15, color='#F4F6F0'),
        text=["🌕 달"], textposition="top center",
        name="Moon"
    ))

    # 레이아웃 설정
    fig.update_layout(
        title="<b>[우주 관점]</b> 태양-지구-달 위치 관계",
        xaxis=dict(visible=False, range=[-3.5, 6]),
        yaxis=dict(visible=False, range=[-3.5, 3.5]),
        width=400, height=300,
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

# --- 메인 UI 구성 ---

st.title("🔭 중학교 과학: 달의 위상 변화 시뮬레이션")
st.markdown("""
왼쪽 메뉴에서 날짜를 변경하며 **달의 위치(우주 관점)**가 변함에 따라 **달의 모양(지구 관점)**이 어떻게 달라지는지 확인해보세요.
""")

# 사이드바 혹은 상단에 컨트롤 배치
col_control, col_dummy = st.columns([1, 2])
with col_control:
    input_date = st.date_input("📅 날짜 선택", datetime.date.today())

# 데이터 계산
target_datetime = datetime.datetime.combine(input_date, datetime.time(0, 0, 0))
info = get_moon_info(target_datetime)

# 메인 화면 분할 (왼쪽: 우주 관점 / 오른쪽: 지구 관점)
st.divider()

col_space, col_earth = st.columns(2)

with col_space:
    # 우주 관점 그래프
    st.plotly_chart(draw_orbit_diagram(info['angle_rad']), use_container_width=True)
    
    st.info(f"""
    **위치 설명:**
    * 태양은 오른쪽에 고정되어 있습니다.
    * 달은 지구 주위를 반시계 방향으로 공전합니다.
    * 현재 달은 태양으로부터 **{info['degrees']:.0f}도** 돌아간 위치에 있습니다.
    """)

with col_earth:
    # 지구 관점 그래프
    st.plotly_chart(draw_moon_phase(info['illumination'], info['is_waxing']), use_container_width=True)
    
    st.success(f"""
    **관측 정보:**
    * **이름:** {info['phase_name']}
    * **달 뜨는 시각:** {info['rise_str']}
    * **달 지는 시각:** {info['set_str']}
    """)

st.divider()

# 교육적 설명 추가
st.subheader("💡 선생님의 설명")
with st.expander("학생들을 위한 원리 설명 보기 (클릭)", expanded=True):
    st.markdown("""
    1. **삭 (New Moon):** - **위치:** [태양 - 달 - 지구] 순서로 나란히 있습니다. (그래프에서 달이 태양 쪽에 있음)
       - **모양:** 달의 그림자 부분만 지구를 향해 있어서 보이지 않습니다.
       
    2. **상현달 (First Quarter):** - **위치:** 달이 태양-지구 선에서 90도(위쪽) 이동했습니다.
       - **모양:** 오른쪽 반달이 보입니다.
       
    3. **보름달 (Full Moon):** - **위치:** [태양 - 지구 - 달] 순서로 지구가 가운데 있습니다. (달이 태양 반대편)
       - **모양:** 햇빛을 받는 면이 지구를 정면으로 향해 둥글게 보입니다.
    """)
