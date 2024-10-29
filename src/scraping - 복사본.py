import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

def get_div_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('div', class_='row')
    links = set()  # 링크를 저장할 집합 (set) 생성
    for row in rows:
        divs = row.find_all('div')
        for div in divs:
            a_tags = div.find_all('a')
            for a in a_tags:
                if a.has_attr('href'):
                    full_url = urljoin(url, a['href'])  # 상대 URL을 절대 URL로 변환
                    links.add(full_url)  # 집합에 링크 추가 (중복 자동 제거)
    return list(links)  # 리스트로 변환하여 반환

def crawl_link(link):
    try:
        response = requests.get(link)
        page_soup = BeautifulSoup(response.text, 'html.parser')
        title = page_soup.find('title').text if page_soup.find('title') else 'No title found'
        return {'URL': link, 'Title': title}
    except Exception as e:
        print(f"Error crawling {link}: {e}")
        return {'URL': link, 'Title': 'Failed to crawl'}

def main():
    url = 'https://scholarworks.unist.ac.kr/browse-researcher?query=&tab=LAB&comm=aa61d9a2-6d45-42ad-9cfb-bdf5062f257a&starts_with=&page=2&offset=12'
    links = get_div_links(url)
    results = []

    for link in links:
        result = crawl_link(link)
        results.append(result)

    # 데이터 프레임 생성 및 중복 제거
    df = pd.DataFrame(results)
    df = df.drop_duplicates(subset=['URL'])  # 데이터프레임에서도 중복 제거

    # 엑셀 파일로 저장
    df.to_excel('div_links_data_unique1.xlsx', index=False)

if __name__ == '__main__':
    main()
