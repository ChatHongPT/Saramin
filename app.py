from flask import Flask, render_template

app = Flask(__name__)

# 필요한 라우트가 없으면 "Not Found" 에러 발생
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
