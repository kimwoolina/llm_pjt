from llm import ask_chatgpt
from weather import get_weather_data
from llm_pjt.settings import SERVICE_KEY, OPEN_API_KEY

# 시스템 안내 메시지 설정


def create_system_instructions(weather_info):
    return f"""
당신은 날씨 관련 정보를 제공하는 챗봇입니다. 사용자가 날씨에 대한 질문을 할 때, 다음과 같은 형식으로 대답해 주세요:

1. **통상적 또는 대략적인 날씨 정보**:
- 🌏 현재 날씨: {weather_info.get('rain', '정보 없음')}
- 🔼 최고 기온: [최고 기온]°C
- 🔽 최저 기온: [최저 기온]°C
- 💧 습도 정도 : {weather_info.get('humidity', '정보 없음')}
- 🔎 관측 지점: [관측 지점]

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


# 날씨 데이터 가져오기
weather_info = get_weather_data(SERVICE_KEY)
system_instructions = create_system_instructions(weather_info)

# 대화 시작
print("봇: 안녕하세요! 무엇을 도와드릴까요?\n")

while True:
    user_input = input("유저: ")
    if user_input.lower() in ["종료", "exit"]:
        print("봇: 대화가 종료되었습니다. 감사합니다!")
        break
    response = ask_chatgpt(user_input, system_instructions)
    print(f"봇: {response}\n\n")
