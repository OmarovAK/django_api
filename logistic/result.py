import requests
from bs4 import BeautifulSoup
import re
import os
import json
import random


def add_products():
    url = 'https://www.colady.ru/spisok-neobxodimyx-produktov-na-mesyac-kak-ekonomit-semejnyj-byudzhet.html'

    html_text = requests.get(url).text

    soup = BeautifulSoup(html_text, 'lxml')

    text = soup.find('article')

    text_stock = text.find_all('h3')
    text_product = text.find_all('ul')

    my_list = []
    for i in text_product:
        local_list = [i.text]
        my_list.append(local_list)

    list_product = []
    for i in my_list:
        result = re.sub(r'[n,\\\[\]\']', '', str(i))
        result = result.strip()
        local_list = result.split('.')
        count = 0
        for k in local_list:
            if len(k) == 0:
                local_list.pop(count)
            count = count + 1
        list_product.append(local_list)

    list_description = []
    for i in text_stock:
        list_description.append(i.text)

    my_dict = dict(zip(list_description, list_product))

    for k, v in my_dict.items():
        for val in v:
            url = 'http://127.0.0.1:8000/products/'
            res = requests.post(url=url, data={'title': val, 'description': k})
            print(res.json())

    file_dump = os.path.join(os.getcwd(), 'index.json')

    with open(file_dump, mode='w', encoding='utf-8') as stock_file:
        json.dump(my_dict, stock_file)


def add_stock():
    file = os.path.join(os.getcwd(), 'index.json')
    with open(file=file, mode='r', encoding='utf-8') as file_json:
        result_json = json.load(file_json)
        for k, v in result_json.items():
            url = 'http://127.0.0.1:8000/stock/'
            result = requests.post(url=url, data={'address': k})
            print(result.json())


def add_product_stock():
    file = os.path.join(os.getcwd(), 'index.json')
    with open(file=file, mode='r') as f:
        my_dict = dict()
        id_stock = None
        json_file = json.load(f)
        for k, v in json_file.items():
            url = 'http://127.0.0.1:8000/stock/'
            res_stock = requests.get(url)
            if len(res_stock.json()) > 0:
                for key in res_stock.json():
                    if k == key['address']:
                        id_stock = key['id']
                url_ = 'http://127.0.0.1:8000/products/'
                res_prod = requests.get(url_)
                ids_prod = []
                for items_file in v:

                    for items_model_prod in res_prod.json():
                        if items_file == items_model_prod['title']:
                            ids_prod.append(items_model_prod['id'])
                my_dict.setdefault(id_stock, ids_prod)
            else:
                pass

    url_stock_prod = 'http://127.0.0.1:8000/stock_product/'
    res = requests.get(url_stock_prod)
    list_id_product = []
    for i in res.json():
        list_id_product.append(i["product"])

    for k, v in my_dict.items():
        url = 'http://127.0.0.1:8000/stock_product/'
        for i in v:
            if i not in list_id_product:
                url_stock = f'http://127.0.0.1:8000/stock/{k}/'
                url_prod = f'http://127.0.0.1:8000/products/{i}/'
                res_prod = requests.get(url_prod)
                res_stock = requests.get(url_stock)
                price = random.randint(1, 100)
                quant = random.randint(5, 58)
                requests.post(url=url, data={'stock': k, 'product': i, 'price': price, 'quantity': quant})
                print(
                    f'Продукт {res_prod.json()["title"].upper()} успешно добавлен на склад {res_stock.json()["address"].upper()}')
            else:
                url_stock = f'http://127.0.0.1:8000/stock/{k}/'
                url_prod = f'http://127.0.0.1:8000/products/{i}/'
                res_prod = requests.get(url_prod)
                res_stock = requests.get(url_stock)
                print(
                    f'Продукт {res_prod.json()["title"].upper()} был ранее добавлен на склад {res_stock.json()["address"].upper()}')


def delete_all_prod():
    url = "http://127.0.0.1:8000/products/"
    res = requests.get(url)
    if len(res.json()) > 0:
        count = 1
        for i in res.json():
            url_ = f'{url}{i["id"]}/'
            title = i['title']
            res_ = requests.delete(url_)
            if res_.status_code:
                print(f'{count}. Продукт с названием {str(title.upper())} успешно удален')
            count = count + 1
    else:
        print('Товаров нет в базе данных')


def delete_stock():
    url = "http://127.0.0.1:8000/stock/"
    res = requests.get(url)
    if len(res.json()) > 0:
        for i in res.json():
            url_ = f'{url}{i["id"]}/'
            res_ = requests.delete(url=url_)
            if res_.status_code:
                print(f'Склад {i["address"].upper()} успешно удален')
    else:
        print("Складов в базе данных нет")


#add_products()

#add_stock()

# delete_stock()

# delete_all_prod()


add_product_stock()
