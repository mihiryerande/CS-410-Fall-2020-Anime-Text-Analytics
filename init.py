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
            print("Adding genre", i, genre)
            new_genre = app.Genre(name=genre)
            try:
                app.db.session.add(new_genre)
            except Exception as e:
                print('There was an issue adding your genre', e)
        try:
            app.db.session.commit()
        except Exception as e:
            print('There was an issue adding your genre', e)
    
    with open('source_code\scraper\scraped.jl', 'rb') as f:
        i = 0
        for item in json_lines.reader(f):
            i += 1
            print("Adding anime", i, item["title"])
            # Create Animes
            new_anime = app.Anime(title=item["title"], description=item["description"])
            try:
                app.db.session.add(new_anime)
            except Exception as e:
                print('There was an issue adding your anime', e)
        try:
            app.db.session.commit()
        except Exception as e:
            print('There was an issue adding your anime', e)


    with open('source_code\scraper\scraped.jl', 'rb') as f:
        i = 0
        for item in json_lines.reader(f):
            i += 1
            print("Adding anime genre", i, item["title"], item["mal genres"])
            # Create Anime Genres
            for genre_key in item["mal genres"].split(","):
                genre = app.db.session.query(app.Genre).filter(app.Genre.name == genre_key).first()
                anime = app.db.session.query(app.Anime).filter(app.Anime.title == item["title"]).first()
                try:
                    anime.genres.append(genre)
                except Exception as e:
                    print('There was an issue adding your anime genre', e, genre)
            try:
                app.db.session.commit()
            except Exception as e:
                print('There was an issue adding your anime genre', e)

    with open('source_code\lda_output\genre_names.jl', 'rb') as f:
        i = 0
        for item in json_lines.reader(f):
            i += 1
            print("Adding lda genre", i)
            # Create LDA Genres
            new_lda_genre = app.LDAGenre(id=item["LDA Genre ID"], name=item["LDA Genre Name"])
            try:
                app.db.session.add(new_lda_genre)
            except Exception as e:
                print('There was an issue adding your lda genre', e)
        try:
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
            except Exception as e:
                print('There was an issue adding your lda genre word', e)
        try:
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
            except Exception as e:
                print('There was an issue adding your anime lda genre link', e)
        try:
            app.db.session.commit()
        except Exception as e:
            print('There was an issue adding your anime lda genre link', e)

    with open('source_code\\lda_distance\\lda_distance.jl', 'rb') as f:
        i = 0
        for item in json_lines.reader(f):
            i += 1
            print("Adding anime similarity", i)
            # Create anime similarities
            anime_1 = app.db.session.query(app.Anime).filter(app.Anime.title == item["Title 1"]).first()
            anime_2 = app.db.session.query(app.Anime).filter(app.Anime.title == item["Title 2"]).first()
            new_similar_anime_link = app.SimilarAnimeLink(anime_1_id=anime_1.id, anime_2_id=anime_2.id, distance=item["Distance"])
            try:
                app.db.session.add(new_similar_anime_link)
            except Exception as e:
                print('There was an issue adding your anime lda genre link', e)
        try:
            app.db.session.commit()
        except Exception as e:
            print('There was an issue adding your anime lda genre link', e) 

    print("Done creating and loading db.")

    
initialize()