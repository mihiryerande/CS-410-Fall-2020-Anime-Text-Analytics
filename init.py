import app
import json_lines

def initialize():
    print("Dropping existing db")
    app.db.drop_all()
    print("Creating new db")
    app.db.create_all()
    genres = set()
    with open('scraper\scraped.jl', 'rb') as f:
        
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
    with open('scraper\scraped.jl', 'rb') as f:
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
    
    print("Done creating and loading db.")

    
initialize()