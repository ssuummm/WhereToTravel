# 필요 모듈 import
import pandas as pd
import folium
from folium.plugins import MarkerCluster, MiniMap
import streamlit as st

# 데이터 로드 및 전처리
out_gr = pd.read_csv('최종_외지인.csv')
 
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
    '공연시설': '문화예술'
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
    '교통': 'gray'
}

# 지도 생성 함수
def create_map(data):

    # 지도의 중심 위치 설정
    center_lat, center_lon = 37.7520, 128.8751
    map = folium.Map(location=[center_lat, center_lon], zoom_start=10)

    # 마커 클러스터 생성
    marker_cluster = MarkerCluster()

    # 데이터프레임 순회하며 마커 추가
    for index, row in data.iterrows():
        lat, lon = row['위도'], row['경도']
        name = row['관광지명']
        address = row['주소']
        category = row['분류']
        search_count = row['외지인 검색 수']

        # 분류별 색상 선택
        color = category_colors.get(category, 'gray')


        # 마커 생성
        popup_content = f"<div style='font-size: 14px;'><b>{name}</b></div><div><b>주소:</b> {address}</div><div><b>분류:</b> {category}</div>"
        icon = folium.Icon(color=color, icon='info-sign')
        marker = folium.Marker(location=[lat, lon], popup=folium.Popup(popup_content, max_width=300), icon=icon)

        # 마커를 클러스터에 추가
        marker_cluster.add_child(marker)

    # 클러스터를 지도에 추가
    map.add_child(marker_cluster)

    # 색깔 범주표 생성
    legend_html = f'''
    <div style="position: fixed;
                 top: 10px; right: 10px; width: auto; padding:0 10px; max-height: 310px; overflow-y: auto;
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
    # map.save('test.html')

    return map

# Streamlit 앱 실행
if __name__ == "__main__":
    st.title("강릉 인기 관광지 Top 100")

    # 카테고리 선택 위젯 생성
    selected_category = st.multiselect(
        "카테고리를 선택하세요", out_gr['분류'].unique(), default=out_gr['분류'].unique()
    )

    # 선택한 카테고리에 해당하는 데이터프레임 필터링
    filtered_out_gr = out_gr[out_gr['분류'].isin(selected_category)]

    # 데이터프레임 테이블로 보여주기
    st.dataframe(filtered_out_gr[['순위', '관광지명', '주소', '분류']], hide_index=True)

    # 지도 생성 및 렌더링
    map = create_map(filtered_out_gr)

    map.save('강릉 인기 여행지.html')

    map_html = open('강릉 인기 여행지.html', 'r', encoding='utf-8').read()
    st.components.v1.html(map_html, width=800, height=600)