import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
import plotly.graph_objects as go

# Set the page width using set_page_config
# st.set_page_config(layout="wide")

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'

# 2030세대 데이터 필터링
df_2030 = pd.read_csv('/Users/choejeong-in/Documents/SNU_Team/travel_streamlit/pages/df_2030_data.csv')

# Streamlit 제목
st.title('2030세대 여행경비 시각화 💰💵')

st.markdown("### (요약) 국내여행 평균지출액 현황")

a = df_2030.loc[:, '국내_숙박여부']

# 숙박여행 개수
num_숙박 = (a == '숙박여행').sum()
# 당일여행 개수
num_당일 = (a == '당일여행').sum()

# 전체여행에 대한 평균 지출액
mean_total_전체 = df_2030['NA9'].mean()
# 숙박여행에 대한 평균 지출액
mean_total_숙박 = df_2030[df_2030['국내_숙박여부'] == '숙박여행']['NA9'].mean()
# 당일여행에 대한 평균 지출액
mean_total_당일 = df_2030[df_2030['국내_숙박여부'] == '당일여행']['NA9'].mean()

# creating a single-element container
placeholder = st.empty()

with placeholder.container():

    # create three columns
    kpi1, kpi2, kpi3 = st.columns(3)

    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="1️⃣ 전체여행",
        value="{:,.0f}원".format(round(mean_total_전체)),
    )

    kpi2.metric(
        label="2️⃣ 숙박여행",
        value="{:,.0f}원".format(round(mean_total_숙박)),
    )

    kpi3.metric(
        label="3️⃣ 당일여행",
        value="{:,.0f}원".format(round(mean_total_당일)),
    )

    # Adjust font size using st.write() with Markdown formatting
    st.write("<style>div[role='columnheader'] { font-size: 10px; }</style>", unsafe_allow_html=True)

# 간격을 위한 빈 줄 추가
st.markdown("---")

# App 레이아웃
st.markdown("### 여행유형별/지출항목별 평균비용 비교")

# 선택 상자 (radio) 위젯으로 여행 유형 선택
travel_type = st.radio('여행 유형 선택', ['숙박여행', '당일여행'])

# 숙박여행과 당일여행 비교 그래프 그리기 함수
# 레이블 설정
def draw_plot(travel_type, col1, col2):
    # 한글 폰트 설정
    plt.rcParams['font.family'] = 'AppleGothic'

    # 레이블 설정
    labels = ['숙박비', '음식점비', '식음료비', '교통비', '여행 활동비', '쇼핑비']

    if travel_type == '숙박여행':
        # 숙박여행 데이터 처리
        df_2030_숙박 = df_2030.loc[:, ['NA9C', 'NA9D', 'NA9E', 'NA9F', 'NA9G', 'NA9H']][df_2030['국내_숙박여부'] == '숙박여행']
        column_means_숙박 = df_2030_숙박.mean()  # 내림차순 정렬

        # 막대 그래프 생성 (Seaborn 사용)
        fig_bar, ax_bar = plt.subplots(figsize=(8, 6))
        ax_bar = sns.barplot(x=column_means_숙박.index, y=column_means_숙박, palette='pastel')
        ax_bar.set_title('barplot')
        ax_bar.set_xticklabels(labels, rotation=45, ha='right')  # X 축 레이블 회전
        ax_bar.set_ylabel('(원)')
        ax_bar.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.1f}'))  # Y 축 숫자에 콤마(,) 적용
        for p in ax_bar.patches:
            ax_bar.annotate(f'{p.get_height():,.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')
        col1.pyplot(fig_bar)

        # 숙박여행 파이 차트 생성
        fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
        ax_pie.pie(column_means_숙박, labels=labels, autopct='%.1f%%', colors=sns.color_palette('pastel'))
        ax_pie.set_title('pie chart')
        col2.pyplot(fig_pie)

    if travel_type == '당일여행':
        # 당일여행 데이터 처리
        df_2030_당일 = df_2030.loc[:, ['NA9C', 'NA9D', 'NA9E', 'NA9F', 'NA9G', 'NA9H']][df_2030['국내_숙박여부'] == '당일여행']
        column_means_당일 = df_2030_당일.mean()

        # 막대 그래프 생성 (Seaborn 사용)
        fig_bar, ax_bar = plt.subplots(figsize=(8, 6))
        ax_bar = sns.barplot(x=column_means_당일.index, y=column_means_당일, palette='pastel')
        ax_bar.set_title('barplot')
        ax_bar.set_xticklabels(labels, rotation=45, ha='right')  # X 축 레이블 회전
        ax_bar.set_ylabel('(원)')
        ax_bar.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.1f}'))  # Y 축 숫자에 콤마(,) 적용
        for p in ax_bar.patches:
            ax_bar.annotate(f'{p.get_height():,.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')
        col1.pyplot(fig_bar)

        # 당일여행 파이 차트 생성
        fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
        ax_pie.pie(column_means_당일, labels=labels, autopct='%.1f%%', colors=sns.color_palette('pastel'))
        ax_pie.set_title('pie chart')
        col2.pyplot(fig_pie)


# 2개 컬럼 레이아웃 설정
col1, col2 = st.columns(2)

# 그래프 그리기 함수 호출
draw_plot(travel_type, col1, col2)

# 간격을 위한 빈 줄 추가
st.markdown("---")

"""가장 많은 사람들이 방문하는 강원도 강릉시 방문객들의 경비지출 현황은 어떨까요?"""

st.markdown("### 강릉시 숙박여행 평균지출액 현황")

# 컬럼 설정
col1, col2 = st.columns([2, 1])

# 그래프 그리기 함수
def draw_plot():
    # 한글 폰트 설정
    plt.rcParams['font.family'] = 'AppleGothic'

    # 강릉 숙박여행(방문1일, 2일차 = 강릉)
    df_2030_강릉 = df_2030.loc[:, ['NA9C', 'NA9D', 'NA9E', 'NA9F', 'NA9G', 'NA9H']][(df_2030['국내_숙박여부'] == '숙박여행') & (df_2030['D_TRA1_1_SPOT'] == '강원도 강릉시') & (df_2030['D_TRA1_2_SPOT'] == '강원도 강릉시')]

    # 각 열의 평균 계산
    column_means_강릉 = df_2030_강릉.mean()

    # 그래프 제목, 축 라벨 폰트 설정
    sns.set(style="whitegrid", font='AppleGothic')

    # 첫 번째 컨테이너에 숙박여행 막대 그래프를 표시
    with col1:
        # 막대그래프 생성
        fig_bar2, ax_bar2 = plt.subplots(figsize=(8, 6))  # 차트 크기 조정
        labels = ['숙박비', '음식점비', '식음료비', '교통비', '여행 활동비', '쇼핑비']
        ax_bar2.bar(labels, column_means_강릉, color=sns.color_palette('pastel'))

        # 숫자 레이블 표시
        for i, v in enumerate(column_means_강릉):
            ax_bar2.text(i, v + 5000, f'{int(v):,}', ha='center', va='bottom', fontweight='bold', fontsize=10)

        ax_bar2.set_ylabel('(원)')
        ax_bar2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
        ax_bar2.set_title('2030세대 항목별 여행경비 (강릉여행)')
        ax_bar2.set_xticklabels(labels, rotation=45)
        st.pyplot(fig_bar2)

        # 빈 공간 생성
        st.empty()

    # 두 번째 컨테이너에 숙박여행 파이차트를 표시
    #with col2:
        # 파이차트 생성
        #fig_pie2, ax_pie2 = plt.subplots(figsize=(8, 8))  # 차트 크기 조정
        #labels = ['숙박비', '음식점비', '식음료비', '교통비', '여행 활동비', '쇼핑비']
        #ax_pie2.pie(column_means_강릉, labels=labels, autopct='%.1f%%', colors=sns.color_palette('pastel'))
        #ax_pie2.set_title('2030세대 항목별 여행경비 비율(강릉시)')
        #st.pyplot(fig_pie2)

    # 두 번째 컨테이너에 평균비용을 표시하기

    total = df_2030_강릉['NA9C'].mean() + df_2030_강릉['NA9D'].mean() + df_2030_강릉['NA9E'].mean() + df_2030_강릉['NA9F'].mean() + df_2030_강릉['NA9G'].mean() + df_2030_강릉['NA9H'].mean()

    # 두 번째 컨테이너에 평균비용을 표시하기


    with col2:
        st.markdown("평균비용")
        # 빈 공간 생성하여 열 간격 조정
        st.text("")  # 비어있는 텍스트를 사용하여 간격 추가

        st.markdown("☑ 숙박비 : {:,.0f}원".format(df_2030_강릉['NA9C'].mean()))
        st.markdown("☑ 음식점비 : {:,.0f}원".format(df_2030_강릉['NA9D'].mean()))
        st.markdown("☑ 식음료비 : {:,.0f}원".format(df_2030_강릉['NA9E'].mean()))
        st.markdown("☑ 교통비 : {:,.0f}원".format(df_2030_강릉['NA9F'].mean()))
        st.markdown("☑ 여행 활동비 : {:,.0f}원".format(df_2030_강릉['NA9G'].mean()))
        st.markdown("☑ 쇼핑비 : {:,.0f}원".format(df_2030_강릉['NA9H'].mean()))

        # 빈 공간 생성하여 열 간격 조정
        st.text("")  # 비어있는 텍스트를 사용하여 간격 추가

        # 두 번째 컨테이너에 총 지출 표시
        st.markdown("<p style='font-size: 16px; font-weight: bold;'>총 지출 : {:,.0f}원</p>".format(total), unsafe_allow_html=True)


# 그래프 그리기 함수 호출
draw_plot()

# 간격을 위한 빈 줄 추가
st.markdown("---")

#
st.markdown("### 강릉 vs 전국 평균경비 비교")

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'

# 강릉여행 데이터프레임 생성
df_2030_강릉 = df_2030.loc[:, ['NA9C', 'NA9D', 'NA9E', 'NA9F', 'NA9G', 'NA9H']][(df_2030['국내_숙박여부'] == '숙박여행') & (df_2030['D_TRA1_1_SPOT'] == '강원도 강릉시') & (df_2030['D_TRA1_2_SPOT'] == '강원도 강릉시')]

# 숙박여행 데이터프레임 생성
df_2030_숙박 = df_2030.loc[:, ['NA9C', 'NA9D', 'NA9E', 'NA9F', 'NA9G', 'NA9H']][df_2030['국내_숙박여부'] == '숙박여행']

# 각 열의 평균 계산
column_means_강릉 = df_2030_강릉.mean()
column_means_전국 = df_2030_숙박.mean()

# 평균값을 데이터프레임으로 변환
df_means = pd.DataFrame({'항목': column_means_강릉.index, '강릉': column_means_강릉.values, '전국': column_means_전국.values})

# 데이터를 '강릉'과 '전국'으로 구분하여 쌓지 않고 옆으로 나란히 표시
df_melted = df_means.melt(id_vars='항목', var_name='지역', value_name='평균 비용(원)')

labels = ['숙박비', '음식점비', '식음료비', '교통비', '여행 활동비', '쇼핑비']

# 막대 그래프 생성
plt.figure(figsize=(10, 6))
ax = sns.barplot(x='항목', y='평균 비용(원)', hue='지역', data=df_melted, palette=['skyblue', 'pink'])
plt.xlabel('비용 항목')
plt.ylabel('평균 비용(원)')
plt.title('강릉 vs. 전국 - 항목별 비용 비교')
plt.xticks(range(len(df_means)), labels, rotation=0)
plt.legend(title='지역')

# 막대 그래프의 데이터 레이블 추가
for p in ax.patches:
    ax.annotate(f'{p.get_height():,.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=9, fontweight='bold')

# 세로축 레이블에 천단위 콤마 삽입
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))

st.pyplot(plt)

# 텍스트 출력
st.markdown("강릉시의 경우, 전국 대비 숙박비, 음식점비, 식음료비 항목의 평균비용이 높았으며 반면, 교통비, 여행활동비, 쇼핑비는 평균비용이 적습니다.")
