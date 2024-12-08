from flask import Flask, jsonify
from services.crawler import crawl_saramin
from services.database import save_to_mongodb

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Job Crawler API!"

@app.route("/crawl/<keyword>/<int:pages>", methods=["POST"])
def crawl_jobs(keyword, pages):
    data = crawl_saramin(keyword, pages)
    save_to_mongodb(data)
    return jsonify({"message": f"{len(data)} jobs crawled and saved!"})

if __name__ == "__main__":
    app.run(debug=True)
