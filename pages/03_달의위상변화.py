import streamlit as st
import ephem
import math
import datetime
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- 페이지 설정 ---
st.set_page_config(page_title="달의 위상 변화 관찰", layout="wide", page_icon="🌕")

# --- 상수 및 설정 (서울 기준) ---
KST_OFFSET = datetime.timedelta(hours=9)
SEOUL_LAT = '37.5665'
SEOUL_LON = '126.9780'

def get_moon_info(target_date):
    """
    ephem 라이브러리를 사용하여 특정 날짜의 달 정보를 계산합니다.
    """
    observer = ephem.Observer()
    observer.lat = SEOUL_LAT
    observer.lon = SEOUL_LON
    observer.elevation = 0
    
    # 날짜 설정 (자정 기준)
    observer.date = target_date - datetime.timedelta(hours=9) # UTC 변환
    
    moon = ephem.Moon()
    sun = ephem.Sun()
    moon.compute(observer)
    sun.compute(observer)
    
    # 1. 월령 (Moon Age) 및 위상(Phase - 조명도 0~100)
    # ephem의 moon.phase는 조명도(%)를 의미합니다.
    illumination = moon.phase 
    
    # 2. 삭망월 기준 위치 (달의 황경 - 태양의 황경)
    # 이 값이 0~180도면 차오르는 달(Waxing), 180~360도면 기우는 달(Waning)
    lon_diff = (moon.hlon - sun.hlon) % (2 * math.pi)
    degrees = math.degrees(lon_diff)
    
    is_waxing = 0 <= degrees < 180
    
    # 3. 뜨고 지는 시각 계산
    try:
        rise_time = observer.next_rising(moon).datetime() + KST_OFFSET
        set_time = observer.next_setting(moon).datetime() + KST_OFFSET
        # 시각 포맷팅
        rise_str = rise_time.strftime("%H시 %M분")
        set_str = set_time.strftime("%H시 %M분")
    except:
        rise_str = "--:--"
        set_str = "--:--"

    # 4. 달의 이름 결정 (대략적 구분)
    phase_name = ""
    if illumination < 2:
        phase_name = "삭 (New Moon)"
    elif illumination > 98:
        phase_name = "보름달 (Full Moon)"
    elif is_waxing:
        if illumination < 45:
            phase_name = "초승달 (Waxing Crescent)"
        elif illumination < 55:
            phase_name = "상현달 (First Quarter)"
        else:
            phase_name = "차오르는 凸달 (Waxing Gibbous)"
    else: # Waning
        if illumination < 45:
            phase_name = "그믐달 (Waning Crescent)"
        elif illumination < 55:
            phase_name = "하현달 (Last Quarter)"
        else:
            phase_name = "기우는 凸달 (Waning Gibbous)"

    return {
        "illumination": illumination,
        "degrees": degrees,
        "is_waxing": is_waxing,
        "rise_str": rise_str,
        "set_str": set_str,
        "phase_name": phase_name,
        "date_str": target_date.strftime("%Y년 %m월 %d일")
    }

def draw_moon_phase(illumination, is_waxing):
    """
    Plotly를 사용하여 달의 위상을 시각화합니다.
    원과 타원을 이용하여 2D 위상 변화를 시뮬레이션합니다.
    """
    
    # 달의 반지름
    r = 10 
    
    # 배경 (어두운 달)
    fig = go.Figure()
    
    # 1. 달의 기본 원 (어두운 색)
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-r, y0=-r, x1=r, y1=r,
        fillcolor="black", line_color="gray", line_width=1,
        layer="below"
    )

    # 2. 빛나는 부분 계산 (수학적 모델링)
    # 조명도(0~100)를 0~2 범위의 비율로 변환 (반지름 대비 너비)
    # illumination 0 -> w=0, 50 -> w=1(반원), 100 -> w=2(전체)
    
    # x, y 좌표 생성
    t = np.linspace(0, np.pi, 100)
    x_edge = r * np.cos(t) # 외곽선
    y_edge = r * np.sin(t)
    
    # 위상에 따른 내부 경계선 (타원 방정식 활용)
    # 조명도(p)를 0.0 ~ 1.0으로 정규화
    p = illumination / 100.0
    
    # 시각적 너비 계산 (Terminator line offset)
    # full moon(1.0) -> offset = -r
    # new moon(0.0) -> offset = r
    # half moon(0.5) -> offset = 0
    offset = -r * (2 * p - 1)

    # 오른쪽이 밝은지 왼쪽이 밝은지 결정
    # Waxing(차오름): 오른쪽이 밝음 (상현)
    # Waning(기움): 왼쪽이 밝음 (하현)
    
    # 다각형 좌표 구성
    if is_waxing:
        # 오른쪽이 빛남
        # 외곽선: 오른쪽 반원 (-pi/2 to pi/2)
        theta = np.linspace(-np.pi/2, np.pi/2, 100)
        x_outer = r * np.cos(theta)
        y_outer = r * np.sin(theta)
        
        # 내부 경계선 (타원)
        x_inner = offset * np.cos(theta)
        
        # 합치기
        x_poly = np.concatenate([x_outer, x_inner[::-1]])
        y_poly = np.concatenate([y_outer, y_outer[::-1]])
        
    else:
        # 왼쪽이 빛남
        # 외곽선: 왼쪽 반원 (pi/2 to 3pi/2)
        theta = np.linspace(np.pi/2, 3*np.pi/2, 100)
        x_outer = r * np.cos(theta)
        y_outer = r * np.sin(theta)
        
        # 내부 경계선 (타원)
        x_inner = offset * np.cos(theta) # offset 부호 주의
        
        # 합치기
        x_poly = np.concatenate([x_outer, x_inner[::-1]])
        y_poly = np.concatenate([y_outer, y_outer[::-1]])

    # 빛나는 부분 그리기
    fig.add_trace(go.Scatter(
        x=x_poly, y=y_poly,
        fill="toself",
        fillcolor="#F4F6F0", # 달 색상 (약간의 미색)
        line=dict(color="#F4F6F0", width=0),
        hoverinfo="skip"
    ))

    # 그래프 레이아웃 설정
    fig.update_layout(
        title=dict(text="오늘의 달 모양", font=dict(size=20)),
        xaxis=dict(range=[-12, 12], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-12, 12], showgrid=False, zeroline=False, visible=False),
        width=400, height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# --- 메인 UI ---

st.title("🌗 중학교 과학: 달의 위상 변화")
st.markdown("날짜를 선택하면 그날 밤 **서울 하늘**에서 볼 수 있는 달의 모양과 정보를 알려줍니다.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📅 날짜 선택")
    # 오늘 날짜 기본 설정
    input_date = st.date_input("확인하고 싶은 날짜를 선택하세요", datetime.date.today())
    
    # 계산 수행
    target_datetime = datetime.datetime.combine(input_date, datetime.time(0, 0, 0))
    info = get_moon_info(target_datetime)
    
    st.divider()
    
    st.markdown(f"### **{info['phase_name']}**")
    st.markdown(f"**밝기(조명도):** {info['illumination']:.1f}%")
    
    # 상식 팁 표시
    if info['illumination'] < 2:
        st.info("💡 **Tip:** 삭일 때는 달이 태양과 같은 방향에 있어 지구에서 보이지 않아요.")
    elif info['illumination'] > 98:
        st.success("💡 **Tip:** 보름달이 뜨는 날입니다! 밤새도록 밝은 달을 볼 수 있어요.")
    elif info['phase_name'].startswith("상현"):
        st.info("💡 **Tip:** 상현달은 초저녁에 남쪽 하늘에서 볼 수 있고 자정쯤 서쪽으로 져요.")
    elif info['phase_name'].startswith("하현"):
        st.info("💡 **Tip:** 하현달은 자정쯤 동쪽에서 떠서 아침에 남쪽 하늘에 보여요.")

    st.divider()
    st.write("📍 **서울 기준 관측 시간**")
    st.write(f"🌅 **달 뜨는 시각:** {info['rise_str']}")
    st.write(f"🌄 **달 지는 시각:** {info['set_str']}")

with col2:
    # Plotly 그래프 표시
    fig = draw_moon_phase(info['illumination'], info['is_waxing'])
    st.plotly_chart(fig, use_container_width=True)

# --- 추가 교육용 설명 ---
st.divider()
st.subheader("📚 달의 위상이 변하는 이유")
st.write("""
달은 스스로 빛을 내지 못하고 태양 빛을 반사하여 빛납니다. 
지구 주위를 공전하면서 태양, 지구, 달의 위치 관계가 달라지기 때문에 
지구에서 보는 우리에게는 달의 밝은 부분의 모양이 매일 조금씩 다르게 보입니다.
""")

with st.expander("더 자세한 원리 보기"):
    st.markdown("""
    * **삭 (New Moon):** 태양 - 달 - 지구 순서일 때. 달의 어두운 면이 지구를 향해 보이지 않음.
    * **상현달 (First Quarter):** 달이 태양의 동쪽으로 90도 떨어져 있을 때. 오른쪽 반이 보임.
    * **망 (Full Moon):** 태양 - 지구 - 달 순서일 때. 달의 전면이 햇빛을 받아 둥글게 보임.
    * **하현달 (Last Quarter):** 달이 태양의 서쪽으로 90도 떨어져 있을 때. 왼쪽 반이 보임.
    """)
