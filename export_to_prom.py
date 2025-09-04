import sqlite3
import requests
from datetime import datetime

# Ендпоінти для обох магазинів
EXCHANGE_URLS = [
    "http://my.prom.ua/cabinet/export_orders/cml/3841314?hash_tag=eyJlbWFpbCI6InRvcmdvay5va0BnbWFpbC5jb20ifQ.Z2FHKQ.biidzJqOVhf-tT0v8RH6yCx4nw0",  # магазин e
    "http://my.prom.ua/cabinet/export_orders/cml/3957686?hash_tag=eyJlbWFpbCI6ImNoZXJrYXN5X21hcmtldEB1a3IubmV0In0.aLjCHA.Md0WX_LQjsc9Mt2GIgu-rNqghdY"   # магазин c
]

# Підключення до вашої бази
conn = sqlite3.connect("../goods.db")
cursor = conn.cursor()

# Вибірка товарів (артикул, назва, ціна, залишок)
cursor.execute("SELECT article, name, sale_price, quantity FROM goods")
goods = cursor.fetchall()

# Формуємо CommerceML XML
now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<КоммерческаяИнформация ВерсияСхемы="2.04" ДатаФормирования="{now}">
  <Каталог>
    <Товары>
'''

for article, name, price, quantity in goods:
    xml += f'''      <Товар>
        <Ид>{article}</Ид>
        <Артикул>{article}</Артикул>
        <Наименование>{name}</Наименование>
        <Цены>
          <Цена>
            <Представление>Розничная</Представление>
            <ЦенаЗаЕдиницу>{price}</ЦенаЗаЕдиницу>
            <Валюта>UAH</Валюта>
          </Цена>
        </Цены>
        <Остатки>
          <Остаток>
            <Количество>{quantity}</Количество>
          </Остаток>
        </Остатки>
      </Товар>
'''

xml += '''    </Товары>
  </Каталог>
</КоммерческаяИнформация>
'''

# Зберігаємо файл (опційно)
with open("export_commerceml.xml", "w", encoding="utf-8") as f:
    f.write(xml)

# Відправляємо файл на обидва магазини
for url in EXCHANGE_URLS:
    print(f"Відправка на: {url}")
    files = {'file': ('export_commerceml.xml', xml, 'text/xml')}
    response = requests.post(url, files=files)
    print("Status:", response.status_code)
    print("Response:", response.text)
