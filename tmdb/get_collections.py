import requests
from tmdb import tmdb_api
from database import db_connection
from time import ctime

moment = ctime()
db_cursor = db_connection.cursor

movies_export_json = "../tmdb_daily_export_20200918/collection_ids_09_18_2020.json"
with open(movies_export_json, 'r', encoding="UTF-8") as f:
    coll_ids = [row.split(",")[0].split(":")[1] for row in f]
    for coll_id in coll_ids:
        coll_id = coll_id
        response = requests.get("https://api.themoviedb.org/3/collection/" + coll_id + "?api_key=" + tmdb_api.api_key + "&language=en-US")
        if response.status_code != 200:
            error_log = "[" + moment + "] Skipping Collection ID " + coll_id + ". Invalid ID. Error code:" + str(response.status_code)
            print(error_log)
            continue
        response_json = response.json()
        collection_id = response_json["id"]
        collection_name = response_json["name"]
        for i in range(len(response_json["parts"])):
            part_id = response_json["parts"][i]["id"]
            coll_dict = dict(collection_id=collection_id,collection_name=collection_name,id=part_id)
            coll_list = []
            coll_list.append(coll_dict)
            sql = "INSERT INTO `collections` (`COLLECTION_ID`,`COLLECTION_NAME`,`ID`) " \
                "VALUES (%(collection_id)s,%(collection_name)s,%(id)s)"
            db_cursor.executemany(sql,coll_list)
            ingest_log = "[" + moment + "] Ingested Collection ID " + coll_id + ": " + collection_name
            print(ingest_log)
            db_connection.database_connection.commit()
