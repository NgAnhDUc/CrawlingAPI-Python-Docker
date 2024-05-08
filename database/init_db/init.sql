CREATE DATABASE chotot_db CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;;
USE chotot_db;
CREATE TABLE Products (
  id INT NOT NULL AUTO_INCREMENT,
  ad_id INT NOT NULL,
  timedate NVARCHAR(512) NOT NULL,
  account_id INT NOT NULL,
  account_name NVARCHAR(512) NOT NULL,
  title TEXT NOT NULL,
  body NVARCHAR(1024) NOT NULL,
  category INT NOT NULL,
  category_name NVARCHAR(256) NOT NULL,
  area INT NOT NULL,
  area_name NVARCHAR(256) NOT NULL,
  region INT NOT NULL,
  region_name NVARCHAR(256) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  price_string NVARCHAR(256) NOT NULL,
  webp_image NVARCHAR(256) NULL,
  PRIMARY KEY (id),
  UNIQUE KEY (ad_id) 
);

