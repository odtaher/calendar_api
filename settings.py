MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_USER = "root"
MONGO_PASSWORD = "root"
MONGO_DB = "calendardb"

MONGO_URI = "mongodb://{user}:{password}@{host}:{port}".format(
    host=MONGO_HOST,
    port=MONGO_PORT,
    user=MONGO_USER,
    password=MONGO_PASSWORD,
)
