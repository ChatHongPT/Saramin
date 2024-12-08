import requests
from bs4 import BeautifulSoup

def crawl_saramin(keyword, pages=1):
    """
    사람인 데이터를 크롤링하는 함수.

    Args:
        keyword (str): 검색 키워드
        pages (int): 검색 페이지 수

    Returns:
        list: 크롤링된 채용 공고 리스트
    """
    jobs = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for page in range(1, pages + 1):
        url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={keyword}&recruitPage={page}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 채용 공고 추출
        job_listings = soup.select('.item_recruit')
        for job in job_listings:
            title = job.select_one('.job_tit a').text.strip()
            company = job.select_one('.corp_name a').text.strip()
            location = job.select_one('.job_condition span').text.strip()
            link = 'https://www.saramin.co.kr' + job.select_one('.job_tit a')['href']
            deadline = job.select_one('.job_date .date').text.strip()

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "link": link,
                "deadline": deadline
            })

    return jobs
