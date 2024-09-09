import json
import os
from .weather import get_weather_data

# 좌표 정보 json 파일 불러오기
def load_location_data():
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'locations.json')
    
    # JSON 파일 읽기
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


# 위치 좌표 찾기
def find_location_coordinates(location_name):
    location_data = load_location_data()
    
    # 지역 이름에 location_name이 포함된 경우 검색
    for location in location_data:
        if location_name in location['name']:  # 부분 문자열이 포함되면 True
            return location  # 일치하는 첫 번째 지역 좌표 반환
        
    return None # 일치하는 지역이 없을 경우

def get_weather_info(service_key, nx, ny):
    return get_weather_data(service_key, nx, ny)
