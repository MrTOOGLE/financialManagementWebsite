from flask import Flask, render_template, request, redirect, g, flash
import sqlite3
from models.DataBase import DataBase
from models.UserLogin import UserLogin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE='E:/_Python/finance/users.db'))
global dbase


login_manager = LoginManager(app)
login_manager.login_view = 'authorization'


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    connect = sqlite3.connect(app.config['DATABASE'])
    connect.row_factory = sqlite3.Row
    return connect


def get_db():
    """Соединение с БД, если оно еще не установлено"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = DataBase(db)


@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно было установлено"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


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
        user = dbase.getUserByMail(mail)
        try:
            if not check_password_hash(user[2], password):
                flash("Неверный пароль", "error")
            else:
                userLogin = UserLogin().create(user)
                login_user(userLogin)
                return redirect('profile')
        except Exception:
            flash("Аккаунт с этой почтой не зарегестрирован", "error")
    return render_template('authorization.html')


@app.route('/signIn', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        mail = request.form.get('Mail')
        password = request.form.get('Password')
        name = request.form.get('Name')
        balance = request.form.get('Balance')
        try:
            balance = int(balance)
            if len(password) > 3 and len(mail) > 3 and balance >= 0:
                password = generate_password_hash(password)
                if dbase.addUser(mail, password, name, balance):
                    flash("Вы успешно зарегестрировались", "success")
                    return redirect('signUp')
                else:
                    flash("Аккаунт с этой почтой уже зарегестрирован", "error")
            else:
                flash("Слишком короткий пароль/почта или баланс меньше 0", "error")
        except ValueError:
            flash("Баланс должен быть числом", "error")
    return render_template('registration.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/index')


@app.route('/profile')
@login_required
def profile():
    user = dbase.getUser(current_user.get_id())
    return render_template('profile.html', name=user[3], balance=user[4])


@app.route('/change_balance')
@login_required
def change_balance():
    return render_template('change_balance.html')


@app.route('/operations')
@login_required
def operations():
    return render_template('operations.html')


if __name__ == "__main__":
    app.run()
