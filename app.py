from flask import Flask, render_template
from flasgger import Swagger
from routes.auth import auth_bp
from routes.jobs import jobs_bp
from routes.applications import applications_bp
from routes.bookmarks import bookmarks_bp

app = Flask(__name__)
Swagger(app)

# 블루프린트 등록
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(jobs_bp, url_prefix="/jobs")
app.register_blueprint(applications_bp, url_prefix="/applications")
app.register_blueprint(bookmarks_bp, url_prefix="/bookmarks")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
