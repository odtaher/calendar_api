import datetime

from flask import Flask, request
from bson.objectid import ObjectId
from pymongo import MongoClient
import settings
from event import Event

app = Flask(__name__)

print("mongo uri: {}".format(settings.MONGO_URI))

events_db = MongoClient(settings.MONGO_URI)[settings.MONGO_DB]


@app.route("/events", methods=["GET"])
def events():
    if not all(["start_date" in request.args.to_dict(), "end_date" in request.args.to_dict()]):
        return _error_response("start_date and end_date must be provided in YYYY-mm-dd format")

    from_date = datetime.datetime.fromisoformat(request.args.get("start_date"))
    end_date = datetime.datetime.fromisoformat(request.args.get("end_date"))
    results = events_db.events.find({
        "start": {
            "$gte": from_date,
            "$lte": end_date,
        }
    })
    event_objects = [Event(**dict(ev)).to_dict() for ev in results]
    return {"ok": False, "events": event_objects}


@app.route("/event/<event_id>", methods=["GET"])
def event_by_id(event_id: str):
    event_row = events_db.events.find_one({"_id": ObjectId(event_id)})
    return {"ok": True, "event": Event(**event_row).to_dict()}


def _error_response(message):
    return {"ok": False, "error": message}
