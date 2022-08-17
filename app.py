import datetime

from flask import Flask, request, Response
import settings
from event import Event

app = Flask(__name__)


@app.after_request
def cors_allow_all(response: Response):
    if settings.DEBUG_MODE:
        response.headers.add('Access-Control-Allow-Methods', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/events", methods=["GET"])
def events():
    filters = request.args.to_dict()
    if not filters.get("start_date") or not filters.get("end_date"):
        return _error_response("start_date and end_date must be provided")

    start = datetime.datetime.strptime(filters.get("start_date"), Event.FMT_DATE)
    end = datetime.datetime.strptime(filters.get("end_date"), Event.FMT_DATE)

    return {"ok": True, "events": list(map(lambda e: e.to_dict(), Event.find(start, end)))}


@app.route("/event/<event_id>", methods=["GET"])
def event_by_id(event_id: str):
    return {"ok": True, "event": Event.find_by_id(event_id)}


@app.route("/events", methods=["POST"])
def create_event():
    event = Event(**request.form.to_dict())
    if not event.save():
        return _error_response(event.errors)

    return {"ok": True, "event": event.to_dict()}


@app.route("/events/<event_id>", methods=["PUT"])
def update_event(event_id):
    event = Event.find_by_id(event_id)
    if not event:
        return _error_response("Event ID not found")

    event.fill(request.form.to_dict())
    if not event.save():
        return _error_response(event.errors)

    return {"ok": True, "event": event.to_dict()}


@app.route("/events/<event_id>", methods=['DELETE'])
def delete_event(event_id):
    event = Event.find_by_id(event_id)
    if not event:
        return _error_response("Event ID not found")

    if not event.delete():
        return _error_response("An error occurred while deleting the event...")

    return {"ok": True}


def _error_response(message):
    # todo: log messages

    return {"ok": False, "error": message}
