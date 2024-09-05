# weather.py
import requests
from datetime import datetime

def get_weather_data(service_key, nx='55', ny='127'):
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
    
    now = datetime.now()
    base_date = now.strftime('%Y%m%d')
    base_time = now.strftime('%H%M')
    
    params = {
        'serviceKey': service_key,
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'JSON',
        'base_date': base_date,
        'base_time': base_time,
        'nx': nx,
        'ny': ny
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    items = data['response']['body']['items']['item']
    
    # 날씨 정보 추출
    weather_info = {
        'rain': '비 없음',
        'temperature': '온도 정보 없음',
        'humidity': '습도 정보 없음'
    }
    
    for item in items:
        category = item['category']
        value = item['obsrValue']
        
        if category == 'PTY' and value != '0':
            weather_info['rain'] = '비가 내림'
        if category == 'T1H':
            temp = float(value)
            if temp < 10:
                weather_info['temperature'] = '추운 날씨'
            elif 10 <= temp <= 20:
                weather_info['temperature'] = '선선한 날씨'
            else:
                weather_info['temperature'] = '더운 날씨'
        if category == 'REH':
            humidity = int(value)
            if humidity > 80:
                weather_info['humidity'] = '높은 습도'
            elif 50 <= humidity <= 80:
                weather_info['humidity'] = '중간 습도'
            else:
                weather_info['humidity'] = '낮은 습도'
    
    return weather_info
