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


def edit_productions():
    url_prod_stock = 'http://127.0.0.1:8000/stock_product/'
    res_prod_stock = requests.get(url_prod_stock)
    count = 1
    for i in res_prod_stock.json():
        id_stock = i['stock']
        id_product = i['product']
        url_product = f'http://127.0.0.1:8000/products/{id_product}/'
        url_stock = f'http://127.0.0.1:8000/stock/{id_stock}/'
        res_stock = requests.get(url_stock)
        res_prod = requests.get(url_product)
        print(
            f"{count}. id продукта: {res_prod.json()['id']} Продукт: {res_prod.json()['title']}, Место склада: {res_stock.json()['address']}, Остаток: {i['quantity']}, Цена: {i['price']}")
        count = count + 1
    result = False
    count = 1
    while not result:
        if count > 1:
            id_product = int(input('Такого id продукта нет Введите id продукта: '))
        else:
            id_product = int(input('Введите id продукта: '))
        count = count + 1
        url = f'http://127.0.0.1:8000/products/'
        res = requests.get(url)
        for i in res.json():
            if i['id'] == id_product:
                for item in res_prod_stock.json():
                    if i['id'] == item['product']:
                        url_stock = f"http://127.0.0.1:8000/stock/{item['stock']}/"
                        res_stock = requests.get(url_stock)
                        print(
                            f"Продукт: {i['title']}, Место склада: {res_stock.json()['address']}, Текущее количество: "
                            f"{item['quantity']}, Цена: {item['price']}")
                        result_edit = False
                        count = 1
                        while not result_edit:
                            my_dict = {
                                'p': f'изменение цены продукта {i["title"]}',
                                'q': f'изменение текущего остатка продукта {i["title"]}'
                            }
                            for key, val in my_dict.items():
                                print(f'Наименование команды: {key} Действие: {val.upper()}')
                            command_edit = input('Введите команду: ')
                            if command_edit == 'p':
                                price_new = input('Введите новую цену: ')
                                if price_new.isdigit():
                                    res_ = requests.get(f'{url_prod_stock}{item["id"]}/')
                                    old_price = res_.json()['price']
                                    res = requests.patch(f'{url_prod_stock}{item["id"]}/', data={'price': price_new})
                                    print(f"У товара {i['title']} изменена цена: \n"
                                          f"\tСтарая цена: {old_price} \n"
                                          f"\tНовая цена: {res.json()['price']}")
                                    result_edit = True
                                else:
                                    print('Вы не ввели число. Выберите команду')
                            elif command_edit == 'q':
                                quant_new = input('Введите новое количество: ')
                                if quant_new.isdigit():
                                    res_ = requests.get(f'{url_prod_stock}{item["id"]}/')
                                    old_quant = res_.json()['quantity']
                                    res = requests.patch(f'{url_prod_stock}{item["id"]}/', data={'quantity': quant_new})
                                    print(f"У товара {i['title']} изменено количество: \n"
                                          f"\tСтарое количество: {old_quant} \n"
                                          f"\tНовое количество: {res.json()['quantity']}")
                                    result_edit = True

                        result = True


def list_product():
    url_prod_stock = 'http://127.0.0.1:8000/stock_product/'
    res_prod_stock = requests.get(url_prod_stock)
    count = 1
    for i in res_prod_stock.json():
        url_prod = f"http://127.0.0.1:8000/products/{i['product']}"
        url_stock = f"http://127.0.0.1:8000/stock/{i['stock']}"
        res_prod = requests.get(url_prod)
        res_stock = requests.get(url_stock)
        print(f"{count}. Товар: {res_prod.json()['title']}, Наименование склада: {res_stock.json()['address']}, "
              f"цена: {i['price']}, количество: {i['quantity']}")
        count = count + 1


# add_products()

# add_stock()

# delete_stock()

# delete_all_prod()

# add_product_stock()

# edit_productions()

list_product()
