from flask import Flask
from flasgger import Swagger
from routes.users import users_bp
from routes.jobs import jobs_bp
from routes.applications import applications_bp
from routes.auth import auth_bp

app = Flask(__name__)
Swagger(app)

# 블루프린트 등록
app.register_blueprint(users_bp, url_prefix="/api/users")
app.register_blueprint(jobs_bp, url_prefix="/api/jobs")
app.register_blueprint(applications_bp, url_prefix="/api/applications")
app.register_blueprint(auth_bp, url_prefix="/api/auth")

# 메인 페이지
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
