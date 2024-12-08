import requests
from bs4 import BeautifulSoup

def crawl_saramin(keyword, pages=5):
    jobs = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    for page in range(1, pages + 1):
        url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={keyword}&recruitPage={page}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch page {page}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        for job in soup.select('.item_recruit'):
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
