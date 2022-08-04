from datetime import datetime
class Event:

    def __init__(self, _id: str = None, start: datetime = None, duration: int = None, description: str = None):
        self._id = str(_id)
        self.start = start
        self.duration = duration
        self.description = description

    def to_dict(self):
        return {
            "id": self._id,
            "start": self.start.strftime("%Y-%m-%d %H:%M:%H"),
            "duration": self.duration,
            "description": self.description,
        }
