import requests
from tmdb import tmdb_api
from time import ctime
from database import db_connection

moment = ctime()
db_cursor = db_connection.cursor
prsn_deets_lst = []
prsn_export_json = "C:/projects/TMDb/tmdb_ingest/tmdb_daily_export_20200918/person_ids_09_18_2020.json"
with open(prsn_export_json, 'r', encoding="UTF-8") as f:
    person_ids = [row.split(",")[1].split(":")[1] for row in f]
    for id in person_ids:
        person_id = str(id)
        response = requests.get("https://api.themoviedb.org/3/person/" + person_id + "?api_key=" + tmdb_api.api_key + "&language=en-US")
        if response.status_code != 200:
            error_log = "[" + moment + "] Skipping Person ID " + person_id + ". Invalid ID. Error code:" + str(response.status_code)
            print(error_log)
            continue
        response_json = response.json()
        person_id = response_json["id"]
        full_name = response_json["name"]
        gender = response_json["gender"]
        person_deets = dict(person_id=person_id,full_name=full_name,gender=gender)
        prsn_deets_lst.append(person_deets)
        sql = "INSERT INTO `people_information` (`ID`,`FULL_NAME`,`GENDER`) " \
              "VALUES (%(person_id)s,%(full_name)s,%(gender)s)"
        db_cursor.executemany(sql, prsn_deets_lst)
        db_connection.database_connection.commit()
        ingest_log = "[" + moment + "] Ingested details for Person ID: " + str(person_id)
        print(ingest_log)
