import base64
import json
import random
import urllib.request

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
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,3840")
    browser = webdriver.Chrome(executable_path=driverLocation, chrome_options=options)
    browser.get('https://image.baidu.com')
    browser.find_element(by=By.XPATH, value='//span/input[@class="s_ipt"]').send_keys(data.get('keyword'))
    browser.find_element(by=By.XPATH, value='//span/input[@class="s_newBtn"]').click()
    image = browser.find_element(by=By.XPATH, value='//li[@class="imgitem"][' + str(
        random.randint(2, 15)) + ']/div/div/a/img').get_attribute('src')
    if str(image).startswith('http'):
        address = urllib.request.urlopen(str(image))
        img = address.read()
        encoded_image = str(base64.b64encode(img))
        result = {
            'image': encoded_image.split("'")[1]
        }
        return json.dumps(result, ensure_ascii=False)
    else:
        if 'data:image/jpg;base64,' in str(image):
            result = {
                'image': str(image).replace('data:image/jpg;base64,', '')
            }
            browser.quit()
            return json.dumps(result, ensure_ascii=False)
        else:
            result = {
                'image': str(image).replace('data:image/jpeg;base64,', '')
            }
            browser.quit()
            return json.dumps(result, ensure_ascii=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=318)
