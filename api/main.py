from fastapi import FastAPI, HTTPException, Header, Query
import mysql.connector.pooling
import time 
from typing import List, Dict, Any

while True:
    try:
        # Tạo một connection pool
        connection_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="my_pool",
            pool_size=5,
            pool_reset_session=True,
            user='root',
            password='123456',
            host='172.17.0.1',
            port='6603',
            database='chotot_db'
        )
        break
    except Exception as e:
        print("Connection failed, retrying...")
        time.sleep(1)

app = FastAPI()

def create_product_data(product):
  return {
    "ad_id": product[1],
    "timedate": product[2],
    "account_id": product[3],
    "account_name": product[4],
    "title": product[5],
    "body": product[6],
    "category": product[7],
    "category_name": product[8],
    "area": product[9],
    "area_name": product[10],
    "region": product[11],
    "region_name": product[12],
    "price": product[13],
    "price_string": product[14],
    "webp_image": product[15],
    }

def get_connection():
    # Lấy một connection từ connection pool
    return connection_pool.get_connection()

@app.post("/crawl")
async def add_products(products: List[Dict[str, Any]]):
    try:
        con = get_connection()
        cursor = con.cursor()
        for product in products:
            data_Product = (
                product["ad_id"],
                product["timedate"],
                product["account_id"],
                product["account_name"],
                product["title"],
                "body",
                product["category"],
                product["category_name"],
                product["area"],
                product["area_name"],
                product["region"],
                product["region_name"],
                product["price"],
                product["price_string"],
                product["webp_image"],
            )
        
            query = """
                INSERT INTO Products
                (ad_id, timedate, account_id, account_name, title, body, category, category_name, area, area_name, region, region_name, price, price_string, webp_image)
                VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE ad_id = VALUES(ad_id), timedate = VALUES(timedate), 
                    account_id = VALUES(account_id), account_name = VALUES(account_name), title = VALUES(title), 
                    body = VALUES(body), category = VALUES(category), category_name = VALUES(category_name), 
                    area = VALUES(area), area_name = VALUES(area_name), region = VALUES(region), region_name = VALUES(region_name), 
                    price = VALUES(price), price_string = VALUES(price_string), webp_image = VALUES(webp_image);
            """
            cursor.execute(query, data_Product)
            con.commit()
        
        cursor.close()
        con.close()
        return {"message": "Products added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/check_connection")
async def check_connection():
    try:
        # Thử lấy một connection từ pool
        con = get_connection()
        # Nếu không có lỗi, connection thành công
        con.close()  # Đóng connection sau khi kiểm tra
        return {"status": "success", "message": "Connection to database successful!"}
    except Exception as e:
        # Nếu có bất kỳ lỗi nào xảy ra, trả về lỗi kết nối
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/products")
async def get_products():
    try:
        # Lấy connection từ pool
        con = get_connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        products_data = [create_product_data(product) for product in products]
        cursor.close()
        con.close()
        return products_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search")
async def search_products(title: str = Query(None)):
    try:
        if title is None:
            raise HTTPException(status_code=400, detail="Title parameter is required")

        con = get_connection()
        cursor = con.cursor()
        query = f"SELECT * FROM Products WHERE title LIKE '%{title}%' OR area_name LIKE '%{title}%' OR region_name LIKE '%{title}%'"
        cursor.execute(query)
        search_results = cursor.fetchall()
        products_data = [create_product_data(product) for product in search_results]
        cursor.close()
        con.close()
        return products_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))