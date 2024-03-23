# 필요 모듈 import
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import streamlit as st


# 데이터 로드 및 전처리
out_gr = pd.read_csv('최종_관광지_맛집 .csv')

category_mapping = {
    '시장': '쇼핑',
    '자연경관(하천/해양)': '자연 및 풍경',
    '호텔': '숙박',
    '대형마트': '쇼핑',
    '전시시설': '역사 유적지',
    '역사유적지': '역사 유적지',
    '복합관광시설': '관광',
    '콘도미니엄': '숙박',
    '기타문화관광지': '관광',
    '농/산/어촌체험': '문화예술',
    '기타레저스포츠': '레포츠 활동',
    '도시공원': '공원',
    '랜드마크관광': '관광',
    '캠핑': '숙박',
    '교통시설': '교통',
    '육상레저스포츠': '레포츠 활동',
    '테마공원': '공원',
    '데이트코스': '관광',
    '기타관광': '관광',
    '자연공원': '공원',
    '펜션/민박': '숙박',
    '자연경관(산)': '자연 및 풍경',
    '모텔': '숙박',
    '공연시설': '문화예술',
    '음식점': '음식점'
}

out_gr['분류'] = out_gr['분류'].map(category_mapping)

# 색상 설정
category_colors = {
    '쇼핑': 'red',
    '자연 및 풍경': 'blue',
    '숙박': 'green',
    '역사 유적지': 'orange',
    '관광': 'purple',
    '문화예술': 'pink',
    '레포츠 활동': 'lightgreen',
    '공원': 'lightblue',
    '교통': 'gray',
    '음식점': 'black'
}

# 지도 생성 함수
def create_map(data, recommended_coords=None):

    # 지도의 중심 위치 설정
    center_lat, center_lon = 37.796503,128.92884
    map = folium.Map(location=[center_lat, center_lon], zoom_start=10.5)

    # 마커 클러스터 생성
    marker_cluster = MarkerCluster()

    # 데이터프레임 순회하며 마커 추가
    for index, row in data.iterrows():
        lat, lon = row['위도'], row['경도']
        name = row['관광지명']
        address = row['주소']
        category = row['분류']

        # 분류별 색상 선택
        color = category_colors.get(category, 'gold')

        # 마커 생성
        popup_content = f"<div style='font-size: 14px;'><b>{name}</b></div><div><b>주소:</b> {address}</div><div><b>분류:</b> {category}</div>"
        icon = folium.Icon(color=color, icon='info-sign')
        marker = folium.Marker(location=[lat, lon], popup=folium.Popup(popup_content, max_width=300), icon=icon)

        # 마커를 지도에 추가
        map.add_child(marker)

    # 추천 여행지를 지도에 선으로 연결
    if recommended_coords:
        # 선 연결 (빨간선)
        folium.PolyLine(locations=recommended_coords[:len(fir_course)], color='red', weight=2).add_to(map)
        # 선 연결 (파란선)
        folium.PolyLine(locations=recommended_coords[len(fir_course)-1:], color='blue', weight=2).add_to(map)

    # 색깔 범주표 생성
    legend_html = f'''
    <div style="position: fixed;
                 top: 5px; right: 5px; width: auto; padding:0 5px; max-height: 400px; overflow-y: auto;
                 border:2px solid grey; z-index:9999; font-size:14px;
                 background-color: white;
                 opacity: 0.9;
                 ">
      <h4 style="font-size:16px; font-weight:bold">Marker Colors</h4>
      <div style="display:block">
        {''.join([f"<div style='padding:0 3px'><i class='fa fa-map-marker fa-2x' style='color:{color}'></i> {category}<br></div>" for category, color in category_colors.items()])}
      </div>
    </div>
    '''

    map.get_root().html.add_child(folium.Element(legend_html))

    # 색깔 범주표 생성
    legend_html_line = f'''
    <div style="position: fixed;
             top: 5px; right: 131px; width: auto; padding:0 5px; max-height: 400px; overflow-y: auto;
             border:2px solid grey; z-index:9999; font-size:14px;
             background-color: white;
             opacity: 0.9;
             ">
    <h4 style="font-size:16px; font-weight:bold">Line Colors</h4>
    <div style="display:block">
        <div style='padding:0 3px'><i class='fa fa-long-arrow-alt-right fa-2x' style='color:red'></i> 1일차 (Day 1)<br></div>
        <div style='padding:0 3px'><i class='fa fa-long-arrow-alt-right fa-2x' style='color:blue'></i> 2일차 (Day 2)<br></div>
    </div>
    </div>
    '''
    map.get_root().html.add_child(folium.Element(legend_html_line))

    return map

# Streamlit 앱 실행
if __name__ == "__main__":
    st.title("1박 2일 강릉 여행 일정")

    # 추천 관광지 리스트
    fir_course = ['주문진항', '주문진수산시장', '도깨비촬영지(영진해변)', '경포대', '호텔아비오']
    sec_course = ['정동진해돋이공원','하슬라아트월드','머구리횟집', '안목해변','강릉중앙시장']
 
    recommended_course = fir_course + sec_course

    # 추천 관광지의 위도, 경도 정보를 가져오기
    recommended_coords = []
    for place in recommended_course:
        place_data = out_gr[out_gr['관광지명'] == place][['위도', '경도']]
        if not place_data.empty:
            recommended_coords.append(tuple(place_data.values[0]))

    # 추천 관광지만 지도에 표시
    filtered_out_gr = out_gr[out_gr['관광지명'].isin(recommended_course)]

    # 지도 생성 및 렌더링   
    map = create_map(filtered_out_gr, recommended_coords)


    # 마커에 숫자 추가
    for i, coord in enumerate(recommended_coords):
        if i < 5:
            number_icon = folium.DivIcon(html=f"<div style='font-size: 14px; color: white; background-color: red; border-radius: 50%; width: 24px; height: 24px; display: flex; justify-content: center; align-items: center;'>{i + 1}</div>")
        else:
            number_icon = folium.DivIcon(html=f"<div style='font-size: 14px; color: white; background-color: blue; border-radius: 50%; width: 24px; height: 24px; display: flex; justify-content: center; align-items: center;'>{i + 1}</div>")
        folium.Marker(location=coord, icon=number_icon).add_to(map) 


    # 지도를 HTML로 렌더링
    map_html = map._repr_html_()
    # st.components.v1.html(map_html, width=800, height=600)

    # 제목과 데이터프레임 사이에 간격 추가
    st.markdown("<br>", unsafe_allow_html=True)

    # 관광지명 데이터프레임 생성
    itinerary_df = pd.DataFrame({'Num': range(1, len(recommended_course) + 1), 'Place': recommended_course})


    day_1 = ['1일차','1일차','1일차','1일차','1일차','2일차','2일차','2일차','2일차','2일차']
    schedule = ['오전','점심','오후1','오후2','숙소','오전1','오전2','점심','오후1','오후2']

    itinerary_df['Day'] = day_1
    itinerary_df['Schedule'] = schedule

    # itinerary_table_html = itinerary_df.to_html(index=False, border=1, justify='center')
    itinerary_df.index = range(1, len(itinerary_df) + 1)
    st.dataframe(itinerary_df[['Day','Schedule','Place']])
    


    st.components.v1.html(map_html, width=800, height=600)

