from flask import Flask, jsonify, request
app = Flask(__name__)

# Sample Data
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
    new_product = {
        "id": len(products) + 1,
        "name": request.json.get('name'),
        "price": round(float(request.json.get('price')), 2),
        "units_in_stock": int(request.json.get('units_in_stock'))
    }
    products.append(new_product)
    return jsonify({"Message": "Product created", "Product": new_product}), 201

# Endpoint 4: Change the units available of a product
@app.route('/products/<int:product_id>', methods=['POST'])
def change_quantity(product_id):
    check_quantity = request.json.get("units_in_stock")
    product = next((product for product in products if product["id"] == product_id), None)
    # Subtract one unit from product availability since one unit was added to cart
    if check_quantity < 0:
        products[product_id - 1]["units_in_stock"] -= 1
        return jsonify({"Message": "Product quantity was decremented by one unit", "Product": product}), 201
    # Add one unit to product availability since one unit was removed from cart
    else:
        products[product_id - 1]["units_in_stock"] += 1
        return jsonify({"Message": "Product quantity was incremented by one unit", "Product": product}), 201

if __name__ == '__main__':
    app.run(debug=True)
