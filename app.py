import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


# Cargar las variables de entorno
load_dotenv()

# Crear instancia de Flask
app = Flask(__name__)


# ==========================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ==========================================

database_url = os.getenv('DATABASE_URL')

# Usar psycopg2
if database_url:
    database_url = database_url.replace(
        'postgresql://',
        'postgresql+psycopg2://',
        1
    )

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ==========================================
# MODELO CATEGORY
# ==========================================

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )


# ==========================================
# MODELO POST
# ==========================================

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(
        db.String(200),
        nullable=False
    )
    content = db.Column(
        db.Text,
        nullable=False
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id'),
        nullable=True
    )

    category = db.relationship(
        'Category',
        backref=db.backref('posts', lazy=True)
    )


# ==========================================
# MOSTRAR POSTS
# ==========================================

@app.route('/')
def index():
    posts = Post.query.all()
    categories = Category.query.all()

    return render_template(
        'index.html',
        posts=posts,
        categories=categories
    )


# ==========================================
# AGREGAR POST
# ==========================================

@app.route('/post/new', methods=['GET', 'POST'])
def add_post():

    if request.method == 'POST':

        title = request.form['title']
        content = request.form['content']
        category_id = request.form.get('category_id')

        new_post = Post(
            title=title,
            content=content,
            category_id=category_id
        )

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('index'))

    categories = Category.query.all()

    return render_template(
        'create_post.html',
        categories=categories
    )


# ==========================================
# ACTUALIZAR POST
# ==========================================

@app.route('/post/update/<int:id>', methods=['GET', 'POST'])
def update_post(id):

    post = Post.query.get(id)

    if request.method == 'POST':

        post.title = request.form['title']
        post.category_id = request.form['category_id']
        post.content = request.form['content']

        db.session.commit()

        return redirect(url_for('index'))

    categories = Category.query.all()

    return render_template(
        'update_post.html',
        post=post,
        categories=categories
    )


# ==========================================
# ELIMINAR POST
# ==========================================

@app.route('/posts/delete/<int:id>')
def delete_post(id):

    post = Post.query.get(id)

    if post:
        db.session.delete(post)
        db.session.commit()

    return redirect(url_for('index'))


# ==========================================
# EJECUTAR APLICACIÓN
# ==========================================

if __name__ == '__main__':
    app.run(debug=True)