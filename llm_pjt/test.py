from llm_pjt.settings import SERVICE_KEY
import requests

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'

# 현재 날짜와 시간을 기준으로 base_date와 base_time 설정
from datetime import datetime
now = datetime.now()
base_date = now.strftime('%Y%m%d')
base_time = now.strftime('%H%M')

params = {
    'serviceKey': SERVICE_KEY,
    'pageNo': '1',
    'numOfRows': '1000',
    'dataType': 'JSON',
    'base_date': base_date,
    'base_time': base_time,
    'nx': '55',
    'ny': '127'
}

response = requests.get(url, params=params)
data = response.json()  # JSON 형식으로 변환

# 필요한 데이터 추출
items = data['response']['body']['items']['item']

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

for item in items:
    base_date = item['baseDate']
    base_time = item['baseTime']
    category = item['category']
    obsr_value = item['obsrValue']
    
    description = descriptions.get(category, '설명 없음')
    print(f"Date: {base_date}, Time: {base_time}, Category: {description}, Value: {obsr_value}")
