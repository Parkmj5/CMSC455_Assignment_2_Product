# /products (GET): Retrieve a list of available grocery products, including their names, prices, and
# quantities in stock.
# /products/product id (GET): Get details about a specific product by its unique ID.
# /products (POST): Allow the addition of new grocery products to the inventory with information
# such as name, price, and quantity.
from flask import Flask, jsonify, request
app = Flask(__name__)

products = [
    {"id": 1, "name": "onions", "price": 0.99, "units_in_stock": 2},
    {"id": 2, "name": "beef", "price": 12.99, "units_in_stock": 4},
    {"id": 3, "name": "shampoo", "price": 7.99, "units_in_stock": 6}
]


# Endpoint 1: Get all products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({"Products": products})


# Endpoint 2: Get a specific product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((product for product in products if product["id"] == product_id), None)
    if product:
        return jsonify({"Product": product})
    else:
        return jsonify({"Error": "Product not found"}), 404


# Endpoint 3: Create a new product
@app.route('/products', methods=['POST'])
def create_product():
    highest_id = products[-1].get("id")
    new_product = {
        "id": highest_id + 1,
        "name": request.json.get('name'),
        "price": round(float(request.json.get('price')), 2),
        "units_in_stock": int(request.json.get('units_in_stock'))
    }
    products.append(new_product)
    return jsonify({"Message": "Product created", "Product": new_product}), 201

# @app.route('/products/<int:product_id>', methods=['POST'])
# def change_quantity(product_id):
#     #product = next((product for product in products if product["id"] == product_id), None)
#     check_quantity = request.json.get("units_in_stock")
#     if check_quantity < 0:
#         products[product_id-1]["units_in_stock"] -= 1
#     else:
#         products[product_id - 1]["units_in_stock"] += 1
    # quantity = product.get('units_in_stock')
    # if operation == 'increment':
    #     product.update({"units_in_stock": quantity + 1})
    #     return jsonify({"Message": "Product quantity was incremented by one unit", "Product": product}), 201
    # elif operation == 'decrement':
    #     product.update({"units_in_stock": quantity - 1})
    #     return jsonify({"Message": "Product quantity was decremented by one unit", "Product": product}), 201

# Endpoint 4: Delete a product with specific ID
@app.route('/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    product = next((product for product in products if product["id"] == product_id), None)
    copy = product.copy()
    for i in range(len(products)):
        if products[i]['id'] == product_id:
            del products[i]
            return jsonify({"Message": "Product was removed", "Product": copy}), 201
    return jsonify({"Error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
