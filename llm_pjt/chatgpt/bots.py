from openai import OpenAI
from django.conf import settings 


CLIENT = OpenAI(api_key=settings.OPEN_API_KEY)


def translate_bot(user_message):
    system_instructions = """
    내가 크롤링해온 IT 기사의 내용을 누구나 이해하기 쉬운 말로 요약해줘. 
    사용자가 너에게 반말을 하더라도 너는 절대 반말을 사용하지 말고 존댓말로 예의있게 대답해.
    """
    
    completion = CLIENT.chat.completions.create(

    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": system_instructions,
        },
        {
            "role": "user",
            "content": user_message,
        },
    ],
    )
    
    return completion.choices[0].message.content