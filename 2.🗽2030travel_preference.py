import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# 데이터 불러오기
# df = pd.read_spss('DATA_2022년 국민여행조사.sav')
df = pd.read_csv('/Users/choejeong-in/Documents/SNU_Team/travel_streamlit/pages/df_2030.csv')

# 필요한 컬럼 추출
aa = df['D_TRA1_1_SPOT'].dropna()
aa = pd.DataFrame(aa)
aa.reset_index(inplace=True)
aa = aa.dropna()

# 컬럼명 변경
aa.columns = ['index', 'D_TRA1_1_SPOT']

# value_counts 계산
item_counts = aa['D_TRA1_1_SPOT'].value_counts()
item_counts_sort = item_counts.sort_values(ascending=False)

top_10_TRA1_1_SPOT = item_counts_sort[:10]

# Streamlit 앱 생성
st.title('20-30대 연령대의 여행자들이 선호하는 1박 2일 여행지')

# 방사형 막대 그래프 그리기
fig = go.Figure()

fig.add_trace(go.Barpolar(
    r=top_10_TRA1_1_SPOT.values,
    theta=top_10_TRA1_1_SPOT.index,
    marker_color='rgb(26, 118, 255)',
    marker_line_color='rgb(8, 48, 107)',
    marker_line_width=1.5,
    opacity=0.7,
    base=0
))

# 데이터표 출력
# st.header('20-30대가  데이터표')
top_10_TRA1_1_SPOT_df = top_10_TRA1_1_SPOT.reset_index()
top_10_TRA1_1_SPOT_df.columns = ['지역명', '빈도수']  # 컬럼 이름 변경
st.table(top_10_TRA1_1_SPOT_df)

fig.update_layout(
    title='1박 2일 여행지 데이터 비율',
    font_size=12,
    polar_angularaxis=dict(direction='clockwise')
)



# 방사형 막대 그래프 시각화
st.plotly_chart(fig)


