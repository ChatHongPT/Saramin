import requests
from bs4 import BeautifulSoup
from services.database import db

def crawl_saramin(keyword, pages=1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    for page in range(1, pages + 1):
        url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={keyword}&recruitPage={page}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch page {page}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings = soup.select('.item_recruit')

        for job in job_listings:
            try:
                company = job.select_one('.corp_name a').text.strip()
                title = job.select_one('.job_tit a').text.strip()
                link = 'https://www.saramin.co.kr' + job.select_one('.job_tit a')['href']
                conditions = job.select('.job_condition span')
                location = conditions[0].text.strip() if len(conditions) > 0 else ''
                experience = conditions[1].text.strip() if len(conditions) > 1 else ''
                deadline = job.select_one('.job_date .date').text.strip()

                job_data = {
                    "title": title,
                    "company": company,
                    "link": link,
                    "location": location,
                    "experience": experience,
                    "deadline": deadline
                }

                # 중복 확인 및 저장
                if not db.job_postings.find_one({"link": link}):
                    db.job_postings.insert_one(job_data)
                    print(f"Saved: {title}")
                else:
                    print(f"Skipped (Duplicate): {title}")

            except Exception as e:
                print(f"Error parsing job: {e}")
