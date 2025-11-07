from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import select

from ..models import Movie
from ..extensions import db


main_bp = Blueprint("main", __name__)


@main_bp.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form.get("name")
        if not name or len(name) > 20:
            flash("Invalid input.")
            return redirect(url_for("main.settings"))
        current_user.name = name
        db.session.commit()
        flash("Settings updated.")
        return redirect(url_for('main.index'))
    return render_template('settings.html')



@main_bp.route("/", methods=['GET', "POST"])
def index():
    if request.method == 'POST':
        title = request.form.get('title').strip()
        year = request.form.get('year').strip()
        if not title or not year or len(year)>4 or len(title)>60:
            flash("Invalid input.")
            return redirect(url_for("main.index"))
        movie = Movie(title=title, year=year)
        db.session.add(movie)
        db.session.commit()
        flash("Item created.")
        return redirect(url_for("main.index"))

    movies = db.session.scalars(select(Movie)).all()
    return render_template('index.html', movies=movies)


@main_bp.route("/movie/edit/<int:movie_id>", methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = db.get_or_404(Movie, movie_id)
    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form.get('title').strip()
        year = request.form.get('year').strip()

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('main.edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('main.index'))  # 重定向回主页

    return render_template('edit.html', movie=movie) 


@main_bp.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required
def delete(movie_id):
    movie = db.get_or_404(Movie, movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('main.index'))  # 重定向回主页