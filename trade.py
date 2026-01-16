import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="2024 대한민국 무역 대시보드", layout="wide")

# 1. 대한민국 전체 무역 통계 섹션
# [수정] 맨 위 텍스트 변경
st.title("2024 대한민국 무역 수치 📈")
# [수정] 문구 변경: 대한민국 무역 수치 + 이모티콘
st.subheader("대한민국 무역 수치 요약 📦✨")

# 주요 지표 (Metric 카드)
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric("총 수출액 (2024년)", "6,838억 달러", "+8.2%") 
with col_m2:
    st.metric("총 수입액 (2024년)", "6,320억 달러", "-1.6%") 
with col_m3:
    st.metric("무역수지 (흑자)", "518억 달러", "최대 규모") 

# --- [추가] 대한민국 전체 무역 성적표 상세 표 ---
st.markdown("#### 📊 2024 대한민국 무역 성적표 (종합)")
general_trade_summary = pd.DataFrame({
    "구분": ["최대 수출국", "최대 수입국", "수출 1위 품목", "수출 2위 품목", "주요 성장 동력"],
    "상세 내용": ["중국 ($1,330억)", "중국 ($1,428억)", "반도체 ($1,419억)", "자동차 ($709억)", "반도체 및 선박 수출 급증"],
    "상태": ["🥇 1위 유지", "🥈 미국 근접", "🚀 역대 최대", "💎 견고한 성장", "📈 흑자 전환 견인"]
})
st.table(general_trade_summary)

st.divider()

# 2. 엑셀 기반 특정 품목 데이터 분석 섹션
# [확인된 품목명 반영] 자동차 제동장치 및 그 부분품 (HS Code: 870830)
st.subheader("🔍 특정 품목 세부 분석 (엑셀 파일 기준)")
st.info("💡 이 섹션의 데이터는 **자동차 제동장치 및 그 부분품 (HS Code: 870830)**에 한정된 수치입니다.")

file_path = '해외유망시장추천_20260116145225.xlsx'

def clean_data(df):
    """데이터 제목 정리 및 숫자 형변환"""
    if 'Unnamed' in str(df.columns):
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)
    
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(',', '').str.strip()
            df[col] = df[col].str.replace('%', '')
        
        converted = pd.to_numeric(df[col], errors='coerce')
        if not converted.isna().all():
            df[col] = converted
            
    return df

try:
    # 엑셀 데이터 로드
    df_raw = pd.read_excel(file_path, sheet_name='수출입 통계')
    df = clean_data(df_raw)
    
    # 국가 데이터만 필터링
    df_clean = df[~df['수입국'].isin(['한국', '-', '전체'])].copy()
    df_clean = df_clean.dropna(subset=['순위'])

    # 시각화 레이아웃
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.write("📌 **제동장치 품목 수입액 Top 10**")
        top10_import = df_clean.nlargest(10, '수입액(천$)')
        fig_import = px.bar(top10_import, x='수입국', y='수입액(천$)', 
                            color='수입액(천$)', color_continuous_scale='Reds',
                            labels={'수입액(천$)': '수입액 ($)'})
        st.plotly_chart(fig_import, use_container_width=True)

    with col_chart2:
        st.write("📌 **제동장치 품목 수출액 Top 10**")
        top10_export = df_clean.nlargest(10, '수출액(천$)')
        fig_export = px.bar(top10_export, x='수입국', y='수출액(천$)', 
                            color='수출액(천$)', color_continuous_scale='Blues',
                            labels={'수출액(천$)': '수출액 ($)'})
        st.plotly_chart(fig_export, use_container_width=True)

except Exception as e:
    st.error(f"엑셀 데이터를 읽는 중 오류가 발생했습니다: {e}")