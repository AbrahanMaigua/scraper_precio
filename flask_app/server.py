from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from datetime import datetime
from api import kabum_scraper, ml_scraper, amazon_scraper
import requests
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Precio Scraper API!"})

@app.route('/kabun', methods=['get'])
def screenshot():
    data = request.args.get('search', default='cpu', type=str)
    url = 'https://www.kabum.com.br/busca/' + data

    print("URL: ", url)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        driver.implicitly_wait(10)  # seconds
        products = []
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        element = soup.find('div')
        classes = element.get('class')  # Retorna uma lista
        print("Classes: ", classes)

        for item in soup.find_all('div', class_='product-item'):
            title = item.find('h2', class_='product-item__content').text.strip()
            price = item.find('span', class_='product-item__new-price').text.strip()
            link = item.find('a')['href']
            products.append({'title': title, 'price': price, 'link': link})

        # Wait for the page to load
        # Take a screenshot
        screenshot_path = "screenshot.png"
        driver.save_screenshot(screenshot_path)
    finally:
        driver.quit()

    return jsonify({'message': 'Screenshot taken', 'url': url, 'screenshot': screenshot_path, 
                    "products":products}), 200

@app.route('/scrape/kabum/<search_term>', methods=['GET'])
def kabum_scraper_server(search_term):
    serch_term = request.args.get('search_term', default='cpu', type=str)

    df = kabum_scraper(serch_term)
    return  jsonify(df.to_dict(orient='records'))

@app.route('/scrape/mercadolivre/<search_term>', methods=['GET'])
def mercadolivre_scraper_server(search_term):

    search_term = request.args.get('search_term', default='cpu', type=str)
    ml = ml_scraper(search_term)

    return jsonify(ml.to_dict(orient='records'))

@app.route('/scrape/amazon/<search_term>', methods=['GET'])
def amazon_scraper_server(search_term):
    search_term = request.args.get('search_term', default='cpu', type=str)
    am = amazon_scraper(search_term)
    return jsonify(am.to_dict(orient='records'))

@app.route('/test', methods=['GET'])
def test():
    response = amazon_scraper_server('cpu')
    data = response.get_json()
    return jsonify({"message": data})

@app.route('/scrape/all', methods=['GET'])
def scrape_all():
    search_term = request.args.get('search_term', default='cpu', type=str)
    kabum_data = kabum_scraper_server(search_term).get_json()
    mercadolivre_data = mercadolivre_scraper_server(search_term).get_json()
    amazon_data = amazon_scraper_server(search_term).get_json()

    all_data = {
        'kabum': kabum_data,
        'mercadolivre': mercadolivre_data,
        'amazon': amazon_data
    }
    print(all_data)
    return jsonify(all_data) # return jsonify(all_data)
@app.route('/scrape/terabyteshop', methods=['GET'])
def scrape_terabyteshop_server(search_term):
    url = 'https://www.terabyteshop.com.br/busca?str=Processador' + search_term
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []
    for item in soup.find_all('div', class_='productCard'):
        title = item.find('h2', class_='productTitle').text.strip()
        price = item.find('span', class_='price').text.strip()
        link = item.find('a')['href']
        products.append({'title': title, 'price': price, 'link': link})

    return products


if __name__ == '__main__':
    app.run(debug=True)