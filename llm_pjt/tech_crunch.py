import requests
from bs4 import BeautifulSoup

# TechCrunch 웹사이트 URL
url = 'https://techcrunch.com/'

# 웹 페이지 요청
response = requests.get(url)
response.raise_for_status()  # 요청 실패 시 예외 발생

# 페이지 내용 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# <article> 내의 기사 링크와 제목만 추출
articles = soup.find_all('article', class_='wp-block-group')

for article in articles:
    # 기사 제목을 가진 <h2> 태그 안의 <a> 태그를 찾습니다.
    title_tag = article.find('h2', class_='wp-block-post-title')
    if title_tag:
        link_tag = title_tag.find('a', href=True)
        if link_tag:
            href = link_tag.get('href')
            text = link_tag.get_text(strip=True)
            if href.startswith('https://techcrunch.com/') and text:
                print(f"Title: {text}")
                print(f"Link: {href}")
                print()
