import streamlit as st
import pandas as pd
import altair as alt

# 페이지 설정
st.set_page_config(
    page_title="세계 MBTI 비율 시각화",
    layout="wide"
)

# 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def load_data():
    # CSV 파일 읽기
    df = pd.read_csv('countriesMBTI_16types.csv')
    return df

def main():
    st.title("🌏 국가별 MBTI 유형 분포")
    st.markdown("특정 MBTI 유형을 선택하면, 해당 유형의 비율이 **가장 높은 나라**와 **가장 낮은 나라**를 보여줍니다.")

    # 데이터 불러오기
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("데이터 파일을 찾을 수 없습니다. 'countriesMBTI_16types.csv' 파일이 같은 경로에 있는지 확인해주세요.")
        return

    # MBTI 유형 리스트 추출 (첫 번째 컬럼인 'Country'를 제외한 나머지 컬럼)
    mbti_types = df.columns[1:].tolist()

    # 사이드바 혹은 메인 영역에 선택 박스 배치
    selected_mbti = st.selectbox("MBTI 유형을 선택하세요:", mbti_types)

    if selected_mbti:
        # 선택된 MBTI 기준으로 데이터 정렬 (내림차순)
        df_sorted = df.sort_values(by=selected_mbti, ascending=False)
        
        # 상위 10개국
        top_10 = df_sorted.head(10)
        
        # 하위 10개국 (오름차순 정렬 후 상위 10개 = 즉 하위 10개)
        bottom_10 = df_sorted.tail(10).sort_values(by=selected_mbti, ascending=True)

        # --- 차트 1: 비율이 가장 높은 나라 Top 10 ---
        st.subheader(f"📊 [{selected_mbti}] 비율이 가장 높은 상위 10개국")
        
        chart_top = alt.Chart(top_10).mark_bar().encode(
            x=alt.X(f'{selected_mbti}:Q', title='비율'),
            y=alt.Y('Country:N', sort='-x', title='국가'),
            color=alt.value('#FF6B6B'),  # 붉은 계열 색상
            tooltip=['Country', alt.Tooltip(f'{selected_mbti}:Q', format='.4f')]
        ).properties(
            height=400
        ).interactive() # 줌, 팬 가능하도록 설정

        st.altair_chart(chart_top, use_container_width=True)

        # --- 차트 2: 비율이 가장 적은 나라 Top 10 ---
        st.divider() # 구분선
        st.subheader(f"📉 [{selected_mbti}] 비율이 가장 낮은 하위 10개국")

        chart_bottom = alt.Chart(bottom_10).mark_bar().encode(
            x=alt.X(f'{selected_mbti}:Q', title='비율'),
            y=alt.Y('Country:N', sort='x', title='국가'),
            color=alt.value('#4D96FF'), # 푸른 계열 색상
            tooltip=['Country', alt.Tooltip(f'{selected_mbti}:Q', format='.4f')]
        ).properties(
            height=400
        ).interactive()

        st.altair_chart(chart_bottom, use_container_width=True)

if __name__ == "__main__":
    main()
