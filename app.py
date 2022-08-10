import datetime

from flask import Flask, request, Response
from bson.objectid import ObjectId
from pymongo import MongoClient
import settings
from event import Event

app = Flask(__name__)

events_db = MongoClient(settings.MONGO_URI)[settings.MONGO_DB]

@app.after_request
def cors_allow_all(response: Response):
    if settings.DEBUG_MODE:
        response.headers.add('Access-Control-Allow-Methods', '*')
        response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/events", methods=["GET"])
def events():
    if "month" in request.args.to_dict():
        query = {
            "month": request.args.get("month")
        }
    elif "week" in request.args.to_dict():
        query = {
            "month": request.args.get("month")
        }
    else:
        return _error_response("either month (Y-m) or week (week number) must be provided")

    results = events_db.events.find(query)
    event_objects = [Event.from_db_row(ev).to_dict() for ev in results]
    return {"ok": True, "events": event_objects}


@app.route("/event/<event_id>", methods=["GET"])
def event_by_id(event_id: str):
    event_row = events_db.events.find_one({"_id": ObjectId(event_id)})
    return {"ok": True, "event": Event(**event_row).to_dict()}


@app.route("/events", methods=["POST"])
def create_event():
    global events_db

    event = Event(**request.form.to_dict())
    if not event.validate():
        return _error_response(",".join(event.errors))

    day_events = events_db.events.find({
        "date": event.start.strftime("%Y-%m-%d")
    })

    if event.is_overlapping(day_events=day_events):
        return _error_response("Event is overlapping")

    new_id = events_db.events.insert_one(event.to_dict())
    if not new_id.acknowledged:
        return _error_response("Cannot save event, please try again ...")

    return {"ok": True, "event": str(new_id.inserted_id)}

@app.route("/events/<event_id>", methods=["PUT"])
def update_event(event_id):
    post_data = request.form.to_dict()
    event_row = events_db.events.find_one({"_id": ObjectId(event_id)})
    if not event_row:
        return _error_response("Event ID not found")
    newEvent = Event(start=post_data['start'], duration=event_row['duration'], description=event_row['description'])
    newEvent.event_id = str(event_row['_id'])
    day_events = events_db.events.find({
        "date": newEvent.start.strftime("%Y-%m-%d")
    })

    if newEvent.is_overlapping(day_events):
        return _error_response("Event is overlapping")

    newEventData = newEvent.to_dict()
    del newEventData['_id']
    events_db.events.update_one({"_id": ObjectId(event_id)}, {"$set": newEventData})

    return {"ok": True}


@app.route("/events/<event_id>", methods=['DELETE'])
def delete_event(event_id):
    event_row = events_db.events.find_one({"_id": ObjectId(event_id)})
    if not event_row:
        return _error_response("Event ID not found")

    events_db.events.delete_one({"_id": ObjectId(event_id)})

    return {"ok": True}


def _error_response(message):
    return {"ok": False, "error": message}

