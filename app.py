from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__,)

CSV_FILE = 'products.csv'



# Read products from CSV
def read_products():
    with open(CSV_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

@app.route('/')
def home():
    products = read_products()
    sort_by = request.args.get('sort_by', 'name')  # Default to sorting by name

    if sort_by == 'rating':
        products = sorted(products, key=lambda x: float(x['rating']), reverse=True)
    elif sort_by == 'price':
        # Sort by effective price: sale_price if available, otherwise price
        for product in products:
            product['effective_price'] = int(
                product['sale_price'].strip('₹') if product['sale_price'].strip('₹') else product['price'].strip('₹')
            )
        products = sorted(products, key=lambda x: x['effective_price'])

    return render_template('index.html', products=products, sort_by=sort_by)


@app.route('/product/<name>')
def product_detail(name):
    products = read_products()
    product = next((p for p in products if p['name'] == name), None)
    if not product:
        return "Product not found", 404
    return render_template('product_detail.html', product=product)

@app.route('/api/products')
def api_products():
    products = read_products()
    return jsonify(products)

if __name__ == '__main__':
    app.run(debug=True)