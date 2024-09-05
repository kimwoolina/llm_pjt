import openai
from llm_pjt.settings import OPEN_API_KEY

# API 키 설정
openai.api_key = OPEN_API_KEY

def ask_chatgpt(user_message, system_instructions):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_message}
        ],
    )
    return completion.choices[0].message['content']
