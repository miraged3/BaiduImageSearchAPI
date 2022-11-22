import base64
import json
import random
import time
import urllib.request

from bs4 import BeautifulSoup
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By

import yinglish

app = Flask(__name__)
driverLocation = "./chromedriver.exe"


@app.route('/image', methods=['POST'])
def baidu():
    data = request.get_json(force=True)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(executable_path=driverLocation, chrome_options=options)
    browser.get('https://image.baidu.com')
    browser.find_element(by=By.XPATH, value='//span/input[@class="s_ipt"]').send_keys(data.get('keyword'))
    browser.find_element(by=By.XPATH, value='//span/input[@class="s_newBtn"]').click()
    time.sleep(3)
    soup = BeautifulSoup(browser.page_source, features='html.parser')
    all_images = soup.find_all('img', class_='main_img img-hover')
    image = random.choice(all_images)
    print(image['src'])
    if str(image['src']).startswith('http'):
        address = urllib.request.urlopen(str(image['src']))
        img = address.read()
        encoded_image = str(base64.b64encode(img))
        result = {
            'image': encoded_image.split("'")[1]
        }
        return json.dumps(result, ensure_ascii=False)
    else:
        if 'data:image/jpg;base64,' in str(image['src']):
            result = {
                'image': str(image['src']).replace('data:image/jpg;base64,', '')
            }
            browser.quit()
            return json.dumps(result, ensure_ascii=False)
        else:
            result = {
                'image': str(image['src']).replace('data:image/jpeg;base64,', '')
            }
            browser.quit()
            return json.dumps(result, ensure_ascii=False)


@app.route('/yinglish', methods=['POST'])
def yin():
    data = request.get_json(force=True)
    result = {
        'yinglish': yinglish.chs2yin(data.get('message'))
    }
    return json.dumps(result, ensure_ascii=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=318)
