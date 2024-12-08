from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# MongoDB 설정
app.config["MONGO_URI"] = "mongodb://localhost:27017/job_portal"
mongo = PyMongo(app)

# 홈 라우트
@app.route('/')
def home():
    return "Welcome to the Job Portal API"

# 크롤링 함수
def crawl_jobs():
    url = "https://example.com/jobs"  # 실제 채용 공고 URL로 변경
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    job_list = []
    for job in soup.find_all("div", class_="job-card"):
        title = job.find("h2").get_text(strip=True)
        company = job.find("span", class_="company-name").get_text(strip=True)
        location = job.find("span", class_="job-location").get_text(strip=True)
        posted_date = job.find("span", class_="posted-date").get_text(strip=True)
        deadline = job.find("span", class_="deadline").get_text(strip=True)

        job_data = {
            "title": title,
            "company": company,
            "location": location,
            "posted_date": posted_date,
            "deadline": deadline
        }
        job_list.append(job_data)

    return job_list

# API: 크롤링 데이터 저장
@app.route('/crawl-and-save', methods=['POST'])
def crawl_and_save():
    jobs = crawl_jobs()
    if jobs:
        mongo.db.job_postings.insert_many(jobs)
        return jsonify({"message": f"{len(jobs)} jobs inserted into MongoDB"}), 201
    else:
        return jsonify({"message": "No jobs found"}), 404

# API: 채용 공고 조회
@app.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = list(mongo.db.job_postings.find({}, {"_id": 0}))  # _id 제외
    return jsonify(jobs)

# API: 특정 공고 검색
@app.route('/jobs/search', methods=['GET'])
def search_jobs():
    query = request.args.get('title')  # 예: /jobs/search?title=Engineer
    jobs = list(mongo.db.job_postings.find({"title": {"$regex": query, "$options": "i"}}, {"_id": 0}))
    return jsonify(jobs)

if __name__ == '__main__':
    app.run(debug=True)
