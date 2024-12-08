import requests
from bs4 import BeautifulSoup

def crawl_saramin(keyword, pages=1):
    jobs = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for page in range(1, pages + 1):
        url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={keyword}&recruitPage={page}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        job_listings = soup.select('.item_recruit')
        for job in job_listings:
            try:
                company = job.select_one('.corp_name a').text.strip()
                title = job.select_one('.job_tit a').text.strip()
                link = 'https://www.saramin.co.kr' + job.select_one('.job_tit a')['href']
                location = job.select('.job_condition span')[0].text.strip() if job.select('.job_condition span') else ''
                jobs.append({
                    '회사명': company,
                    '제목': title,
                    '링크': link,
                    '지역': location
                })
            except Exception as e:
                print(f"Error parsing job: {e}")
                continue

    return jobs
