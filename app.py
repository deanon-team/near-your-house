from flask import Flask, render_template, url_for, app, request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3
import os
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Bhj2fjk7Rnl1TYE1snl5YR3FbmTRv52mkUrtv4JK'
db = SQLAlchemy(app)
app.permanent_session_lifetime = datetime.timedelta(days=30)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    typeofuser = db.Column(db.Integer)
    
    def __repr__(self):
        return '<Users %r>' % self.id
    
class products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    weight = db.Column(db.Float, nullable=True)
    size = db.Column(db.String(50), nullable=True)
    
    def __repr__(self):
        return '<Product %r>' % self.id
    



@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalog')
@login_required
def catalog():
    return render_template('catalog.html')

@app.route('/user')
def user():
    return 'user'

@app.route('/about')
def about():
    return render_template('about.html')


#Все страницы которые касаються регистрации/входа пользователей на сайт
@app.route('/login', methods=['GET', 'POST'])
def login():
    #if current_user.is_authenticated: return render_template('index.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                
                return "Введён невепный пароль"
        else:
            return "Неправильно введён логин или такого пользователся не существует"
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form['password1'] == request.form['password2']:
            userdata = users(username=request.form['username'], password=request.form['password1'], email=request.form['email'], typeofuser=request.form['userType'])
            try:
                db.session.add(userdata)
                db.session.commit()
                return 'Вы зарегестрировались!'
            except:
                return 'Произошла ошибка'
            #сохранение инфы о пользователе
            #sqlite3.Cursor.execute('INSERT INTO user_data (username, email, password, typeofuser) VALUES (?, ?, ?, ?)', (username, email, password, typeofuser))
            #conn.commit() # type: ignore

        else:
            return 'Пароли не совпадают'
    else:
        return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.username}! This is the dashboard.'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are logged out'



if __name__ == '__main__':
    with app.app_context(): db.create_all()  # Создаем таблицы в базе данных
    app.run(debug=True)