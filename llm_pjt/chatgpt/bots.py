import openai
from llm_pjt.settings import OPEN_API_KEY


# OpenAI API 키를 설정합니다.
openai.api_key = OPEN_API_KEY

def translate_bot(user_message):
    system_instructions = """
    누구나 이해하기 쉽게 5줄 정도로 요약한 것을, 한국말로 번역해서 알려줘. 
    사용자가 너에게 반말을 하더라도 너는 절대 반말을 사용하지 말고 존댓말로 예의있게 대답해.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_message}
        ]
    )
    
    return response.choices[0].message['content']
