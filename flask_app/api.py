# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By         
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 16:23:29 2023 
"""
from bs4 import BeautifulSoup
import pandas as pd
import os
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Asegura formato brasileño



# %%
def get_driver():
    # Configuración del driver de Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin interfaz gráfica)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(), options=chrome_options)

def get_soup(url):
    driver = get_driver()
    driver.get(url)
    driver.implicitly_wait(10)  # Espera implícita de 10 segundos
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    return soup

def kabum_scraper(search):
    url = 'https://www.kabum.com.br/busca/' + search
    filter = "?page_number=1&page_size=100"
    soup = get_soup(url + filter)

    cards = soup.find_all('div', class_='bg-white')
    productos = []

    for card in cards:
        try:
            name = card.find('h3').text.strip()
            price = card.find('span', class_='priceCard').text.strip()
            price = price.replace("R$", "").replace("\u00a0", "").strip()
            price = locale.atof(price)  # Convertir a float 
            image_url = card.find('img')['src']
            product_url = card.find('a')['href']
            productos.append({
                'name': name,
                'price': price,
                'image_url': image_url,
                'product_url': product_url
            })
        except AttributeError:
            continue  # Si falta algún dato, pasa al siguiente

    # Crear un DataFrame de pandas
    df = pd.DataFrame(productos)
    # Guardar el DataFrame en un archivo CSV
    df.to_csv('productos.csv', index=False)

    return df

def ml_scraper(search):
    url = 'https://lista.mercadolivre.com.br/' + search
    soup = get_soup(url)
    cards = soup.find_all('div', class_='poly-card--grid-card')

    productos = []

    for card in cards:
        try:
            name_tag = card.find('a', class_='poly-component__title')
            name = name_tag.text.strip()
            url = name_tag['href']
            price_tag = card.find('span', class_='andes-money-amount__fraction')
            price = price_tag.text.strip()
            image = card.find('img')['src']
            productos.append({
                'name': name,
                'price': price,
                'image_url': image,
                'product_url': url
            })
        except AttributeError:
            continue  # Si falta algún dato, pasa al siguiente

    df_poly = pd.DataFrame(productos)
    df_poly.head()
    return df_poly


def amazon_scraper(search):
    soup = get_soup('https://www.amazon.com.br/s?k=' + search)
    cards = soup.find_all('div', class_='a-spacing-base')
    productos = []

    for card in cards:
        try:
            name = card.find('h2').text.strip()
            price = card.find('span', class_='a-price-whole').text.strip()
            image_url = card.find('img')['src']
            product_url = card.find('a')['href']
            productos.append({
                'name': name,
                'price': price,
                'image_url': image_url,
                'product_url': product_url
            })
        except AttributeError:
            continue  # Si falta algún dato, pasa al siguiente

    df_amazon = pd.DataFrame(productos)
    return df_amazon

