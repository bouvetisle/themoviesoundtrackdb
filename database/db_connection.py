import pymysql

# Connected to localhost for testing
host = "localhost"
username = "root"
password = "root"
database = "tmdb"

# Open database connection - cursor outputs in dictionary
database_connection = pymysql.connect(
    host,
    username,
    password,
    database,
    cursorclass=pymysql.cursors.DictCursor)
cursor = database_connection.cursor()