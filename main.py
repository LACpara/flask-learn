from flask import Flask, url_for, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, select
from markupsafe import escape
from pathlib import Path
import click

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(Path(app.root_path) / 'data.sqlite3')
app.config['SECRET_KEY'] = 'dev'

db = SQLAlchemy(app, model_class=Base)

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))

class Movie(db.Model):
    __tablename__ = "movie"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(60))
    year: Mapped[str] = mapped_column(String(4))

@app.cli.command('init-db')
@click.option('--drop', is_flag=True, help='Create after drop.')
def init_database(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")

@app.cli.command()
def forge():
    db.drop_all()
    db.create_all()

    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    
    db.session.commit()
    click.echo("Done.")

@app.context_processor
def inject_user():
    user = db.session.scalar(select(User))
    return {'user': user}

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.route("/", methods=['GET', "POST"])
@app.route("/index", methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def index():
    if request.method == 'POST':
        title = request.form.get('title').strip()
        year = request.form.get('title').strip()
        if not title or not year or len(year)>4 or len(title)>60:
            flash("Invalid input.")
            return redirect(url_for("index"))
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash("Item created.")
        return redirect(url_for("index"))

    movies = db.session.scalars(select(Movie)).all()
    return render_template('index.html', movies=movies)


@app.route("/movie/edit/<int:movie_id>", methods=['GET', 'POST'])
def edit(movie_id):
    movie = db.get_or_404(Movie, movie_id)
    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form.get('title').strip()
        year = request.form.get('year').strip()

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie) 


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = db.get_or_404(Movie, movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页


@app.route("/user/<name>")
def user_page(name):
    return f'User {escape(name)}'


@app.route("/test")
def test_url_for():
    print(url_for('index'))
    print(url_for('user_page', name='greyli'))
    print(url_for('user_page', name='peter'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return 'Test page'