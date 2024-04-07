from flask import Flask, render_template, url_for, app, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
import sqlite3
import os
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.permanent_session_lifetime = datetime.timedelta(days=30)
login_manager = LoginManager(app)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    typeofuser = db.Column(db.Integer)
    
    def __repr__(self):
        return '<Users %r>' % self.id
    





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user')
def user():
    return 'user'


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        datausers = users.query.all()
        for user in datausers:
            if user.username == request.form['username']:
                if user.password == request.form['password']:
                    return "Вы успешно вошли"
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
            username = request.form['username']
            email = request.form['email']
            password = request.form['password1']
            typeofuser = request.form['userType']
            
            userdata = users(username=username, password=password, email=email, typeofuser=typeofuser)
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


if __name__ == "__main__":
    app.run(debug=True)