import datetime
from datetime import date
import math


class Task:
    def __init__(self, name: str, hour: int):
        self.name = name
        self.hour = hour


class DeadlineTask(Task):
    def __init__(self, name: str, hour: int, deadline: str):
        super().__init__(name, hour)
        self.hour_left = self.hour
        self.deadline = self._parse_date(deadline)
        self.hour_scheduled = 0

    def _parse_date(self, date_str: str) -> date:
        while True:
            try:
                deadline_date = date.fromisoformat(date_str)
                if deadline_date <= date.today():
                    raise ValueError("Deadline must be after today.")
                return deadline_date
            except ValueError:
                date_str = input("Invalid date. Please enter a date after today (YYYY-MM-DD): ")

    def get_hour_per_day_schedule(self, date_schedule):
        return math.ceil((self.hour_left - self.hour_scheduled) / ((self.deadline - date_schedule).days + 1))


class RegularTask(Task):
    def __init__(self, name: str, hour: int):
        super().__init__(name, hour)
        self.hour_left = self.hour



    def get_hour_per_day_schedule(self, date_schedule):
        return self.hour

