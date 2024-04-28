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
        while True:
            try:
                deadline_date = date.fromisoformat(date_str)
                if deadline_date <= date.today():
                    raise ValueError("Deadline must be after today.")
                return deadline_date
            except ValueError:
                date_str = input("Invalid date. Please enter a date after today (YYYY-MM-DD): ")

    def days_left(self):
        return (self.deadline - date.today()).days


class RegularTask(Task):
    def __init__(self, name: str, hour: int):
        super().__init__(name, hour)

