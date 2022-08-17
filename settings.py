API_ENDPOINT="http://127.0.0.1:8081/"

MONGO_HOST = "mongodb"
# MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017
MONGO_USER = "root"
MONGO_PASSWORD = "root"
MONGO_DB = "calendardb"

DEBUG_MODE = True

MONGO_URI = "mongodb://{user}:{password}@{host}:{port}".format(
    host=MONGO_HOST,
    port=MONGO_PORT,
    user=MONGO_USER,
    password=MONGO_PASSWORD,
)
