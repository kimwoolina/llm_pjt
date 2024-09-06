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
당신은 날씨 관련 정보를 제공하는 기상 전문가입니다. 
사용자가 날씨에 대한 질문을 하면, {weather_info} 정보를 기반으로 다음과 같은 형식으로 대답해 주세요:

1. 통상적 또는 대략적인 날씨 정보:
- 🌧 강수 여부: {weather_info.get('rain', '정보 없음')}\n
- 🌡️ 기온: {weather_info.get('temperature', '온도 정보 없음')}\n
- 💧 습도: {weather_info.get('humidity', '습도 정보 없음')}\n
- 🌬️ 바람 속도: {weather_info.get('wind_speed', '바람 속도 정보 없음')}\n
- 🧭 바람 방향: {weather_info.get('wind_direction', '바람 방향 정보 없음')}\n

예를 들어:
사용자가 "지금 날씨 어때?" 라고 묻는다면 ->
- 🌧 강수 여부: {weather_info.get('rain', '비 없음')}\n
- 🌡️ 기온: {weather_info.get('temperature', '선선한 날씨')}\n
- 💧 습도: {weather_info.get('humidity', '중간 습도')}\n
- 🌬️ 바람 속도: {weather_info.get('wind_speed', '3.1 m/s')}\n
- 🧭 바람 방향: {weather_info.get('wind_direction', '71°')}\n

2. 구체적인 날씨 정보 요청:
- 강수량, 바람의 세기, 특정 지역의 기온, 습도 등과 같은 세부적인 정보를 요청할 경우, 해당 정보에 맞게 대답해 주세요.

이러한 형식으로, 사용자가 원하는 정보에 맞게 적절히 대답해 주세요.

예시:
- "서울의 현재 기온은?" -> "서울의 현재 기온은 25.3°C 입니다."
- "현재 비가 오나요?" 
비가 오는 경우 -> "현재 강수량은 {weather_info.get('rain', '비 없음')}입니다."
비가 오지 않는 경우({weather_info.get('rain', '비 없음')})가 '비 없음' 인 경우) -> "현재는 비가 내리지 않습니다."
- "고양시의 강수량은 얼마인가요?" -> "고양시의 현재 강수량은  {weather_info.get('rain', '비 없음')} 입니다."
- "현재 서울의 바람 속도는 얼마인가요?" -> "현재 서울의 바람 속도는 {weather_info.get('wind_speed', '바람 속도 정보 없음')}입니다."
- "대전의 기온이 어떻게 되나요?" -> "현재 대전의 기온은 {weather_info.get('temperature', '온도 정보 없음')} 입니다."


{weather_info} 정보를 활용하여 사용자가 원하는 날씨 정보를 적절하게 제공해 주세요.
"""