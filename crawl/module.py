import json
import requests

def crawl_data():
    products = []

    url = "https://gateway.chotot.com/v1/public/ad-listing?limit=100&protection_entitlement=true&cg=5010&st=s,k&key_param_included=true"

    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to get data from Chotot API")

    print("Run crawl service")
    for item in response.json().get("ads"):
        product = {
            "ad_id": item.get("ad_id"),
            "timedate": item.get("date"),
            "account_id": item.get("account_id"),
            "account_name": item.get("account_name"),
            "title": item.get("subject"),
            "body": item.get("body"),
            "category": item.get("category"),
            "category_name": item.get("category_name"),
            "area": item.get("area"),
            "area_name": item.get("area_name"),
            "region": item.get("region"),
            "region_name": item.get("region_name"),
            "price": item.get("price"),
            "price_string": item.get("price_string"),
            "webp_image": item.get("webp_image"),
        }
        products.append(product)

    with open("products.json", "w", encoding="utf-8") as file:
        json.dump(products, file, ensure_ascii=False, indent=4)

    try:
        response_api = requests.post('http://api_service:8000/crawl', json=products)
        response_api.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        print(products)
    except requests.exceptions.RequestException as e:
        print('Error:', e)

    return products