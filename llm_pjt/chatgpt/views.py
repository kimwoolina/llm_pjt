from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .weather import get_weather_data
from .bots import ask_chatgpt

class WeatherChatAPIView(APIView):
    def post(self, request):
        user_message = request.data.get("message")

        # 날씨 정보 가져오기
        weather_info = get_weather_data(settings.SERVICE_KEY)
        
        # 시스템 안내 메시지 생성
        system_instructions = create_system_instructions(weather_info)

        # ChatGPT에 메시지 전송
        chatgpt_response = ask_chatgpt(user_message, system_instructions)

        return Response({"message": chatgpt_response})

def create_system_instructions(weather_info):
    return f"""
당신은 날씨 관련 정보를 제공하는 챗봇입니다. 사용자가 날씨에 대한 질문을 할 때, 다음과 같은 형식으로 대답해 주세요:

1. **통상적 또는 대략적인 날씨 정보**:
- 🌏 현재 날씨: {weather_info.get('rain', '정보 없음')}
- 🔼 최고 기온: {weather_info.get('highest_temp', '정보 없음')}°C
- 🔽 최저 기온: {weather_info.get('lowest_temp', '정보 없음')}°C
- 💧 습도 정도 : {weather_info.get('humidity', '정보 없음')}
- 🔎 관측 지점: {weather_info.get('location', '정보 없음')}

예를 들어:
- 🌏 현재 날씨: 비가 오지 않음
- 🔼 최고 기온: 27°C
- 🔽 최저 기온: 20°C
- 💧 습도 정도 : 보통
- 🔎 관측 지점: 서울 강남구 개포2동

2. **구체적인 날씨 정보 요청**:
- 강수량, 바람의 세기, 특정 지역의 기온, 습도 등과 같은 세부적인 정보를 요청할 경우, 해당 정보에 맞게 대답해 주세요.

예를 들어:
- "고양시의 강수량은 얼마인가요?"
- "현재 서울의 바람 속도는 얼마인가요?"
- "대전의 기온이 어떻게 되나요?"

이러한 형식으로, 사용자가 원하는 정보에 맞게 적절히 대답해 주세요.
"""
