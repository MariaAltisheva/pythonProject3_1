from __future__ import annotations

from flask import Flask, Blueprint, render_template, current_app, request
from werkzeug.exceptions import abort

from bp_posts.dao.comment import Comment
from bp_posts.dao.comment_dao import CommentDAO
from bp_posts.dao.post import Post
from config import DATA_PATH_POSTS, DATA_PATH_COMMENTS
from bp_posts.dao.post_dao import PostDAO

#Создаем блупринт
bp_posts = Blueprint("bp_posts", __name__, template_folder="templates")

# Создаем объекты доступа к данным

post_dao = PostDAO(DATA_PATH_POSTS)
comments_dao = CommentDAO(DATA_PATH_COMMENTS)



@bp_posts.route("/")
def page_posts_index():
    """Страница всех постов"""
    all_posts = post_dao.get_all()
    return render_template("index.html", posts=all_posts)

@bp_posts.route("/posts/<int:pk>/")
def page_posts_single(pk: int):
    """Страница одного поста"""
    post: Post | None = post_dao.get_by_pk(pk)
    comments: list[Comment] = comments_dao.get_comments_by_post_pk(pk)
    comments_len = len(comments)
    if post is None:
        abort(404)

    return render_template("post.html", post=post, comments=comments, comments_len=len(comments))

@bp_posts.route("/users/<user_name>")
def page_posts_by_user(user_name: str):
    """Возвращает посты пользователя"""
    posts = post_dao.get_by_poster(user_name)

    if posts == []:
        abort(404, "Такого пользователя нет")


    return render_template("user-feed.html", posts=posts,user_name=user_name)

@bp_posts.route("/search/")
def page_posts_search():
    """Возвращает результаты поиска"""

    query:str = request.args.get("s", "")

    if query == "":
        posts = []
    else:
        posts = post_dao.search_in_content(query)

    return render_template("search.html", posts=posts, query=query, posts_len=len(posts))