import sqlite3
import os
from flask import Flask, render_template, url_for, request, flash, session, redirect, g

from FDataBase import FDataBase

DATABASE = '/tmp/flsk.db'
DEBUG = True
SECRET_KEY = "431aad16756852cd4d33370cbe77cb14629c5743"

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsk.db')))


def connect_db():
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row
    return con


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', title='Pricing', menu=dbase.get_menu(), cursy=dbase.get_curses())


@app.route("/curs/<slug>")
def show_curs(slug):
    db = get_db()
    dbase = FDataBase(db)
    title, price, body = dbase.get_curs(slug)
    return render_template('curs.html', menu=dbase.get_menu(), title=title, price=price, body=body)


@app.route("/info")
def info():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('info.html', title='Информация', menu=dbase.get_menu())


@app.route("/add_curs", methods=["GET", "POST"])
def add_curs():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if len(request.form['title']) > 4 and len(request.form['body']) > 10:
            res = dbase.add_curs(request.form['title'], request.form['url'], request.form['body'],
                                 request.form['price'])
            if not res:
                flash("Ошибка добавления статьи", category="error")
            else:
                flash("Статья добавлена успешно", category="success")
        else:
            flash("Ошибка длины", category="error")

    return render_template('add_curs.html', title='Добавить курс', menu=dbase.get_menu())


@app.errorhandler(404)
def page_not_found(error):
    db = get_db()
    dbase = FDataBase(db)
    return render_template("page404.html", title='Станица не найдена', menu=dbase.get_menu())


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == '__main__':
    app.run(debug=True)
