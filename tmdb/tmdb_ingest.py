import requests
from tmdb import tmdb_api
from time import ctime
from database import db_connection

moment = ctime()
db_cursor = db_connection.cursor

movies_export_json = "../tmdb_daily_export_20200918/movie_ids_09_18_2020.json"
with open(movies_export_json, 'r', encoding="UTF-8") as f:
    tmdb_ids = [row.split(",")[1].split(":")[1] for row in f]
    for id in tmdb_ids:
        tmdb_id = str(id)
        response = requests.get("https://api.themoviedb.org/3/movie/" + tmdb_id + "?api_key=" + tmdb_api.api_key + "&language=en-US")
        if response.status_code != 200:
            error_log = "[" + moment + "] Skipping TMDB ID " + tmdb_id + ". Invalid ID. Error code:" + str(response.status_code)
            print(error_log)
            continue
        response_json = response.json()
        movie_id = response_json["id"]
        title = response_json["title"][:500]
        org_language = response_json["original_language"]
        org_title = response_json["original_title"][:500]
        if response_json["overview"] is not None:
            overview = response_json["overview"][:1000]
        else:
            continue
        tagline = response_json["tagline"][:500]
        movie_dict = dict(movie_id=movie_id, title=title, org_title=org_title, org_language=org_language,
                          tagline=tagline, overview=overview)
        movie_list = []
        movie_list.append(movie_dict)
        sql = "INSERT INTO `movie_details` (`MOVIE_ID`,`TITLE`,`ORG_TITLE`,`ORG_LANGUAGE`,`TAGLINE`,`OVERVIEW`) " \
              "VALUES (%(movie_id)s,%(title)s,%(org_title)s,%(org_language)s,%(tagline)s,%(overview)s)"
        db_cursor.executemany(sql, movie_list)
        db_connection.database_connection.commit()
        genres = response_json["genres"]
        for g in range(len(genres)):
            genre_id = genres[g]["id"]
            genre_dict = dict(movie_id=movie_id,genre_id=genre_id)
            genre_list = []
            genre_list.append(genre_dict)
            sql = "INSERT INTO `movie_genres` (`MOVIE_ID`,`GENRE_ID`) " \
               "VALUES (%(movie_id)s,%(genre_id)s)"
            db_cursor.executemany(sql,genre_list)
            db_connection.database_connection.commit()
        ingest_log = "[" + moment + "] Ingested TMDB ID " + tmdb_id + ": " + title
        print(ingest_log)
