import requests
from tmdb import tmdb_api
from time import ctime
from database import db_connection

moment = ctime()

db_cursor = db_connection.cursor
poster_list = []
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
        if response_json["poster_path"] is not None:
            poster_url = response_json["poster_path"]
            poster_dict = dict(movie_id=movie_id,poster_url=poster_url)
        else:
            continue
        poster_list.append(poster_dict)
        sql = "INSERT INTO `posters` (`MOVIE_ID`,`POSTER_URL`) " \
        "VALUES ('{0}','{1}')"
        db_cursor.execute(sql.format(movie_id,poster_url))
        ingest_log = "[" + moment + "] Ingested TMDB ID " + tmdb_id
        print(ingest_log)
        db_connection.database_connection.commit()