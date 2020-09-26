import requests
from tmdb import tmdb_api
from time import ctime
from database import db_connection

moment = ctime()
db_cursor = db_connection.cursor
ext_ids_lst = []
movies_export_json = "../tmdb_daily_export_20200918/movie_ids_09_18_2020.json"
with open(movies_export_json, 'r', encoding="UTF-8") as f:
    tmdb_ids = [row.split(",")[1].split(":")[1] for row in f]
    for id in tmdb_ids:
        tmdb_id = str(id)
        response = requests.get("https://api.themoviedb.org/3/movie/" + tmdb_id + "/external_ids?api_key=" + tmdb_api.api_key)
        if response.status_code != 200:
            error_log = "[" + moment + "] Skipping TMDB ID " + tmdb_id + ". Invalid ID. Error code:" + str(response.status_code)
            print(error_log)
            continue
        response_json = response.json()
        ext_ids_lst.append(response_json)
        sql = "INSERT INTO `movie_external_id` (`MOVIE_ID`,`imdb_id`,`facebook_id`,`instagram_id`,`twitter_id`) " \
              "VALUES (%(id)s,%(imdb_id)s,%(facebook_id)s,%(instagram_id)s,%(twitter_id)s)"
        db_cursor.executemany(sql, ext_ids_lst)
        db_connection.database_connection.commit()
        ingest_log = "[" + moment + "] Ingested TMDB ID " + tmdb_id
        print(ingest_log)
