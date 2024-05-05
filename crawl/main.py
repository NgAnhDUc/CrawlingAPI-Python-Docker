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
            'ad_id': item.get('ad_id'),
            'timedate': item.get('date'), # Đảm bảo định dạng của ngày/giờ là chính xác
            'account_id': item.get('account_id'), # Kiểu dữ liệu của cột này?
            'account_name': item.get('account_name'),
            'title': item.get('subject'), # Kiểu dữ liệu của cột này?
            'body': item.get('body'),
            'category': item.get('category'),
            'category_name': item.get('category_name'),
            'area': item.get('area'), # Kiểu dữ liệu của cột này?
            'area_name': item.get('area_name'),
            'region': item.get('region'), # Kiểu dữ liệu của cột này?
            'region_name': item.get('region_name'),
            'price': item.get('price'),
            'price_string': item.get('price_string'),
            'webp_image': item.get('webp_image')
        }
        products.append(product)

    with open('products.json', 'w', encoding='utf-8') as file:
        json.dump(products, file, ensure_ascii=False, indent=4)

    try:
        # Kết nối đến cơ sở dữ liệu MySQL
        con = mysql.connector.connect(
            user='root',
            password='123456',
            host='localhost',
            port='1000',
            database='chotot_db'
        )

        if con.is_connected():
            print('Connected to MySQL database')

            cursor = con.cursor()

            # Chèn dữ liệu vào bảng
            for product in products:
                cursor.execute("""
                    INSERT INTO Products (ad_id, timedate, account_id, account_name, title, body, category, category_name, area, area_name, region, region_name, price, price_string, webp_image)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (product['ad_id'], product['timedate'], product['account_id'], product['account_name'], product['title'], product['body'], product['category'], product['category_name'], product['area'], product['area_name'], product['region'], product['region_name'], product['price'], product['price_string'], product['webp_image']))

            # Commit các thay đổi
            con.commit()

    except Exception as e:
        print("Failed to connect to MySQL database:", e)

    finally:
        # Đóng kết nối
        if 'con' in locals() and con.is_connected():
            cursor.close()
            con.close()
            print("MySQL connection is closed")

    print(products)
else:
    print("Failed to get data from Chotot API")
