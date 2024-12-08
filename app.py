from flask import Flask, render_template
from routes.users import users_bp
from routes.jobs import jobs_bp
from routes.applications import applications_bp

app = Flask(__name__)

# 라우트 등록
app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(jobs_bp, url_prefix="/api/jobs")
app.register_blueprint(applications_bp, url_prefix="/api/applications")

# 메인 페이지
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
