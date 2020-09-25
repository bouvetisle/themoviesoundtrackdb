import requests
from tmdb import tmdb_api
from database import db_connection

db_cursor = db_connection.cursor
response = requests.get("https://api.themoviedb.org/3/genre/movie/list" + "?api_key=" + tmdb_api.api_key + "&language=en-US")
response_json = response.json()["genres"]
for i in range(len(response_json)):
    genre_id = response_json[i]["id"]
    genre_name = response_json[i]["name"]
    genre_dict = dict(genre_id=genre_id,genre_name=genre_name)
    genre_list = []
    genre_list.append(genre_dict)
    for i in range(len(genre_list)):
        genre_dict = genre_list[i]
        sql = "INSERT INTO `tmdb_genre` (`GENRE_ID`,`GENRE_NAME`) VALUES (%(genre_id)s,%(genre_name)s)"
        db_cursor.execute(sql,genre_dict)
        print("Ingested Genre: " + genre_name)
db_connection.database_connection.commit()

