import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_db", user="postgres", password="2004", host="localhost", port="5432")
cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            # Исключение пустого логина или пароля
            if username == "" or password == "":
                return render_template('empty.html')
            cursor.execute("SELECT * FROM service.users")
            for element in cursor:
                if element[2] == username and element[3] == password:
                    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s",
                                   (str(username), str(password)))
                    records = list(cursor.fetchall())
                    return render_template('account.html', full_name=records[0][1],
                                           login=records[0][2], password=records[0][3])
            else:
                # Исключение неправильного пароля
                cursor.execute("SELECT * FROM service.users")
                for element in cursor:
                    if element[2] == username and element[3] != password:
                        return render_template('wrong.html')
                else:
                    # Исключение несуществующего пользователя
                    return render_template('error.html')
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        # Исключение пустого логина или имени или пароля
        if name == "" or login == "" or password == "":
            return render_template('emptyreg.html')
        # Исключение повтора логина
        cursor.execute("SELECT * FROM service.users")
        for element in cursor:
            if element[2] == login:
                return render_template('tlae.html')
        else:
            cursor.execute(
                'INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                (str(name), str(login), str(password)))
            conn.commit()
            return redirect('/login/')
    return render_template('registration.html')


app.run()
