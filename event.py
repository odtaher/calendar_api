from datetime import datetime

class Event:

    FMT_DATE = "%Y-%m-%d"
    FMT_MONTH = "%Y-%m"
    FMT_FULL = "%Y-%m-%d %H:%M:%S"
    FMT_TIME = "%H:%M"

    def __init__(self, start: datetime = None, duration: int = None, description: str = None):
        if type(start).__name__ == "str":
            start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        self.start = start
        self.duration = int(duration)
        self.description = description
        self.errors = list()
        self.event_id = None

    @staticmethod
    def from_db_row(row: dict):
        event = Event(start=row['start'], duration=row['duration'], description=row['description'])
        event.event_id = row['_id']

        return event


    def to_dict(self) -> dict:
        ret = {
            "start": self.start.strftime(Event.FMT_FULL),
            "month": self.start.strftime(Event.FMT_MONTH),
            "week": self.start.isocalendar().week,
            "date": self.start.strftime(Event.FMT_DATE),
            "time": self.start.strftime(Event.FMT_TIME),
            "duration": self.duration,
            "description": self.description,
        }
        if self.event_id:
            ret['_id'] = str(self.event_id)

        return ret

    def validate(self) -> bool:
        valid = True
        if self.start is None:
            self.errors.append("start_date has to be set")
            valid = False
        if self.duration is None or self.duration <= 0:
            self.errors.append("duration has to be set to a positive number (minutes)")
            valid = False
        if not self.description or not len(self.description):
            self.errors.append("description has to be set")
            valid = False

        return valid

    def time_int(self) -> int:
        return int(self.to_dict().time.replace(":", ""))

    def is_overlapping(self, day_events: list) -> bool:
        # find an event later than this event's time
        # and check if its overlapping
        for event in day_events:
            if str(event['_id']) == self.event_id:
                continue
            event['start'] = datetime.strptime(event['start'], Event.FMT_FULL)
            if event['start'] == self.start:
                return True
            if self.start.timestamp() + self.duration*60 > event['start'].timestamp() and event['start'] > self.start:
                return True
            if event['start'].timestamp() + self.duration*60 > self.start.timestamp() and event['start'] < self.start:
                return True


        return False


