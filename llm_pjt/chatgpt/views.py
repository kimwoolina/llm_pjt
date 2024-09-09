from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .utils import find_location_coordinates, get_weather_info
from .bots import ask_chatgpt
from .prompts import prompt, create_system_instructions
from .serializers import WeatherInfoSerializer
import logging

logger = logging.getLogger(__name__)

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

        # 날씨 정보 가져오기
        try:
            weather_info = get_weather_info(settings.SERVICE_KEY, 
                                            nx=location_coords['x'], 
                                            ny=location_coords['y'])
            
            # Serializer 사용
            serializer = WeatherInfoSerializer(weather_info)
            weather_info_data = serializer.data
            
            # ChatGPT에 날씨 정보 전송
            try:
                chatgpt_response = ask_chatgpt(user_message, create_system_instructions(weather_info_data))
            except Exception as e:
                logger.error(f"ChatGPT 요청 실패: {str(e)}")
                return Response({"error": "날씨 정보를 가져오는 중 문제가 발생했습니다."}, status=500)

            return Response({"message": chatgpt_response})
        except Exception as e:
            logger.error(f"날씨 데이터 요청 실패: {str(e)}")
            return Response({"error": "날씨 정보를 가져오는 중 문제가 발생했습니다."}, status=500)