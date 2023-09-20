#/products (GET): Retrieve a list of available grocery products, including their names, prices, and
#quantities in stock.
#/products/product id (GET): Get details about a specific product by its unique ID.
#/products (POST): Allow the addition of new grocery products to the inventory with information
#such as name, price, and quantity.

import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'products.sqlite')
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(precision=2), nullable=False)
    in_stock = db.Column(db.Integer, default=1)

# Endpoint 1: Get all tasks
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{"id": product.id, "name": product.name, "price": product.price,
                     "quantity in stock": product.in_stock} for product in products]
    return jsonify({"products": product_list})

# Endpoint 2: Get a specific product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({"Product": {"id": product.id, "name": product.name, "price": product.price,
                     "quantity in stock": product.in_stock}})
    else:
        return jsonify({"Error": "Product not found"}), 404

# Endpoint 3: Create a new task
@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    if "name" not in data:
        return jsonify({"error": "Product name is required"}), 400

    new_product = Product(name=data['title'], in_stock=True)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product created", "Product": {"id": new_product.id, "name": new_product.name,
                                                              "price": new_product.price, "quantity in stock": new_product.in_stock}}), 201

if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)