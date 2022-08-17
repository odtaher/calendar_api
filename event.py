from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
import settings


class Event:
    FMT_DATE = "%Y-%m-%d"
    FMT_MONTH = "%Y-%m"
    FMT_FULL = "%Y-%m-%d %H:%M:%S"
    FMT_TIME = "%H:%M"

    events_db = MongoClient(settings.MONGO_URI)[settings.MONGO_DB]

    def __init__(self, start: str, end: str, description: str, all_day: bool = False, _id=None):
        self.start = start
        self.end = end
        self.description = description
        self.all_day = all_day
        self.errors = list()
        self._id = _id

        self._reformat()

    def _reformat(self):
        if type(self.all_day).__name__ != "bool":
            self.all_day = self.all_day == "1" or str(self.all_day).lower() == "true"
        if type(self.start).__name__ == "str":
            self.start = datetime.strptime(self.start, Event.FMT_FULL)
        if not self.all_day and type(self.end).__name__ == "str":
            self.end = datetime.strptime(self.end, Event.FMT_FULL)


    def to_dict(self, with_id=True):
        ret = vars(self)
        if 'errors' in ret:
            del ret['errors']
        if '_id' in ret and not with_id:
            del ret['_id']
        if '_id' in ret and not ret['_id']:
            del ret['_id']
        if ret.get('_id'):
            ret['_id'] = str(ret.get('_id'))
        return ret

    def save(self):
        if not self._validate():
            return False
        if self._id:
            result = Event.events_db.events.update_one({"_id": ObjectId(self._id)}, {"$set": self.to_dict(False)})
            return result.modified_count >= 0

        else:
            result = Event.events_db.events.insert_one(self.to_dict(False))
            if not result.inserted_id:
                return False
            self._id = result.inserted_id

        return True

    def fill(self, data: dict):
        for key, val in data.items():
            setattr(self, key, val)

        self._reformat()
        return self

    def delete(self):
        result = Event.events_db.events.delete_one({"_id": ObjectId(self._id)})
        return result.deleted_count > 0

    @staticmethod
    def find_by_id(event_id):
        row = Event.events_db.events.find_one({"_id": ObjectId(event_id)})
        if not row:
            return None
        return Event(**row)

    @staticmethod
    def find(start: datetime, end: datetime):
        results = Event.events_db.events.find({
            "start": {
                "$gte": start,
            },
            "end": {
                "$lte": end
            }
        })

        return map(lambda row: Event(**row), results)

    def _validate(self) -> bool:
        valid = True
        if self.start is None:
            self.errors.append("start date/time has to be set")
            valid = False
        if self.end is None and not self.all_day:
            self.errors.append("end date/time has to be set")
            valid = False
        if not self.description or not len(self.description):
            self.errors.append("description has to be set")
            valid = False

        return valid and not self._is_overlapping([])

    def _is_overlapping(self, day_events: list) -> bool:
        return False
