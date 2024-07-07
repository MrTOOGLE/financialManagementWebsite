from flask import Flask, render_template, request, redirect
import sqlite3
from functions.authNreg import closeDB

app = Flask(__name__)


@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contacts")
def contacts():
    return render_template('contacts.html')


@app.route("/signUp", methods=['GET', 'POST'])
def authorization():
    if request.method == 'POST':
        mail = request.form.get('Mail')
        password = request.form.get('Password')
        db = sqlite3.connect('users.db')
        cursor = db.cursor()
        cursor.execute(('''SELECT password FROM passwords WHERE mail = '{}';''').format(mail))
        pas = cursor.fetchall()
        closeDB(cursor, db)
        try:
            if pas[0][0] != password:
                return render_template('badAuth.html')
        except Exception as e:
            return render_template('badAuth.html')
        # TODO: переделать когда сделаю страницу юзера
        return redirect('index')
    return render_template('authorization.html')


@app.route('/signIn', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        mail = request.form.get('Mail')
        password = request.form.get('Password')
        db = sqlite3.connect('users.db')
        cursor = db.cursor()
        sql_insert = '''INSERT INTO passwords VALUES('{}','{}');'''.format(mail, password)
        cursor.execute(sql_insert)
        db.commit()
        closeDB(cursor, db)
        return render_template('successfulReg.html')
    return render_template('registration.html')


if __name__ == "__main__":
    app.run()
