from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="",
    password="",
    database="objects.db"
)

# Создание таблицы если не существует
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS products (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), description TEXT, price DECIMAL(10, 2), image_url VARCHAR(255), weight DECIMAL(255, 2), size DECIMAL(255, 255, 255))")

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template('addProduct.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    image_url = request.form['image_url']
    weight = request.form['weight']
    size = request.form['size']

    cursor = db.cursor()
    cursor.execute("INSERT INTO products (name, description, price, image_url, weight, size) VALUES (%s, %s, %s, %s, s%, s%)", (name, description, price, image_url, weight, size))
    db.commit()
    return 'Success'

if __name__ == '__main__':
    app.run(debug=True)
