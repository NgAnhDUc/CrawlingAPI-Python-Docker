import requests # type: ignore

products = []
url = "https://gateway.chotot.com/v1/public/ad-listing?limit=10&protection_entitlement=true&cg=5010&st=s,k&key_param_included=true"

respone = requests.get(url)

if respone.status_code == 200:
    print("get success")
    for item in respone.json().get('ads'):
        products.append({'id': item.get('ad_id')})
        products.append({'date': item.get('date')})
        products.append({'body': item.get('body')})
        products.append({'category': item.get('category')})
        products.append({'category_name': item.get('category_name')})
        products.append({'price': item.get('price')})
        products.append({'subject': item.get('subject')})

print(products)

    
    
