from datetime import date
import math


class Task:
    def __init__(self, name: str, hour: int):
        self.name = name
        self.hour = hour

    def hour_per_day(self):
        if isinstance(self, StudyTask):
            return math.ceil(self.hour_left / (self.days_left() + 1))
        else:
            return self.hour


class StudyTask(Task):
    def __init__(self, name: str, hour: int, deadline: str):
        super().__init__(name, hour)
        self.hour_left = hour
        self.deadline = self._parse_date(deadline)

    def _parse_date(self, date_str: str) -> date:
        try:
            return date.fromisoformat(date_str)
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD format.")

    def days_left(self):
        return (self.deadline - date.today()).days


class RegularTask(Task):
    def __init__(self, name: str, hour: int):
        super().__init__(name, hour)

