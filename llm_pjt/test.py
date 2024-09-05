import requests
from bs4 import BeautifulSoup
from chatgpt.bots import translate_bot

def get_techcrunch_articles():
    url = 'https://techcrunch.com/'
    response = requests.get(url)
    response.raise_for_status()  # 요청 실패 시 예외 발생
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', class_='wp-block-group')
    article_list = []
    for article in articles:
        title_tag = article.find('h2', class_='wp-block-post-title')
        if title_tag:
            link_tag = title_tag.find('a', href=True)
            if link_tag:
                href = link_tag.get('href')
                text = link_tag.get_text(strip=True)
                if href.startswith('https://techcrunch.com/') and text:
                    article_list.append({'title': text, 'link': href})
    return article_list

def get_article_content_and_translate(article_url):
    response = requests.get(article_url)
    response.raise_for_status()  # 요청 실패 시 예외 발생
    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find('div', class_='entry-content wp-block-post-content is-layout-flow wp-block-post-content-is-layout-flow')
    if content_div:
        content_text = content_div.get_text(strip=True)
        if content_text:
            translated_content = translate_bot(content_text)
            return translated_content
    return "기사 내용을 추출할 수 없습니다."

if __name__ == "__main__":
    articles = get_techcrunch_articles()
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"Link: {article['link']}")
        print()
    selected_article_url = input("번역할 기사의 URL을 입력하세요: ")
    translated_content = get_article_content_and_translate(selected_article_url)
    print(f"Translated Content: {translated_content}")
