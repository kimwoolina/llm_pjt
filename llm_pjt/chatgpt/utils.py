import json
import os
from django.core.cache import cache
from django.conf import settings
from .weather import get_weather_data

# 캐시 키
CACHE_KEY = 'location_data'

# 위치 데이터 캐시 저장
def cache_set(key, value):
    cache.set(key, json.dumps(value), timeout=3600)  # 1시간 동안 캐시 저장

# 위치 데이터 캐시 가져오기
def cache_get(key):
    data = cache.get(key)
    return json.loads(data) if data else None

# 위치 좌표 찾기
def find_location_coordinates(location_name):
    # 캐시에서 위치 데이터 가져오기
    location_data = cache_get(CACHE_KEY)
    
    if not location_data:
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'locations.json')
        # JSON 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as file:
            location_data = json.load(file)
        # 캐시 저장
        cache_set(CACHE_KEY, location_data)

    # 위치 데이터에서 지역 이름 검색
    for location in location_data:
        if location_name in location['name']:  # 부분 문자열이 포함되면 True
            return location  # 일치하는 첫 번째 지역 좌표 반환
        
    return None  # 일치하는 지역이 없을 경우

def get_weather_info(service_key, nx, ny):
    return get_weather_data(service_key, nx, ny)
