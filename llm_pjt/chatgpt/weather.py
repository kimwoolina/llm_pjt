import requests
from datetime import datetime


def get_weather_data(service_key, nx='60', ny='127'):
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

    items = data.get('response', {}).get(
        'body', {}).get('items', {}).get('item', [])

    # 각 항목에 대한 설명 추가
    descriptions = {
        'PTY': '강수 형태',
        'REH': '상대 습도 (%)',
        'RN1': '1시간 강수량 (mm)',
        'T1H': '기온 (°C)',
        'UUU': '동서 방향 바람 성분 (m/s)',
        'VEC': '바람 방향 (°)',
        'VVV': '남북 방향 바람 성분 (m/s)',
        'WSD': '바람 속도 (m/s)'
    }

    # 날씨 정보 초기화
    weather_info = {
        'rain': '비 없음',
        'temperature': '온도 정보 없음',
        'humidity': '습도 정보 없음',
        'wind_direction': '바람 방향 정보 없음',
        'wind_speed': '바람 속도 정보 없음'
    }

    # 날씨 정보 추출
    for item in items:
        category = item.get('category')
        value = item.get('obsrValue')

        # 강수 형태 (PTY)
        if category == 'PTY':
            if value == '0':
                weather_info['rain'] = '비 없음'
            elif value == '1':
                weather_info['rain'] = '비'
            elif value == '2':
                weather_info['rain'] = '비/눈'
            elif value == '3':
                weather_info['rain'] = '눈'
            elif value == '5':
                weather_info['rain'] = '빗방울'
            elif value == '6':
                weather_info['rain'] = '빗방울눈날림'
            elif value == '7':
                weather_info['rain'] = '눈날림'
            elif value == '4':  # 소나기 (단기)
                weather_info['rain'] = '소나기'

        # 기온 (T1H)
        if category == 'T1H':
            temp = float(value)
            weather_info['temperature'] = f"{value}°C"  # 기온 그대로 저장
            if temp < 10:
                weather_info['temperature'] = '추운 날씨'
            elif 10 <= temp <= 20:
                weather_info['temperature'] = '선선한 날씨'
            else:
                weather_info['temperature'] = '더운 날씨'

        # 습도 (REH)
        if category == 'REH':
            humidity = int(value)
            weather_info['humidity'] = f"{humidity}%"
            if humidity > 80:
                weather_info['humidity'] = '높은 습도'
            elif 50 <= humidity <= 80:
                weather_info['humidity'] = '중간 습도'
            else:
                weather_info['humidity'] = '낮은 습도'

        # 바람 속도 (WSD)
        if category == 'WSD':
            wind_speed = float(value)
            weather_info['wind_speed'] = f"{wind_speed} m/s"

        # 바람 방향 (VEC)
        if category == 'VEC':
            wind_direction = int(value)
            weather_info['wind_direction'] = f"{wind_direction}°"

        # 1시간 강수량 (RN1)
        if category == 'RN1':
            rain_amount = float(value)
            if rain_amount < 1.0:
                weather_info['rain'] = '1.0mm 미만'
            elif 1.0 <= rain_amount < 30.0:
                weather_info['rain'] = f"{rain_amount:.1f} mm"
            elif 30.0 <= rain_amount < 50.0:
                weather_info['rain'] = '30.0~50.0mm'
            elif rain_amount >= 50.0:
                weather_info['rain'] = '50.0mm 이상'

    return weather_info
