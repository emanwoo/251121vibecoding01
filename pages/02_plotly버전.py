import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="국가별 MBTI 비율 분석",
    page_icon="🌍",
    layout="wide"
)

# 데이터 로드 함수 (캐싱을 사용하여 속도 향상)
@st.cache_data
def load_data():
    try:
        # 데이터 파일 읽기
        df = pd.read_csv('countriesMBTI_16types.csv')
        return df
    except FileNotFoundError:
        return None

# 메인 타이틀
st.title("🌍 국가별 MBTI 성격 유형 비율 분석")
st.markdown("이 웹 애플리케이션은 전 세계 국가들의 MBTI 성격 유형 분포를 시각화하여 보여줍니다.")

# 데이터 불러오기
df = load_data()

if df is None:
    st.error("데이터 파일(countriesMBTI_16types.csv)을 찾을 수 없습니다. 앱과 같은 폴더에 파일을 위치시켜 주세요.")
else:
    # MBTI 컬럼 목록 추출 (Country 컬럼 제외)
    mbti_types = df.columns[1:].tolist()

    # 사이드바 (옵션이지만 메인 화면 상단에 배치하는 것이 깔끔할 수 있음, 여기서는 메인 영역 사용)
    st.subheader("분석할 MBTI 유형 선택")
    selected_mbti = st.selectbox("MBTI 유형을 선택하세요:", mbti_types)

    # 선택된 MBTI 기준으로 데이터 정렬
    # 원본 데이터를 훼손하지 않기 위해 복사본 사용
    df_sorted = df.sort_values(by=selected_mbti, ascending=False)

    # --- 시각화 1: 상위 10개국 ---
    top_10 = df_sorted.head(10)
    
    # Plotly 막대 그래프 그리기 (상위)
    fig_top = px.bar(
        top_10,
        x='Country',
        y=selected_mbti,
        title=f"📈 [{selected_mbti}] 비율이 가장 높은 상위 10개국",
        color=selected_mbti,
        color_continuous_scale='Blues', # 파란색 계열
        labels={'Country': '국가', selected_mbti: '비율'},
        text_auto='.3f' # 막대 위에 수치 표시
    )
    
    # 그래프 레이아웃 다듬기
    fig_top.update_layout(
        xaxis_title="국가",
        yaxis_title="비율",
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_top, use_container_width=True)

    st.markdown("---") # 구분선

    # --- 시각화 2: 하위 10개국 ---
    # 하위 10개를 뽑은 뒤, 그래프 가독성을 위해 오름차순으로 다시 정렬
    bottom_10 = df_sorted.tail(10).sort_values(by=selected_mbti, ascending=True)

    # Plotly 막대 그래프 그리기 (하위)
    fig_bottom = px.bar(
        bottom_10,
        x='Country',
        y=selected_mbti,
        title=f"📉 [{selected_mbti}] 비율이 가장 적은 하위 10개국",
        color=selected_mbti,
        color_continuous_scale='Reds', # 붉은색 계열
        labels={'Country': '국가', selected_mbti: '비율'},
        text_auto='.3f'
    )

    # 그래프 레이아웃 다듬기
    fig_bottom.update_layout(
        xaxis_title="국가",
        yaxis_title="비율",
        hovermode="x unified"
    )

    st.plotly_chart(fig_bottom, use_container_width=True)

    # 데이터 출처 표시 (하단)
    st.caption("Data Source: countriesMBTI_16types.csv")
