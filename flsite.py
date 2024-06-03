from flask import Flask, render_template, url_for

app = Flask(__name__)

menu = [
    {"name": "Главная", "url": "/"},
    {"name": "Статьи", "url": "/post"},
    {"name": "Добавить статью", "url": "/add_post"},
    {"name": "Контакты", "url": "/contact"}
]


@app.route("/")
def index():
    return render_template('index.html', title='Главная', menu=menu)


@app.route("/post")
def post():
    return render_template("post.html", title='Статьи', menu=menu)


@app.route("/add_post")
def add_post():
    return render_template("add_post.html", title='Добавить статью', menu=menu)


@app.route("/contact")
def contact():
    return render_template("contact.html", title='Контакты', menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page404.html", title='Станица не найдена', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
