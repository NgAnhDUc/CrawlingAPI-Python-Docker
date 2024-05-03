import json
import requests
import mysql.connector

products = []
url = "https://gateway.chotot.com/v1/public/ad-listing?limit=10&protection_entitlement=true&cg=5010&st=s,k&key_param_included=true"

response = requests.get(url)

if response.status_code == 200:
    print("get success")
    for item in response.json().get('ads'):
        product = {
            'id': item.get('ad_id'),
            'date': item.get('date'),
            'body': item.get('body'),
            'category': item.get('category'),
            'category_name': item.get('category_name'),
            'price': item.get('price'),
            'subject': item.get('subject')
        }
        products.append(product)

with open('products.json', 'w', encoding='utf-8') as file:
    json.dump(products, file, ensure_ascii=False, indent=4)

try:
    con = mysql.connector.connect(
        user='root',
        password='123456',
        host='172.17.0.2',
        port='6603',
        database='chotot_db'
    )

    if con.is_connected():
        print('Connected to MySQL database')

        cursor = con.cursor()

        # Tạo bảng (nếu chưa có)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                price DECIMAL(10, 2),
                subject VARCHAR(255)
            )
        """)

        # Chèn dữ liệu vào bảng
        for product in products:
            cursor.execute("""
                INSERT INTO Products (name, price, subject)
                VALUES (%s, %s, %s)
            """, (product['name'], product['price'], product['subject']))

        # Commit các thay đổi
        con.commit()

except Exception as e:
    print("Failed to connect to MySQL database")

print(products)
