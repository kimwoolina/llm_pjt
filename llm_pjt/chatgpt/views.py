from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .weather import get_weather_data
from .bots import ask_chatgpt
from .prompts import prompt, create_system_instructions
import os
import json
import logging

logger = logging.getLogger(__name__)

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



class WeatherChatAPIView(APIView):
    def get(self, request):
        user_message = request.GET.get("message")

        if not user_message:
            return Response({"error": "메시지를 제공해 주세요."}, status=400)

        # ChatGPT에 메시지 전송하여 위치 추출
        try:
            chatgpt_response = ask_chatgpt(user_message, prompt)
        except Exception as e:
            logger.error(f"ChatGPT 요청 실패: {str(e)}")
            return Response({"error": "정보를 가져오는 중 문제가 발생했습니다."}, status=500)
        
        # 위치 이름 추출
        location_name = chatgpt_response

        # 위치 좌표 찾기
        location_coords = find_location_coordinates(location_name)
        if not location_coords:
            return Response({"message": chatgpt_response})
        
        print("location_coords: " , location_coords)
        
        # 날씨 정보 가져오기
        try:
            weather_info = get_weather_data(settings.SERVICE_KEY, 
                                            nx=location_coords['x'], 
                                            ny=location_coords['y'])
            
            # 시스템 안내 메시지 생성
            system_instructions = create_system_instructions(weather_info)

            # ChatGPT에 메시지 전송
            try:
                chatgpt_response = ask_chatgpt(user_message, system_instructions)
            except Exception as e:
                logger.error(f"ChatGPT 요청 실패: {str(e)}")
                return Response({"error": "날씨 정보를 가져오는 중 문제가 발생했습니다."}, status=500)

            return Response({"message": chatgpt_response})
        except Exception as e:
            logger.error(f"날씨 데이터 요청 실패: {str(e)}")
            return Response({"error": "날씨 정보를 가져오는 중 문제가 발생했습니다."}, status=500)