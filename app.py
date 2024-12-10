from flask import Flask, render_template
from routes.auth import auth_bp
from routes.jobs import jobs_bp
from routes.applications import applications_bp
from routes.bookmarks import bookmarks_bp
from flasgger import Swagger
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# Flask 앱 초기화
app = Flask(__name__)

# Swagger 설정
swagger = Swagger(app)

# 블루프린트 등록
app.register_blueprint(auth_bp, url_prefix='/auth')  # 회원 관리 API
app.register_blueprint(jobs_bp, url_prefix='/jobs')  # 채용 공고 API
app.register_blueprint(applications_bp, url_prefix='/applications')  # 지원 관리 API
app.register_blueprint(bookmarks_bp, url_prefix='/bookmarks')  # 북마크 API

# 기본 라우트 설정
@app.route('/')
def index():
    """
    Home Page
    ---
    responses:
      200:
        description: Renders the home page.
    """
    return render_template("index.html")

if __name__ == '__main__':
    # Flask 앱 실행
    app.run(
        debug=True,
        host=os.getenv("FLASK_RUN_HOST", "127.0.0.1"),  # 기본값: 127.0.0.1
        port=int(os.getenv("FLASK_RUN_PORT", 5000))      # 기본값: 5000
    )
