
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, render_template, request
import time
from selenium import webdriver

app = Flask(__name__)

def crawling(query):
    url = f"https://www.saramin.co.kr/zf_user/search?searchword={query}"
    
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920x1080") 
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    driver.implicitly_wait(10) 
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2) 
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    results = []

    # 데이터 수집
    try:
        job_titles = driver.find_elements(By.CSS_SELECTOR, ".job_tit")
        job_dates = driver.find_elements(By.CSS_SELECTOR, ".date")
        job_conditions = driver.find_elements(By.CSS_SELECTOR, ".job_condition")
        job_sectors = driver.find_elements(By.CSS_SELECTOR, ".job_sector")
        corp_names = driver.find_elements(By.CSS_SELECTOR, ".area_corp")

        for i in range(len(job_conditions)):
            title = job_titles[i].text
            date = job_dates[i].text
            condition = job_conditions[i].text
            sector = job_sectors[i].text
            corp_name = corp_names[i].text

            results.append({
                'title': title,
                'date': date,
                'condition': condition,
                'sector': sector,
                'corp_name': corp_name
            })
    
    except Exception as e:
        print(f"Error occurred: {e}")

    driver.quit()
    return results

@app.route('/')
def index():
    return render_template('saramin.html')

@app.route('/crawl', methods=['GET', 'POST'])
def crawl():
    query = request.args.get('query', '')
    if query:
        results = crawling(query)
        return render_template('result.html', jobs=results)
    return render_template('result.html', jobs=[])

if __name__ == '__main__':
    app.run(debug=True)
