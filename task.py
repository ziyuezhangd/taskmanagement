from datetime import date
class Task:
    def __init__(self, name: str, hour: int):
        self.name = name
        self.hour = hour

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

class RegularTask(Task):
    def __init__(self, name: str, hour: int):
        super().__init__(name, hour)

