from flask import Flask, render_template, request, redirect
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime

Base = declarative_base()
app = Flask(__name__)


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    intro = Column(String(300), nullable=False)
    text = Column(Text)

    def __repr__(self):
        return '<Article %r>' % self.id


engine = create_engine('sqlite:///Article.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = session.query(Article).order_by(Article.id.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = session.query(Article).get(id)
    return render_template("posts_detail.html", article=article)


@app.route('/posts/<int:id>/del')
def posts_delete(id):
    article = session.query(Article).get(id)
    try:
        session.delete(article)
        session.commit()
        return redirect('/posts')
    except:
        session.rollback()
        return "При удалении статьи произошла ошибка"


@app.route('/posts/<int:id>/update', methods=['GET', 'POST'])
def post_update(id):
    article = session.query(Article).get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template("post_update.html", article=article)


@app.route('/create-article', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            session.add(article)
            session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create-article.html")


if __name__ == '__main__':
    app.run(debug=True)