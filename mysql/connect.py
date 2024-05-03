import mysql.connector

try:
    con = mysql.connector.connect(
        user = 'root',
        password = '123456',
        host = '172.17.0.2',
        port = '3306',
        database = 'chotot_db'
    )
    if con.is_connected():
        print('Connected to MySQL database')
except Exception as e:
    print("Failed to connect to MySQL database")


