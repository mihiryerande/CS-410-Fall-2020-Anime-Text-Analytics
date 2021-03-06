from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_msearch import Search


### DB Connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['MSEARCH_BACKEND'] = 'whoosh'
db = SQLAlchemy(app)
search = Search()
search.init_app(app)

# Association tables
class AnimeLDAGenreLink(db.Model):
    ''' Links Animes to LDA Genres '''
    __tablename__ = 'anime_lda_genre_link'
    lda_genre_id = db.Column(db.Integer(), db.ForeignKey('lda_genres.id'), primary_key=True)
    anime_id = db.Column(db.Integer, db.ForeignKey('animes.id'), primary_key=True)
    weight = db.Column(db.Integer(), nullable=False)

# Links Animes to Genres
anime_genres = db.Table('anime_genres',
    db.Column('anime_id', db.Integer, db.ForeignKey('animes.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id')),
)

class SimilarAnimeLink(db.Model):
    ''' Links similar anime with self-referential many-to-many relationship'''
    __tablename__ = 'similar_anime_link'
    anime_1_id = db.Column(db.Integer(), db.ForeignKey('animes.id'), primary_key=True)
    anime_2_id = db.Column(db.Integer, db.ForeignKey('animes.id'), primary_key=True)
    distance = db.Column(db.Integer(), nullable=False)

### Models
class LDAGenreWord(db.Model):
    '''Keywords for LDA Genres'''
    __tablename__ = 'lda_genre_words'
    __searchable__ = ['word']
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(200), nullable=False)
    weight = db.Column(db.Integer(), nullable=False)
    lda_genre_id = db.Column(db.Integer(), db.ForeignKey('lda_genres.id'))
    
    def __repr__(self):
        return '<LDA Genre Word %r, %s>' % (self.id, self.word)



class LDAGenre(db.Model):
    ''' LDA Genre model '''
    __tablename__ = 'lda_genres'
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    words = db.relationship('LDAGenreWord', backref='LDAGenre')
    animes = db.relationship(
        'Anime',
        secondary='anime_lda_genre_link'
    )

    def __repr__(self):
        return '<LDA Genre %r, %s>' % (self.id, self.name)


class Anime(db.Model):
    ''' Anime model with title and description '''
    __tablename__ = 'animes'
    __searchable__ = ['title', 'description']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text(), default="")
    genres = db.relationship('Genre', secondary='anime_genres', backref='anime')
    similar_animes = db.relationship('SimilarAnimeLink', backref='Anime')
    similar_animes = db.relationship(
        'Anime', 
        secondary="similar_anime_link",
        primaryjoin=(SimilarAnimeLink.anime_1_id == id),
        secondaryjoin=(SimilarAnimeLink.anime_2_id == id),
        backref=db.backref('anime1s', lazy='dynamic'),
        lazy='dynamic'
    )


    lda_genres = db.relationship(
        'LDAGenre',
        secondary='anime_lda_genre_link'
    )

    def __repr__(self):
        return '<Anime %r, %s>' % (self.id, self.title)

class Genre(db.Model):
    ''' Genre model with name '''
    __tablename__ = 'genres'
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    animes = db.relationship('Anime', secondary='anime_genres', backref='genre')

    def __repr__(self):
        return '<Genre %r, %s>' % (self.id, self.name)

### Routes
@app.route('/', methods=['GET'])
def index():
    ''' Home page, displays information on site '''
    lda_genres = LDAGenre.query.order_by(LDAGenre.id).all()
    carousel_animes = []
    for lda_genre in lda_genres:
        anime_weights = AnimeLDAGenreLink.query.filter(AnimeLDAGenreLink.lda_genre_id == lda_genre.id).order_by(db.desc(AnimeLDAGenreLink.weight))[0:4]
        lda_genre_animes = []
        for item in anime_weights:
            lda_genre_animes.append(Anime.query.get(item.anime_id))
        carousel_animes.append(lda_genre_animes)
    animes = Anime.query.order_by(Anime.title).all()
    return render_template('index.html', lda_genres=lda_genres, carousel_animes=carousel_animes, animes=animes)

@app.route('/search')
def search():
    ''' Search page, uses msearch preprocessed inverted index to do full text search of relevant models '''
    query = request.args.get('q')
    if query == None:
        query = " "
    lda_genres = LDAGenre.query.msearch(query,limit=20).all()
    words = LDAGenreWord.query.msearch(query,limit=20).all()
    genres = Genre.query.msearch(query,limit=20).all()
    animes = Anime.query.msearch(query,limit=20).all()
    for word in words:
        if word.lda_genre_id not in list(map(lambda x: x.id, lda_genres)):
            lda_genres.append(LDAGenre.query.get(word.lda_genre_id))
    return render_template('search.html', lda_genres=lda_genres, genres=genres, animes=animes)

@app.route('/anime')
@app.route('/anime/page/<int:page_num>')
def anime_list(page_num=1):
    ''' List page for all anime '''
    animes = Anime.query.order_by(Anime.title).paginate(page=page_num, per_page=20)
    lda_genres = []
    for anime in animes.items:
        anime_weight = AnimeLDAGenreLink.query.filter(AnimeLDAGenreLink.anime_id == anime.id).order_by(db.desc(AnimeLDAGenreLink.weight))[0]
        lda_genres.append(LDAGenre.query.get(anime_weight.lda_genre_id))
    return render_template('anime_list.html', animes=animes, lda_genres=lda_genres)

@app.route('/anime/<int:id>')
def anime(id):
    ''' Page for individual animes with info on related genres and LDA genres '''
    anime = Anime.query.get_or_404(id)
    anime_weights = AnimeLDAGenreLink.query.filter(AnimeLDAGenreLink.anime_id == id).order_by(db.desc(AnimeLDAGenreLink.weight))[0:10]
    lda_genres = []
    for item in anime_weights:
        lda_genres.append(LDAGenre.query.get(item.lda_genre_id))
    similar_anime_links = SimilarAnimeLink.query.filter(SimilarAnimeLink.anime_1_id == id).order_by(db.asc(SimilarAnimeLink.distance)) 
    similar_animes = []
    for item in similar_anime_links:
        similar_animes.append(Anime.query.get(item.anime_2_id))
    return render_template('anime.html', anime=anime, anime_weights=anime_weights, lda_genres=lda_genres, similar_anime_links=similar_anime_links, similar_animes=similar_animes)

@app.route('/genre')
@app.route('/genre/page/<int:page_num>')
def genre_list(page_num=1):
    ''' List page for all genres '''
    genres = Genre.query.order_by(Genre.name).paginate(page=page_num, per_page=20)
    return render_template('genre_list.html', genres=genres)

@app.route('/genre/<int:id>')
def genre(id):
    ''' Page for individual genres with info on related animes '''
    genre = Genre.query.get_or_404(id)
    return render_template('genre.html', genre=genre)

@app.route('/lda_genre')
@app.route('/lda_genre/page/<int:page_num>')
def lda_genre_list(page_num=1):
    ''' List page for all LDA Genres '''
    lda_genres = LDAGenre.query.order_by(LDAGenre.id).paginate(page=page_num, per_page=20)
    animes = []
    for lda_genre in lda_genres.items:
        anime_weights = AnimeLDAGenreLink.query.filter(AnimeLDAGenreLink.lda_genre_id == lda_genre.id).order_by(db.desc(AnimeLDAGenreLink.weight))[0:3]
        lda_genre_animes = []
        for item in anime_weights:
            lda_genre_animes.append(Anime.query.get(item.anime_id))
        animes.append(lda_genre_animes)
    words = []
    for lda_genre in lda_genres.items:
        words.append(LDAGenreWord.query.filter(LDAGenreWord.lda_genre_id == lda_genre.id).order_by(db.desc(LDAGenreWord.weight))[0:3])
    return render_template('lda_genre_list.html', lda_genres=lda_genres, animes=animes, words=words)

@app.route('/lda_genre/<int:id>')
def lda_genre(id):
    ''' Page for individual LDA Genres with info on related animes and keywords '''
    lda_genre = LDAGenre.query.get_or_404(id)
    anime_weights = AnimeLDAGenreLink.query.filter(AnimeLDAGenreLink.lda_genre_id == id).order_by(db.desc(AnimeLDAGenreLink.weight))[0:10]
    animes = []
    for item in anime_weights:
        animes.append(Anime.query.get(item.anime_id))
    words = LDAGenreWord.query.filter(LDAGenreWord.lda_genre_id == id).order_by(db.desc(LDAGenreWord.weight))[0:10]
    return render_template('lda_genre.html', lda_genre=lda_genre, anime_weights=anime_weights, animes=animes, words=words)

### Runtime
if __name__ == "__main__":
    app.run(debug=True)