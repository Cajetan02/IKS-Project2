
from flask import Flask, render_template, jsonify
from bs4 import BeautifulSoup
import requests
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (name TEXT, price TEXT, website TEXT, rating TEXT, authenticity TEXT, url TEXT, image_url TEXT)''')
    conn.commit()
    conn.close()

def scrape_products():
    urls = [
        'https://www.runwayindia.in/',
        'https://www.amazon.in/karigar',
        'https://gaatha.com/',
        'https://www.chanderiyaan.com/',
        'https://www.exclusivelane.com/'
    ]
    products = []
    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        for product in soup.find_all('div', class_='product'):
            name = product.find('h3').text
            price = product.find('span', class_='price').text
            website = url.split('/')[2]
            rating = product.find('span', class_='rating').text
            authenticity = "Verified"  # Add your logic to get authenticity rating
            product_url = product.find('a')['href']
            image_url = product.find('img')['src']

            products.append((name, price, website, rating, authenticity, product_url, image_url))

    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.executemany('''INSERT INTO products (name, price, website, rating, authenticity, url, image_url) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)''', products)
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    products = c.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/api/products')
def api_products():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    products = c.fetchall()
    conn.close()
    
    product_list = [{"name": p[0], "price": p[1], "website": p[2], "rating": p[3], "authenticity": p[4], "url": p[5], "image_url": p[6]} for p in products]
    return jsonify(product_list)

if __name__ == '__main__':
    init_db()
    scrape_products()
    app.run(debug=True)
    