import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from database import db_connection

db_cursor = db_connection.cursor
from spotify import spotify_api
spotify_track_analysis_lst = []

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotify_api.client_id,
                                                           client_secret=spotify_api.client_secret))

#album_search_result = sp.search("Kill Bill Soundtrack")
#album_id = album_search_result["tracks"]["items"][0]["album"]["id"]
album_id='3TREjkFTTmuQu1H08IhyRn'
album_tracks = sp.album_tracks(album_id)["items"]
album_deets = sp.album(album_id)
album_title = album_deets["name"]

for track in album_tracks:
    album_track_id = track["id"] #id
    album_track_name = track["name"] #title
    album_track_artist = track["artists"][0]["name"] #artist
    album_track_audio_features = sp.audio_features(album_track_id)
    track_href = album_track_audio_features[0]["track_href"]
    analysis_url = album_track_audio_features[0]["analysis_url"]
    duration_ms = album_track_audio_features[0]["duration_ms"]
    time_signature = album_track_audio_features[0]["time_signature"]
    tempo = album_track_audio_features[0]["tempo"]
    valence = album_track_audio_features[0]["valence"]
    instrumentalness = album_track_audio_features[0]["instrumentalness"]
    acousticness = album_track_audio_features[0]["acousticness"]
    speechiness = album_track_audio_features[0]["speechiness"]
    mode = album_track_audio_features[0]["mode"]
    loudness = album_track_audio_features[0]["loudness"]
    key = album_track_audio_features[0]["key"]
    energy = album_track_audio_features[0]["energy"]
    danceability = album_track_audio_features[0]["danceability"]
    spotify_track_analysis = dict(id=album_track_id,
                                  title=album_track_name,
                                  artist=album_track_artist,
                                  track_href=track_href,
                                  analysis_url=analysis_url,
                                  duration_ms=duration_ms,
                                  time_signature=time_signature,
                                  tempo=tempo,
                                  valence=valence,
                                  instrumentalness=instrumentalness,
                                  acousticness=acousticness,
                                  speechiness=speechiness,
                                  mode=mode,
                                  loudness=loudness,
                                  key=key,
                                  energy=energy,
                                  danceability=danceability)
    print(spotify_track_analysis)
    spotify_track_analysis_lst.append(spotify_track_analysis)
print(spotify_track_analysis_lst)
spotify_track_analysis_sql = "INSERT INTO `spotify_track_analysis` (`ID`,`TRACK_HREF`,`ANALYSIS_URL`,`DURATION_MS`,`TIME_SIGNATURE`,`TEMPO`,`VALENCE`," \
                             "`INSTRUMENTALNESS`,`ACOUSTICNESS`,`SPEECHINESS`,`MODE`,`LOUDNESS`,`KEY`,`ENERGY`,`DANCEABILITY`) " \
                            "VALUES (%(id)s,%(track_href)s,%(analysis_url)s,%(duration_ms)s,%(time_signature)s,%(tempo)s,%(valence)s," \
                             "%(instrumentalness)s,%(acousticness)s,%(speechiness)s,%(mode)s,%(loudness)s,%(key)s,%(energy)s,%(danceability)s)"
db_cursor.executemany(spotify_track_analysis_sql, spotify_track_analysis_lst)
db_cursor.fetchall()
db_connection.database_connection.commit()
spotify_tracks_sql = "INSERT INTO `spotify_tracks` (`ID`,`TITLE`,`ARTIST`) VALUES (%(id)s,%(title)s,%(artist)s)"
db_cursor.executemany(spotify_tracks_sql,spotify_track_analysis_lst)
db_cursor.fetchall()
db_connection.database_connection.commit()
