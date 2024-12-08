from flask import Flask
from routes.jobs import jobs_bp

app = Flask(__name__)

# API 라우트 등록
app.register_blueprint(jobs_bp, url_prefix="/api/jobs")

if __name__ == "__main__":
    app.run(debug=True)
