def Filter_products(products, category_name, min_price):
    result = []

    for product in products:
        if product['category'] == category_name and product['price'] >= min_price:
            result.append(product['name'])

    return result


# ✅ DEFINE products BEFORE calling function
products = [
    {'name': 'Laptop', 'category': 'Electronics', 'price': 50000},
    {'name': 'Mouse', 'category': 'Electronics', 'price': 500},
    {'name': 'Shirt', 'category': 'Clothing', 'price': 1200},
    {'name': 'Jeans', 'category': 'Clothing', 'price': 2000}
]

print(Filter_products(products, 'Electronics', 1000))