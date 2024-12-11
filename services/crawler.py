import requests
from bs4 import BeautifulSoup
from datetime import datetime
from services.database import jobs_collection  # MongoDB 컬렉션 가져오기

def crawl_saramin(keyword, pages=5):
    headers = {'User-Agent': 'Mozilla/5.0'}
    for page in range(1, pages + 1):
        url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={keyword}&recruitPage={page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        job_listings = soup.select('.item_recruit')
        for job in job_listings:
            try:
                # 크롤링한 데이터 추출
                title = job.select_one('.job_tit a').text.strip()
                company = job.select_one('.corp_name a').text.strip()
                location = job.select_one('.job_condition span').text.strip()
                deadline = job.select_one('.job_date .date').text.strip()
                date_crawled = datetime.now()

                # 중복 데이터 확인 및 업데이트
                existing_job = jobs_collection.find_one({"title": title, "company": company})
                if existing_job:
                    # 기존 데이터가 있으면 업데이트하지 않고 무시
                    print(f"Duplicate found: {title} at {company}. Skipping...")
                    continue
                
                # 새 데이터를 MongoDB에 삽입
                job_data = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "deadline": deadline,
                    "date_crawled": date_crawled
                }
                jobs_collection.insert_one(job_data)
                print(f"Inserted: {title} at {company}")
            except Exception as e:
                print(f"Error while processing a job: {e}")

