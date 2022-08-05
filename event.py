from datetime import datetime
class Event:

    def __init__(self, _id: str = None, start: datetime = None, duration: int = None, description: str = None):
        self._id = str(_id)
        self.start = start
        self.duration = duration
        self.description = description
        self.errors = list()

    def to_dict(self):
        return {
            "id": self._id,
            "start": self.start.strftime("%Y-%m-%d %H:%M:%H"),
            "duration": self.duration,
            "description": self.description,
        }

    def validate(self):
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
