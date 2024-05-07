from fastapi import FastAPI, HTTPException, Header, Query
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
async def search_products(title: str = Query(None)):
    try:
        if title is None:
            raise HTTPException(status_code=400, detail="Title parameter is required")

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