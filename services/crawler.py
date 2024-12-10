import requests
from bs4 import BeautifulSoup
from datetime import datetime
from services.database import jobs_collection

def crawl_saramin(keyword, pages=5):
    headers = {'User-Agent': 'Mozilla/5.0'}
    for page in range(1, pages + 1):
        url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword={keyword}&recruitPage={page}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        job_listings = soup.select('.item_recruit')
        for job in job_listings:
            try:
                title = job.select_one('.job_tit a').text.strip()
                company = job.select_one('.corp_name a').text.strip()
                location = job.select_one('.job_condition span').text.strip()
                deadline = job.select_one('.job_date .date').text.strip()
                date_crawled = datetime.now()

                job_data = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "deadline": deadline,
                    "date_crawled": date_crawled
                }

                jobs_collection.update_one(
                    {"title": title, "company": company},
                    {"$set": job_data},
                    upsert=True
                )
            except Exception as e:
                print(f"Error: {e}")
