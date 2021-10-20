import json
import random

from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By

app = Flask(__name__)
driverLocation = "./chromedriver"


@app.route('/image', methods=['POST'])
def baidu():
    data = request.get_json(force=True)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('blink-settings=imagesEnabled=false')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(executable_path=driverLocation, chrome_options=options)
    browser.get('https://image.baidu.com')
    browser.find_element(by=By.XPATH, value='//span/input[@class="s_ipt"]').send_keys(data.get('keyword'))
    browser.find_element(by=By.XPATH, value='//span/input[@class="s_newBtn"]').click()
    image = browser.find_element(by=By.XPATH, value='//li[@class="imgitem"][' + str(
        random.randint(2, 6)) + ']/div/div/a/img').get_attribute('src')
    result = {
        'image': str(image)
    }
    browser.quit()
    return json.dumps(result, ensure_ascii=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=318, debug=False)
