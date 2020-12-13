from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

### Models

class Anime(db.Model):
    __tablename__ = 'animes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), default="")
    genres = db.relationship('Genre', secondary='anime_genres', backref='anime')
    # anime_genres = db.relationship('AnimeGenre', backref='anime')
    # anime_lda_genres = db.relationship('AnimeLDAGenre', backref='anime')

    def __repr__(self):
        return '<Anime %r, %s>' % (self.id, self.title)

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    animes = db.relationship('Anime', secondary='anime_genres', backref='genre')

    def __repr__(self):
        return '<Genre %r, %s>' % (self.id, self.name)

anime_genres = db.Table('anime_genres',
    db.Column('anime_id', db.Integer, db.ForeignKey('animes.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id')),
)

# class LDAGenre(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     anime_ldagenres = db.relationship('AnimeLDAGenre', backref='LDAGenre')

#     def __repr__(self):
#         return '<LDA Genre %r, %s>' % (self.id, self.name)


### Routes

@app.route('/', methods=['POST', 'GET'])
def index():
    genres = Genre.query.order_by(Genre.name).all()
    animes = Anime.query.order_by(Anime.title).all()
    return render_template('index.html', genres=genres, animes=animes)

@app.route('/anime')
@app.route('/anime/page/<int:page_num>')
def anime_list(page_num=1):
    animes = Anime.query.order_by(Anime.title).paginate(page=page_num, per_page=20)
    print("page_num:", page_num)
    print(animes.items[0])
    return render_template('anime_list.html', animes=animes)

@app.route('/anime/<int:id>')
def anime(id):
    anime = Anime.query.get_or_404(id)
    return render_template('anime.html', anime=anime)

@app.route('/genre')
@app.route('/genre/page/<int:page_num>')
def genre_list(page_num=1):
    genres = Genre.query.order_by(Genre.name).paginate(page=page_num, per_page=20)
    print("page_num:", page_num)
    print(genres.items)
    return render_template('genre_list.html', genres=genres)

@app.route('/genre/<int:id>')
def genre(id):
    genre = Genre.query.get_or_404(id)
    return render_template('genre.html', genre=genre)




### Runtime
if __name__ == "__main__":
    # from init import initialize
    # initialize()
    app.run(debug=True)