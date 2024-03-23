import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
st.set_option('deprecation.showPyplotGlobalUse', False)

# Load the data for df_pay from the CSV file (Replace 'data_2030.csv' with the actual filename)
df_pay = pd.read_csv('/Users/choejeong-in/Documents/SNU_Team/travel_streamlit/pages/df_pay.csv')

# Create the Streamlit app
st.title('여행지출 분포')
st.subheader('소득별 여행지출')

# Create a 1x2 grid of subplots
fig, axes = plt.subplots(1, 2, figsize=(13, 6))  # Adjust figsize as per your preference

# First subplot - Violin plot for '본인소득: DQ6A' vs. '지출액: NA9'
sns.violinplot(x=df_pay['DQ6A'], y=df_pay['NA9'], alpha=0.5, ax=axes[0])
axes[0].set_title('Violin Plot: 개인소득 vs. 여행지출')
axes[0].set_xlabel('개인소득')
axes[0].set_ylabel('지출액')
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45, ha='right')  # Rotate x-axis labels by 45 degrees and align them to the right

# Second subplot - Violin plot for '가구소득: DQ6B' vs. '지출액: NA9'
sns.violinplot(x=df_pay['DQ6B'], y=df_pay['NA9'], alpha=0.5, ax=axes[1])
axes[1].set_title('Violin Plot: 가구소득 vs. 여행지출')
axes[1].set_xlabel('가구소득')
axes[1].set_ylabel('지출액')
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45, ha='right')  # Rotate x-axis labels by 45 degrees and align them to the right

plt.tight_layout()  # Adjust the spacing between subplots for better visualization

# Display the plots using Streamlit's st.pyplot() function
st.pyplot(fig)

df_pay = df_pay.rename(columns={
    'DQ6A': '월 평균 개인소득',
    'DQ6B': '월 평균 가구소득',
    'BINC1': '개인소득',
    'BINC2': '가구소득',
    'NA9': '여행 경비 지출'
})

# Display the DataFrame df_pay
st.dataframe(df_pay)



# Load the data
df_20 = pd.read_csv('/Users/choejeong-in/Documents/SNU_Team/travel_streamlit/pages/df_20.csv')  # Replace 'data_20.csv' with the actual filename for 20s data
df_30 = pd.read_csv('/Users/choejeong-in/Documents/SNU_Team/travel_streamlit/pages/df_30.csv')  # Replace 'data_30.csv' with the actual filename for 30s data


# Create a function to plot the violin plot
def plot_violin_plot(df, title):
    plt.rcParams['font.family'] = 'AppleGothic'
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.violinplot(data=df, y='NA9', color='skyblue', alpha=0.7)
    ax.set_xlabel(title)
    ax.set_ylabel('여행지출')
    ax.set_title(f'{title} 여행지출 바이올린 플롯')
    ax.grid(True)
    return fig

# Plot violin plots for age group 20s and 30s
st.subheader('20대 여행지출')
fig_20 = plot_violin_plot(df_20, '20대')
st.pyplot(fig_20)

st.subheader('30대 여행지출')
fig_30 = plot_violin_plot(df_30, '30대')
st.pyplot(fig_30)
