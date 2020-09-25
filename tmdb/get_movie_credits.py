import requests
from tmdb import tmdb_api
from time import ctime
from database import db_connection

moment = ctime()
db_cursor = db_connection.cursor
movie_cast_lst = []
movies_export_json = "../tmdb_daily_export_20200918/movie_ids_09_18_2020.json"
with open(movies_export_json, 'r', encoding="UTF-8") as f:
    tmdb_ids = [row.split(",")[1].split(":")[1] for row in f]
    #for id in tmdb_ids[228378:len(tmdb_ids)]:
    for id in tmdb_ids:
        tmdb_id = str(id)
        response = requests.get("https://api.themoviedb.org/3/movie/" + tmdb_id + "/credits?api_key=" + tmdb_api.api_key)
        if response.status_code != 200:
            error_log = "[" + moment + "] Skipping TMDB ID " + tmdb_id + ". Invalid ID. Error code:" + str(response.status_code)
            print(error_log)
            continue
        response_json = response.json()
        movie_id = response_json["id"]
        cast = response_json["cast"]
        for item in cast:
            cast_id = item["cast_id"]
            credit_id = item["credit_id"]
            character = item["character"][:1000]
            order = item["order"]
            cast_dict = dict(movie_id=movie_id,cast_id=cast_id,credit_id=credit_id,character=character,order=order)
            movie_cast_lst.append(cast_dict)
            sql = "INSERT INTO `movie_credits_cast` (`MOVIE_ID`,`CAST_ID`,`CREDIT_ID`,`CHARACTER`,`ORDER`) " \
              "VALUES (%(movie_id)s,%(cast_id)s,%(credit_id)s,%(character)s,%(order)s)"
            db_cursor.executemany(sql, movie_cast_lst)
            db_connection.database_connection.commit()
        ingest_log = "[" + moment + "] Ingested cast for TMDB ID " + tmdb_id
        print(ingest_log)
