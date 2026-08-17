"""
Скрипт відкриває сторінку товару iPhone за прямим URL,
збирає дані за допомогою Requests
та BeautifulSoup і зберігає результати в базу даних Django.
"""
import re
import requests
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import Phone

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'uk-UA,uk;q=0.9,ru;q=0.8',
}

url = 'https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html'

print(f"Запит на: {url}")
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

product = {}

try:
    product['full_name'] = soup.find('h1').text.strip()
except AttributeError:
    product['full_name'] = None

try:
    product['product_code'] = soup.find('span', attrs={'class': 'br-pr-code-val'}).text.strip()
except AttributeError:
    product['product_code'] = f"ID_{url.split('-p')[-1].replace('.html', '')}"

try:
    manuf_link = soup.find('a', title=re.compile(r'^Виробник '))
    product['manufacturer'] = manuf_link.text.strip() if manuf_link else None
except AttributeError:
    product['manufacturer'] = None

try:
    old_price_div = soup.find('div', class_=re.compile(r'br-pp-op'))
    if old_price_div:
        price_str = old_price_div.find('span').text.strip()
        product['regular_price'] = int(''.join(filter(str.isdigit, price_str)))
    else:
        product['regular_price'] = None
except (AttributeError, ValueError):
    product['regular_price'] = None

try:
    promo_div = soup.find('div', class_=re.compile(r'red-price'))
    if promo_div:
        first_span = promo_div.find('span')
        if first_span:
            promo_str = first_span.text.strip()
            product['promo_price'] = int(''.join(filter(str.isdigit, promo_str)))
        else:
            product['promo_price'] = None
    else:
        product['promo_price'] = None
except (AttributeError, ValueError):
    product['promo_price'] = None

try:
    reviews_link = soup.find('a', href='#reviews-list')
    if reviews_link:
        reviews_str = reviews_link.text.strip()
        digits = ''.join(filter(str.isdigit, reviews_str))
        product['reviews_count'] = int(digits) if digits else 0
    else:
        product['reviews_count'] = 0
except (AttributeError, ValueError):
    product['reviews_count'] = 0

product['photos'] = []
try:
    images = soup.find_all('img', attrs={'class': 'br-main-img'})
    for img in images:
        img_url = img.get('src')
        if img_url and 'no-photo' not in img_url and img_url not in product['photos']:
            product['photos'].append(img_url)
except AttributeError:
    pass

product['specifications'] = {}
product['color'] = None
product['memory_capacity'] = None
product['screen_diagonal'] = None
product['screen_resolution'] = None

try:
    char_block = soup.find('div', class_='br-pr-chr')

    if char_block:
        all_rows = char_block.find_all('div')

        for row in all_rows:
            spans = row.find_all('span', recursive=False)

            if len(spans) == 2:
                key = spans[0].text.strip()
                raw_value = spans[1].text.replace('\xa0', ' ')
                value = ' '.join(raw_value.split())

                if key and value:
                    product['specifications'][key] = value

        for key, value in product['specifications'].items():
            key_lower = key.lower()

            if "колір" in key_lower or "цвет" in key_lower:
                product['color'] = value
            elif "об'єм пам'яті" in key_lower or "встроенная память" in key_lower or "пам'ять" in key_lower:
                product['memory_capacity'] = value
            elif "діагональ" in key_lower or "диагональ" in key_lower:
                product['screen_diagonal'] = value
            elif "роздільна здатність" in key_lower or "разрешение" in key_lower:
                product['screen_resolution'] = value

except Exception as e:
    print(f"Помилка парсингу характеристик: {e}")

print('\n' + '-' * 50)
print("Зібрані дані:")
for key, value in product.items():
    if key == 'specifications':
        print(f'{key}: [Словник, {len(value)} шт.]')
    else:
        print(f'{key}: {value}')
print('-' * 50 + '\n')

try:
    new_phone, created = Phone.objects.update_or_create(
        product_code=product.get('product_code'),
        defaults={
            'full_name': product.get('full_name'),
            'manufacturer': product.get('manufacturer'),
            'color': product.get('color'),
            'memory_capacity': product.get('memory_capacity'),
            'screen_diagonal': product.get('screen_diagonal'),
            'screen_resolution': product.get('screen_resolution'),
            'regular_price': product.get('regular_price'),
            'promo_price': product.get('promo_price'),
            'reviews_count': product.get('reviews_count', 0),
            'photos': product.get('photos', []),
            'specifications': product.get('specifications', {})
        }
    )
    if created:
        print(f"Товар {new_phone.full_name} створено в БД")
    else:
        print(f"Товар {new_phone.full_name} оновлено в БД")
except Exception as e:
    print(f"Помилка збереження: {e}")