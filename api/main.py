from fastapi import FastAPI, HTTPException, Header
import mysql.connector.pooling

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

app = FastAPI()

def create_product_data(product):
  return {
    "ad_id": product["ad_id"],
    "timedate": product["timedate"],
    "account_id": product["account_id"],
    "account_name": product["account_name"],
    "title": product["title"],
    "body": product["body"],
    "category": product["category"],
    "category_name": product["category_name"],
    "area": product["area"],
    "area_name": product["area_name"],
    "region": product["region"],
    "region_name": product["region_name"],
    "price": product["price"],
    "price_string": product["price_string"],
    "webp_image": product["webp_image"],
    }

def get_connection():
    # Lấy một connection từ connection pool
    return connection_pool.get_connection()

@app.on_event("startup")
async def startup_event():
    # Tạo một connection và giữ nó mở
    con = get_connection()
    con.close()

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
async def search_products(title: str = Header(..., convert_underscores=True)):
    try:
        con = get_connection()
        cursor = con.cursor()
        query = f"SELECT * FROM Products WHERE title LIKE '%{title}%'"
        cursor.execute(query)
        search_results = cursor.fetchall()
        products_data = [create_product_data(product) for product in search_results]
        cursor.close()
        con.close()
        return products_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
