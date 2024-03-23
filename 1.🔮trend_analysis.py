#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def generate_word_cloud(final_data):
    text = ','.join(final_data)
    wordcloud = WordCloud(font_path='/path/to/AppleGothic.ttf', background_color='white').generate(text)

    # Display the generated image using Streamlit
    st.image(wordcloud.to_array(), use_column_width=True)

def main():
    from matplotlib import rc
    rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False

    st.title("네이버 블로그 텍스트 분석")

    # Load data from the pickled file
    try:
        with open('data.pickle', 'rb') as f:
            final_data = pickle.load(f)
    except FileNotFoundError:
        st.warning("Data file 'data.pickle' not found. Please make sure the file exists.")
        return

    if not final_data:
        st.warning("The loaded data is empty.")
        return

    # Generate and display the word cloud
    st.subheader("Wordcloud 시각화")
    st.text('블로그에서 언급된 명사들을 Wordcloud로 시각화하였습니다.')
    generate_word_cloud(final_data)

    st.markdown("---")
    
    st.subheader("LDA 토픽모델링 시각화")
    st.text('비슷한 토픽을 가진 블로그 글들을 군집화하여 시각화하였습니다.')
    pyldavis_html_file = 'lda.html'
    with open(pyldavis_html_file, 'r', encoding='utf-8') as f:
        pyldavis_html = f.read()

    st.components.v1.html(pyldavis_html, width = 1210, height = 780)

if __name__ == "__main__":
    main()
    
