from datetime import date, timedelta
from task import DeadlineTask, RegularTask
from datetime import datetime
from operator import attrgetter


class TaskManagement:
    def __init__(self):
        self.__ongoing_task = {}
        self.__starting = date.today()
        self.__schedule = []
        self.__mode = 1  # 1 means Concentrated, 2 means Alternating
        self.__max_hour_daily = 5
        self.__today = self.__starting
        self.__task_modified = False

    def show_task_board(self):
        if not self.__ongoing_task:
            print("There are currently no tasks.")
        else:
            # Get the task list containing only DeadlineTask
            deadline_tasks = [task for task in self.__ongoing_task.values() if isinstance(task, DeadlineTask)]

            # Sort DeadlineTasks by deadline
            sorted_deadline_tasks = sorted(deadline_tasks, key=attrgetter('deadline'))

            print("Task Statistics:")
            for task in sorted_deadline_tasks:
                deadline_str = f"Deadline: Day {task.deadline}"
                if task.hour > 0:
                    completion_percentage = (task.hour - task.hour_left) / task.hour * 100
                else:
                    completion_percentage = 100  # Prevent division by zero

                print(f"{task.name} - {deadline_str}, "
                      f"Completion: {completion_percentage:.2f}%. "
                      f"{task.hour_left} hours remaining")

            # Print statistics information of RegularTask
            for task_name, task in self.__ongoing_task.items():
                if not isinstance(task, DeadlineTask):
                    print(f"{task_name} with minimum daily {task.hour} hours has no specific deadline.")

    def __next_day(self):
        """Start the next day"""
        self.__today += timedelta(days=1)

    def get_today(self):
        """Get today's date"""
        return self.__today

    def add_task(self):
        valid_task_types = ['deadline', 'regular', '-1']
        print("There are two task types: one is task with a deadline, "
              "the other is regular task without specific deadline.")
        task_type = input("Enter task type (deadline/regular/-1 to exit): ").lower()

        while task_type not in valid_task_types:
            print("Invalid task type. Please enter 'deadline' or 'regular' or '-1'.")
            task_type = input("Enter task type (deadline/regular): ").lower()
        if task_type == '-1':
            return
        name = input("Enter task name: ")

        if task_type == "deadline":
            if name in self.__ongoing_task:
                existing_task = self.__ongoing_task[name]
                print(f"Task '{name}' already exists with {existing_task.hour_left} hours remaining.")
                additional_hours = self.__get_valid_hours("Enter additional hours to add (enter 0 to keep as is): ",
                                                          minimum=0)
                if additional_hours > 0:
                    existing_task.hour_left += additional_hours
                    existing_task.hour += additional_hours
                    self.__task_modified = True
                print(f"Updated hours for task '{name}': {existing_task.hour_left} hours remaining.")
                if existing_task.get_hour_per_day_schedule(self.__today) > self.__max_hour_daily:
                    print(f"It's hard to complete the task working at most {self.__max_hour_daily} hours per day. "
                          f"Consider increase maximum daily working hours on the main interface.")
            else:
                hours = self.__get_valid_hours("Enter total hours needed: ")
                deadline = self.__get_valid_date("Enter deadline (YYYY-MM-DD): ")
                task = DeadlineTask(name, hours, deadline)
                self.__ongoing_task[task.name] = task
                self.__task_modified = True
                if task.get_hour_per_day_schedule(self.__today) > self.__max_hour_daily:
                    print(f"It's hard to complete the task working at most {self.__max_hour_daily} hours per day. "
                          f"Please consider increasing maximum daily working hours on the main interface.")
        else:
            if name in self.__ongoing_task:
                existing_task = self.__ongoing_task[name]
                print(f"Task '{name}' already exists with the daily minimum {existing_task.hour} hours remaining.")
                additional_hours = self.__get_valid_hours("Enter additional hours to add (enter 0 to keep as is): ",
                                                          minimum=0)
                if additional_hours > 0:
                    existing_task.hour += additional_hours
                    self.__task_modified = True
                print(f"Updated hours for task '{name}': minimum {existing_task.hour} hours every day.")
            else:
                hours = self.__get_valid_hours("Enter daily minimum hours: ", minimum=1)
                task = RegularTask(name, hours)
                self.__ongoing_task[task.name] = task
                self.__task_modified = True
            if sum([x.hour for x in self.__ongoing_task.values() if
                    isinstance(x, RegularTask)]) > self.__max_hour_daily:
                print(f"It's hard to complete existing regular tasks at most {self.__max_hour_daily} hours per day. "
                      f"Please consider increasing maximum daily working hours on the main interface.")

        print(f"Task '{name}' added successfully.")

    def delete_task(self):
        """Delete a task from taskboard"""
        task_name = input("Enter the name of the task to delete (-1 to exit): ")
        if task_name == '-1':
            return
        elif task_name in self.__ongoing_task:
            del self.__ongoing_task[task_name]
            self.__task_modified = True
            print(f"Task '{task_name}' has been deleted from the taskboard.")
        else:
            print(f"Task '{task_name}' is not in the taskboard.")

    def show_today_schedule(self):
        # Reschedule if needed
        if not self.__schedule or self.__task_modified:
            self._generate_schedule()
        print(f"Today is {self.__today}")
        today_index = (self.__today - self.__starting).days
        if today_index < 0 or today_index >= len(self.__schedule):
            print("Today's schedule is not available.")
            return
        today_schedule = self.__schedule[today_index] if today_index < len(self.__schedule) else []
        print("Today's schedule:")
        for task in today_schedule:
            print(f"Task: {task[0]}, Hours: {task[1]}")

    def today_feedback(self):
        """"""
        # Display today's schedule at first
        # Avoid users directly report feedback without display schedule, resulting in not generating/updating schedule
        self.show_today_schedule()
        today_index = (self.__today - self.__starting).days
        if today_index < 0 or today_index >= len(self.__schedule):
            print("Today's schedule is not available.")
            return

        today_schedule = self.__schedule[today_index]
        for task_tuple in today_schedule:
            task_name, hours = task_tuple
            task = self.__ongoing_task[task_name]
            completed = input(f"Did you do '{task_name}' today? (yes/no): ").lower()
            while True:
                if completed == 'yes':
                    today_hour = self.__get_valid_hours(f"You are scheduled to do {task_name} for {hours} hours today. "
                                                        f"How many hours did you actually spend on it? ")
                    # deadline
                    if isinstance(task, DeadlineTask):
                        task.hour_left -= today_hour
                        # Response to the feedback
                        if task.hour_left <= 0:  # If task is finished
                            print(f"Awesome! You have finished {task_name}. It will be removed from the taskboard.")
                            del self.__ongoing_task[task_name]
                        else:  # If task is not finished
                            if task.deadline != self.__today:  # If deadline is not today
                                if today_hour < hours:
                                    print(f"It's okay. {task_name} will be rescheduled in the upcoming days.")
                                    self.__task_modified = True
                                elif today_hour == hours:
                                    print(f"Great! You have completed your plan to do {task_name} for {hours} hours today.")
                                    pass
                                else:
                                    print(f"Excellent! You exceeded your plan to do {task_name} today. "
                                          f"You actually did {task_name} for {hours} hours.")
                                    self.__task_modified = True
                            else:  # If deadline is today
                                print(f"Unfortunately, the deadline of {task_name} is today, but you didn't complete it.")
                                while True:
                                    due_choice = input("Do you want to delay the deadline or delete the task?\n"
                                                       "Enter a later date to postpone or enter -1 to delete the task: ")
                                    if due_choice == '-1':
                                        del self.__ongoing_task[task_name]
                                        print(f"Task '{task_name}' has been deleted from the taskboard.")
                                        break
                                    else:
                                        try:
                                            new_ddl = datetime.strptime(due_choice, "%Y-%m-%d").date()
                                            if new_ddl > self.__today:
                                                self.__ongoing_task[task_name].deadline = new_ddl
                                                print(f"Task '{task_name}' deadline has been postponed to {new_ddl}.")
                                                self.__task_modified = True
                                                break
                                            else:
                                                print("Invalid date. Please enter a valid date in the format YYYY-MM-DD "
                                                      "that is later than today.")
                                        except ValueError:
                                            print("Invalid date. Please enter a valid date in the format YYYY-MM-DD "
                                                  "that is later than today.")
                        break
                    # regular
                    else:
                        if today_hour >= hours:
                            print(f"Great! You completed {task_name} planned for today")
                        else:
                            print(f"Don't be upset! Try to finish {task_name} next time.")
                        break
                elif completed == 'no':
                    if isinstance(task, DeadlineTask):
                        self.__task_modified = True
                        if task.deadline == self.__today:
                            print(f"Unfortunately, the deadline of {task_name} is today, but you didn't complete it.")
                            while True:
                                due_choice = input("Do you want to delay the deadline or delete the task?\n"
                                                   "Enter a later date to postpone or enter -1 to delete the task: ")
                                if due_choice == '-1':
                                    del self.__ongoing_task[task_name]
                                    print(f"Task '{task_name}' has been deleted from the taskboard.")
                                    break
                                else:
                                    try:
                                        new_ddl = datetime.strptime(due_choice, "%Y-%m-%d").date()
                                        if new_ddl > self.__today:
                                            self.__ongoing_task[task_name].deadline = new_ddl
                                            print(f"Task '{task_name}' deadline has been postponed to {new_ddl}.")
                                            break
                                        else:
                                            print("Invalid date. Please enter a valid date in the format YYYY-MM-DD "
                                                  "that is later than today.")
                                    except ValueError:
                                        print("Invalid date. Please enter a valid date in the format YYYY-MM-DD "
                                              "that is later than today.")
                            break
                    print(f"It's okay. {task_name} will be rescheduled in the upcoming days.")
                    print("If you don't need this task, you can delete it on the main interface.")
                    break
                else:
                    completed = input(f"Did you do '{task_name}' today? (yes/no): ").lower()
        self.__next_day()

    def show_week_schedule(self):
        """Display the schedule for the next 7 days"""
        # Reschedule if needed
        if not self.__schedule or self.__task_modified:
            self._generate_schedule()
        print("Schedule for the next 7 days:")
        for i in range(7):  # Display the schedule for the next 7 days
            day = self.__today + timedelta(days=i)
            day_index = (day - self.__starting).days
            if day_index < len(self.__schedule):
                daily_schedule = self.__schedule[day_index]
                if daily_schedule:  # Check if no schedule for that day
                    print(f"Day {day}: {daily_schedule}")
                else:
                    print(f"Day {day}: No tasks scheduled.")
            else:
                print(f"Day {day}: No tasks scheduled.")

    def set_mode(self):
        mode_name = 'Concentrated' if self.__mode == 1 else 'Alternating'
        print(f"Current mode is {mode_name}.")
        print("In CONCENTRATED mode, users focus on completing one task at a time in accordance with their deadlines.")
        print("In ALTERNATING mode, users switch between multiple tasks on a day while still meeting their deadlines.")
        while True:
            mode_input = input("Enter mode (1 for Concentrated, 2 for Alternating, -1 to keep as it is and continue): ")
            if mode_input == '-1':
                return
            elif mode_input.isdigit() and mode_input in ['1', '2']:
                self.__mode = int(mode_input)
                mode_name = 'Concentrated' if self.__mode == 1 else 'Alternating'
                print(f"Mode set to {mode_name}.\n")
                self.__task_modified = True
                break
            else:
                print("Invalid input. Please enter '1' for Concentrated or '2' for Round Robin or -1 to exit.")

    def set_max_daily_hours(self):
        print(f"Current maximum daily working hours is {self.__max_hour_daily}.")
        print("Note:\nWhen tasks with deadlines are urgent and time-consuming, "
              "the total duration of tasks scheduled on one day may exceed the maximum daily working hours, "
              "and regular tasks may be ignored."
              "Please prepare accordingly.")
        while True:
            max_hour_daily = self.__get_valid_hours("Enter maximum daily working hours (1-24) "
                                                    "(-1 to keep as it is and continue): ", minimum=-1)
            if max_hour_daily == -1:
                return
            elif 1 <= max_hour_daily <= 24:
                self.__max_hour_daily = max_hour_daily
                print(f"Daily maximum working hours set to {self.__max_hour_daily}.\n")
                self.__task_modified = True
                break
            else:
                print("Invalid input. Please enter a number between 1 and 24 or -1.")



    def __get_valid_hours(self, prompt, minimum=1):
        # Get and validate hours input
        while True:
            try:
                hours = int(input(prompt))
                if hours >= minimum:
                    return hours
                else:
                    print(f"Hours must be at least {minimum}. Please enter a valid number of hours.")
            except ValueError:
                print("Invalid input. Please enter a valid integer for hours.")

    def __get_valid_date(self, prompt):
        """Get and validate date input"""
        while True:
            date_str = input(prompt)
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                print("Invalid date format. Please enter a date in YYYY-MM-DD format.")

    def _generate_schedule(self):
        """Generate/regenerate schedule - called when displaying schedule"""
        if len(self.__ongoing_task) != 0:
            if self.__mode == 1:
                self.ddl_sorting()
            elif self.__mode == 2:
                self._alternating_sorting()
        self.__task_modified = False

    def ddl_sorting(self):
        """Schedule tasks by deadline"""
        # Divide tasks
        deadline_tasks = []
        regular_tasks = []
        max_deadline = self.__today
        for task in self.__ongoing_task.values():
            if isinstance(task, DeadlineTask):
                deadline_tasks.append(task)
                if task.deadline > max_deadline:
                    max_deadline = task.deadline
            else:
                regular_tasks.append(task)

        # Sort deadline tasks by deadline
        sorted_deadline_tasks = sorted(deadline_tasks, key=lambda x: x.deadline)
        max_index = (max_deadline - self.__starting).days  # max deadline index
        today_index = (self.__today - self.__starting).days  # today index
        current_day_index = today_index  # current day index
        lastday_index = current_day_index  # last day index

        if len(self.__schedule) < current_day_index:
            for _ in range(len(self.__schedule), current_day_index):
                self.__schedule.append(set())
        for i in range(current_day_index, max(max_index + 1, current_day_index + 7)):
            if len(self.__schedule) > i:
                self.__schedule[i] = set()
            elif len(self.__schedule) == i:
                self.__schedule.append(set())

        hour_assigned = 0
        for task in sorted_deadline_tasks:
            remaining_hours = task.hour_left
            task_deadline_index = (task.deadline - self.__starting).days
            # sum(hours for _, hours in self.__schedule[current_day_index])
            # Assign tasks based on remaining hours per day
            while True:
                if current_day_index == task_deadline_index:  # On the deadline day
                    # No max daily hour limit on the deadline day
                    available_hours = 24 - hour_assigned
                else:  # Before the deadline day
                    # Add the regular tasks at first
                    if hour_assigned == 0:
                        for r in regular_tasks:
                            self.__schedule[current_day_index].add((r.name, r.hour))
                            hour_assigned += r.hour
                    available_hours = max(self.__max_hour_daily - hour_assigned, 0)

                if available_hours > 0:
                    hours_today = min(remaining_hours, available_hours)
                    self.__schedule[current_day_index].add((task.name, hours_today))  # Add to set
                    remaining_hours -= hours_today
                    hour_assigned += hours_today
                    if hour_assigned >= self.__max_hour_daily:
                        current_day_index += 1
                        hour_assigned = 0
                    else:
                        if current_day_index == task_deadline_index:
                            for r in regular_tasks:
                                if hour_assigned >= self.__max_hour_daily:
                                    current_day_index += 1
                                    hour_assigned = 0
                                    break
                                else:
                                    self.__schedule[current_day_index].add((r.name, r.hour))
                                    hour_assigned += r.hour
                else:
                    current_day_index += 1
                    hour_assigned = 0

                if remaining_hours <= 0 or current_day_index > task_deadline_index:
                    break  # Exit loop if task hours are fully allocated or past deadline
            lastday_index = current_day_index

        if lastday_index - today_index < 7:
            for i in range(lastday_index, today_index + 7):
                for r in regular_tasks:
                    self.__schedule[i].add((r.name, r.hour))

    def _alternating_sorting(self):
        """Schedule tasks alternatively"""
        # Store current scheduling date
        schedule_date = self.__today
        index = (schedule_date - self.__starting).days
        # Sort all tasks: descending by average hour per day, if same, ascending by deadline, regular tasks at last
        sorted_tasks = list(sorted(self.__ongoing_task.values(),
                                   key=lambda x: (-x.get_hour_per_day_schedule(schedule_date),
                                                  x.deadline if isinstance(x, DeadlineTask) else date.max)))
        # Exit the loop if no deadline tasks in the pool
        # Exception: no deadline tasks but schedule range less than 7 days - schedule regular tasks for the left days
        while any(isinstance(task, DeadlineTask) for task in sorted_tasks) or (schedule_date - self.__today).days < 7:
            if len(self.__schedule) < index:
                # There is a gap in the schedule - shouldn't happen
                for i in range(len(self.__schedule), index):
                    self.__schedule.append(set())
            # Schedule tasks for the current scheduling day
            daily_plan = set()
            daily_hour = 0
            # Loop through the task pool
            for task in sorted_tasks:
                # Stop scheduling for the current day if total hours exceed max hours
                # Will still go through the rest tasks in the pool to check if there is a task with ddl on current day
                if self.__max_hour_daily <= daily_hour:
                    # If ddl is current day, must be scheduled
                    if isinstance(task, RegularTask) or task.deadline != schedule_date:
                        continue
                hour_task = task.get_hour_per_day_schedule(schedule_date)
                # Add task to the current day
                if isinstance(task, DeadlineTask):
                    if task.deadline == schedule_date:
                        hour_task = task.hour_left - task.hour_scheduled
                    else:
                        hour_task = min(hour_task, task.hour_left - task.hour_scheduled,
                                        self.__max_hour_daily - daily_hour)
                else:
                    hour_task = min(hour_task, self.__max_hour_daily - daily_hour)
                daily_plan.add((task.name, hour_task))
                daily_hour += hour_task
                # Update the schedule for that task
                if isinstance(task, DeadlineTask):
                    task.hour_scheduled += hour_task
            # If total hours exceed max hours, check if there are tasks to postpone
            if daily_hour > self.__max_hour_daily:
                modify_tasks = set()
                for task_name, hour in daily_plan:
                    # Check for regular tasks
                    if isinstance(self.__ongoing_task.get(task_name), RegularTask):
                        while hour != 0 and daily_hour > self.__max_hour_daily:
                            hour -= 1
                            daily_hour -= 1
                        modify_tasks.add((task_name, hour))
                    if daily_hour <= self.__max_hour_daily:
                        break
            # Add schedule for current day to the schedule list
            if len(self.__schedule) == index:
                # Previous schedule ends on the last day
                # Or initial state: empty schedule
                self.__schedule.append(daily_plan)
            elif len(self.__schedule) > index:
                # Previous schedule covers the current day, needs to modify not append
                self.__schedule[index] = daily_plan

            # Update current scheduling date and its index
            # Prepare to schedule for the next day
            schedule_date += timedelta(days=1)
            index += 1
            # Clear deadline tasks that have finished scheduling from the pool
            sorted_tasks = list(filter(lambda x: isinstance(x, RegularTask) or x.hour_scheduled < x.hour_left,
                                       sorted_tasks))
            # Reorder
            sorted_tasks.sort(key=lambda x: (-x.get_hour_per_day_schedule(schedule_date),
                                             x.deadline if isinstance(x, DeadlineTask) else date.max))
        # Before finishing scheduling, clear scheduled hour records in object Tasks
        for task in self.__ongoing_task.values():
            if isinstance(task, DeadlineTask):
                task.hour_scheduled = 0
