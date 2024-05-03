CREATE DATABASE chotot_db;
USE chotot_db,
CREATE TABLE products (
	ad_id INT,
	timedate NVARCHAR(256),
	account_id INT,
	account_name NVARCHAR(256),
	title NVARCHAR(256),
	body NVARCHAR(256),
	category INT,
	category_name NVARCHAR(256),
	area INT,
	area_name NVARCHAR(256),
	region INT,
	region_name NVARCHAR(256),
	price INT,
	price_string NVARCHAR(256),
	webp_image NVARCHAR(256)
)