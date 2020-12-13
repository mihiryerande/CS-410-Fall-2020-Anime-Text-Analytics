import app
import json_lines

def initialize():
    print("Dropping existing db")
    app.db.drop_all()
    print("Creating new db")
    app.db.create_all()
    genres = set()
    with open('source_code\scraper\scraped.jl', 'rb') as f:
        
        # Create Genres
        for item in json_lines.reader(f):
            for genre in item["mal genres"].split(","):
                genres.add(genre)
        i = 0
        for genre in genres:
            i += 1
            print("Adding genre", i)
            new_genre = app.Genre(name=genre)
            try:
                app.db.session.add(new_genre)
                app.db.session.commit()
            except Exception as e:
                print('There was an issue adding your genre', e)
    
    i = 0
    with open('source_code\scraper\scraped.jl', 'rb') as f:
        for item in json_lines.reader(f):
            i += 1
            print("Adding anime", i)
            # Create Animes
            new_anime = app.Anime(title=item["title"], description=item["description"])
            try:
                app.db.session.add(new_anime)
                app.db.session.commit()
            except Exception as e:
                print('There was an issue adding your anime', e)

            # Create Anime Genres
            for genre_key in item["mal genres"].split(","):
                genre = app.db.session.query(app.Genre).filter(app.Genre.name == genre_key).first()
                anime = app.db.session.query(app.Anime).filter(app.Anime.title == item["title"]).first()
                try:
                    anime.genres.append(genre)
                    app.db.session.commit()
                except Exception as e:
                    print('There was an issue adding your anime', e)

    with open('source_code\lda_output\genre_names.jl', 'rb') as f:
        i = 0
        for item in json_lines.reader(f):
            i += 1
            print("Adding lda genre", i)
            # Create LDA Genres
            new_lda_genre = app.LDAGenre(id=item["LDA Genre ID"], name=item["LDA Genre Name"])
            try:
                app.db.session.add(new_lda_genre)
                app.db.session.commit()
            except Exception as e:
                print('There was an issue adding your lda genre', e)
    with open('source_code\lda_output\genre_word_weights.jl', 'rb') as f:
        i = 0
        for item in json_lines.reader(f):
            i += 1
            print("Adding lda genre word weights", i)
            # Create LDA Genres
            lda_genre = app.db.session.query(app.LDAGenre).get(item["LDA Genre ID"])
            new_lda_genre_word = app.LDAGenreWord(word=item["Word"], weight=item["Word Weight"])
            new_lda_genre_word.lda_genre_id = lda_genre.id
            try:
                app.db.session.add(new_lda_genre_word)
                app.db.session.commit()
            except Exception as e:
                print('There was an issue adding your lda genre word', e)
    with open('source_code\\lda_output\\anime_genre_weights.jl', 'rb') as f:
        i = 0
        for item in json_lines.reader(f):
            i += 1
            print("Adding lda anime genre weights", i)
            # Create LDA Genres
            lda_genre = app.db.session.query(app.LDAGenre).get(item["LDA Genre ID"])
            anime = app.db.session.query(app.Anime).filter(app.Anime.title == item["Anime Title"]).first()
            new_anime_lda_genre_link = app.AnimeLDAGenreLink(lda_genre_id=lda_genre.id, anime_id=anime.id, weight=item["LDA Genre Weight"])
            try:
                app.db.session.add(new_anime_lda_genre_link)
                app.db.session.commit()
            except Exception as e:
                print('There was an issue adding your anime lda genre link', e)
    print(app.db.session.query(app.LDAGenre).first())
    print(app.db.session.query(app.LDAGenre).first().words)
    print(app.db.session.query(app.LDAGenre).first().animes)
    print("Done creating and loading db.")

    
initialize()