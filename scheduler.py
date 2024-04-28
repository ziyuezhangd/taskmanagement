from datetime import date, timedelta
from task import Task, StudyTask, RegularTask
from datetime import datetime
from operator import attrgetter
import time



class TaskManagement:
    def __init__(self):
        self.__ongoing_task = {}
        self.__completed_task = {}
        self.__starting = date.today()
        # self.__schedule = []
        self.__schedule = [set() for _ in range(30)]
        self.__mode = 2  # 1 means sorting by deadline, 2 means round-robin style
        self.__max_hour_daily = 4


    def get_ongoing_tasks(self):
        return self.__ongoing_task
    def show_task_board(self):
        if not self.__ongoing_task:
            print("There are currently no tasks.")
        else:
            for task_name, task in self.__ongoing_task.items():
                if isinstance(task, StudyTask):
                    print(f"{task_name}: {task.hour_left} hours remaining")
                else:
                    print(f"{task_name}: minimal {task.hour} hours every day")

    def get_ongoing_task(self):
        return self.__ongoing_task

    def daily_update(self):
        while True:
            self.generate_schedule()
            print("Daily schedule update completed.")
            time.sleep(86400)  # 每24小时更新一次，86400秒等于一天


    def add_task(self):
        valid_task_types = ['study', 'regular', '-1']
        task_type = input("Enter task type (study/regular/-1 to exit): ").lower()

        while task_type not in valid_task_types:
            print("Invalid task type. Please enter 'study' or 'regular' or '-1'.")
            task_type = input("Enter task type (study/regular): ").lower()
        if task_type == '-1':
            return
        name = input("Enter task name: ")

        if task_type == "study":
            if name in self.__ongoing_task:
                existing_task = self.__ongoing_task[name]
                print(f"Task '{name}' already exists with {existing_task.hour_left} hours remaining.")
                additional_hours = self.__get_valid_hours("Enter additional hours to add (enter 0 to keep as is): ",
                                                          minimum=0)
                existing_task.hour_left += additional_hours
                existing_task.hour += additional_hours
                print(f"Updated hours for task '{name}': {existing_task.hour_left} hours remaining.")
            else:
                hours = self.__get_valid_hours("Enter total hours needed: ")
                deadline = self.__get_valid_date("Enter deadline (YYYY-MM-DD): ")
                task = StudyTask(name, hours, deadline)
                self.__ongoing_task[task.name] = task

        else:
            if name in self.__ongoing_task:
                existing_task = self.__ongoing_task[name]
                print(f"Task '{name}' already exists with the daily minimum {existing_task.hour} hours remaining.")
                additional_hours = self.__get_valid_hours("Enter additional hours to add (enter 0 to keep as is): ",
                                                          minimum=0)
                existing_task.hour += additional_hours
                print(f"Updated hours for task '{name}': minimum {existing_task.hour} hours every day.")
            else:
                hours = self.__get_valid_hours("Enter daily minimum hours: ", minimum=1)
                task = RegularTask(name, hours)
                self.__ongoing_task[task.name] = task

        self.generate_schedule()
        print(f"Task '{name}' added successfully.")

        print("Generating schedule...")
        self.generate_schedule()
        print("Schedule generated.")

    def delete_task(self):
        task_name = input("Enter the name of the task to delete (-1 to exit): ")
        if task_name == '-1':
            return
        elif task_name in self.__ongoing_task:
            del self.__ongoing_task[task_name]
            print(f"Task '{task_name}' has been deleted from the taskboard.")
        else:
            print(f"Task '{task_name}' is not in the taskboard.")

    def show_today_schedule(self):
        today = date.today()  # 获取今天的日期
        today_index = (today - self.__starting).days
        if today_index < 0 or today_index >= len(self.__schedule):
            print("Today's schedule is not available.")
            return
        today_schedule = self.__schedule[today_index] if today_index < len(self.__schedule) else []
        print("Today's schedule:")
        for task in today_schedule:
            print(f"Task: {task[0]}, Hours: {task[1]}")

    def today_feedback(self):
        today = date.today()
        today_index = (today - self.__starting).days
        if today_index < 0 or today_index >= len(self.__schedule):
            print("Today's schedule is not available.")
            return

        today_schedule = self.__schedule[today_index]

        for task_tuple in today_schedule:
            task_name, hours = task_tuple
            if isinstance(task_name, StudyTask):
                while True:
                    completed = input(f"Did you do '{task_name}' today? (yes/no): ").lower()
                    if completed == 'yes':
                        # 做了，问做了多久
                        today_hour = self.__get_valid_hours(input(f"You are scheduled to do {task_name} for {hours} hours today. How many hours did you actually do it?"),minimum=1)
                        if today_hour < task_name.hour_left:
                            task_name.hour_left -= today_hour
                            if today_hour >= hours:
                                print("Great job!")
                            print(f"You have did {task_name} for {today_hour} hours today. You still need to do it for {task_name.hour_left} hours in the future.")
                            break
                        else:

                            self.delete_task(task_name)
                            print(f"Awesome! You have finished {task_name}.")
                            break
                    elif completed == 'no':
                        print(f"It's okay. I will reschedule {task_name} for you.")
                        print("You can also choose to delete it on the main interface.")
                        break
                    else:
                        print("Invalid input. Please answer 'yes' or 'no'.")
             # regular task
            else:
                while True:
                    completed = input(f"Did you do '{task_name}' today? (yes/no): ").lower()
                    if completed == 'yes':
                        # 做了，问做了多久
                        today_hour = self.__get_valid_hours(input(
                            f"You are scheduled to do {task_name} for {hours} hours today. How many hours did you actually do it?"),
                                                            minimum=1)
                        if today_hour >= hours:
                            print(f"Great! You completed {task_name} planned for today")
                    elif completed == 'no':
                        print(f"Unfortunately, you did not complete {task_name} planned for today")
                    else:
                        print("Invalid input. Please answer 'yes' or 'no'.")
        self.generate_schedule()
        print("Based on your task completion status, a new scheduler has been generated for you.")


    def show_week_schedule(self):
        print("This week's schedule :")
        for i in range(7):  # 显示接下来7天的日程
            day = self.__starting + timedelta(days=i)
            if i < len(self.__schedule):
                daily_schedule = self.__schedule[i]
                if daily_schedule:  # 检查日程是否为空
                    print(f"Day {day}: {daily_schedule}")
                else:
                    print(f"Day {day}: No tasks scheduled.")
            else:
                print(f"Day {day}: No tasks scheduled.")

    def set_mode(self):
        mode_name = 'DDL sorting' if self.__mode == 1 else 'Round Robin'
        print(f"Current mode is {mode_name}.")
        while True:
            mode_input = input("Enter mode (1 for DDL sorting, 2 for Round Robin, -1 to keep current and exit): ")
            if mode_input == '-1':
                return
            elif mode_input.isdigit() and mode_input in ['1', '2']:
                self.__mode = int(mode_input)
                mode_name = 'DDL sorting' if self.__mode == 1 else 'Round Robin'
                print(f"Mode set to {mode_name}.")
                break
            else:
                print("Invalid input. Please enter '1' for DDL sorting or '2' for Round Robin or -1 to exit.")

    def set_daily_workinghours(self):
        print(f"Current daily working hours is {self.__max_hour_daily}.")
        while True:
            max_hour_daily = self.__get_valid_hours("Enter daily working hours (1-24) (-1 to keep current and exit): ",minimum=-1)
            if max_hour_daily == -1:
                return
            elif 1 <= max_hour_daily <= 24:
                self.__max_hour_daily = max_hour_daily
                print(f"Daily working hours set to {self.__max_hour_daily}.")
                break
            else:
                print("Invalid input. Please enter a number between 1 and 24 or -1.")

    def statistics(self):
        if not self.__ongoing_task:
            print("No tasks available")
            return

        # 获取仅包含 StudyTask 的任务列表
        study_tasks = [task for task in self.__ongoing_task.values() if isinstance(task, StudyTask)]

        # 按照截止日期对 StudyTask 进行排序
        sorted_study_tasks = sorted(study_tasks, key=attrgetter('deadline'))

        print("Task Statistics:")
        for task in sorted_study_tasks:
            deadline_str = f"Deadline: Day {task.deadline}"
            if task.hour > 0:
                completion_percentage = (task.hour - task.hour_left) / task.hour * 100
            else:
                completion_percentage = 100  # 防止除以零

            print(f"{task.name} - {deadline_str}, Completion: {completion_percentage:.2f}%")

        # 输出regular task类型的任务统计信息
        for task_name, task in self.__ongoing_task.items():
            if not isinstance(task, StudyTask):
                print(f"{task_name} with minimum daily {task.hour} hours has no specific deadline.")


    def __get_valid_hours(self, prompt, minimum=1):
        """获取并验证小时数输入"""
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
        """获取并验证日期输入"""
        while True:
            date_str = input(prompt)
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                print("Invalid date format. Please enter a date in YYYY-MM-DD format.")
    def generate_schedule(self):
        if self.__mode == 1:
            self.ddl_sorting()
        elif self.__mode == 2:
            self.rr_sorting()
        # 生成一个每日任务安排的sequence
        # 两种算法/mode：1按ddl排序，2round robin（且需满足ddl）
        # 优先满足StudyTask，剩余时间满足RegularTask
        # 如果ddl紧张，一天可以超过daily_working_hour（但不能超过24）
        pass

    def ddl_sorting(self):
        print("Starting DDL sorting...")
        study_tasks = [(task, task.deadline) for task in self.__ongoing_task.values() if isinstance(task, StudyTask)]
        study_tasks.sort(key=lambda x: x[1])  # Sort by deadline

        #确保日程数组足够大以容纳所有的任务
        max_deadline = max((task.deadline for task, _ in study_tasks), default=self.__starting)
        days_needed = (max_deadline - self.__starting).days + 1
        if len(self.__schedule) < days_needed:
            self.__schedule.extend([set() for _ in range(days_needed - len(self.__schedule))])

        for task, _ in study_tasks:
            current_date = self.__starting
            assigned = False

            while not assigned and task.hour_left > 0:
                day_index = (current_date - self.__starting).days
                if day_index >= len(self.__schedule):
                    self.__schedule.append(set())
                today_hours = sum(hours for _, hours in self.__schedule[day_index])
                remaining_hours = self.__max_hour_daily - today_hours

                if remaining_hours > 0:
                    hours_to_assign = min(task.hour_left, remaining_hours)
                    self.__schedule[day_index].add((task.name, hours_to_assign))
                    task.hour_left -= hours_to_assign

                if remaining_hours == 0 or not assigned:
                    current_date += timedelta(days=1)

        print("DDL sorting completed.")

        # # 分离StudyTask和RegularTask
        # study_tasks = []
        # regular_tasks = []
        # for task in self.__ongoing_task.values():
        #     if isinstance(task, StudyTask):
        #         study_tasks.append(task)
        #     elif isinstance(task, RegularTask):
        #         regular_tasks.append(task)
        #
        # # 按截止日期排序StudyTask
        # study_tasks.sort(key=lambda x: x.deadline)
        #
        # # 安排任务
        # day_index = 0
        # while study_tasks:
        #     today_hours = 0
        #     if day_index >= len(self.__schedule):
        #         break
        #     today_schedule = self.__schedule[day_index]
        #     remaining_hours = self.__max_hour_daily - today_hours
        #
        #     new_tasks = []
        #     for task in study_tasks:
        #         print(f"Assigning task {task.name} with {task.hour_left} hours left.")
        #
        #         if today_hours < self.__max_hour_daily:
        #             hours_to_assign = min(task.hour_left, remaining_hours)
        #             today_schedule.append((task.name, hours_to_assign))
        #             today_hours += hours_to_assign
        #             task.hour_left -= hours_to_assign
        #             if task.hour_left > 0:
        #                 new_tasks.append(task)
        #             remaining_hours = self.__max_hour_daily - today_hours
        #         if today_hours >= self.__max_hour_daily:
        #             break
        #     study_tasks = new_tasks
        #
        #     # 补充RegularTask到每天的剩余时间
        #     for task in regular_tasks:
        #         if today_hours < self.__max_hour_daily:
        #             hours_to_assign = min(1, self.__max_hour_daily - today_hours)  # RegularTask通常每天分配固定时间
        #             today_schedule.append((task.name, hours_to_assign))
        #             today_hours += hours_to_assign
        #             remaining_hours = self.__max_hour_daily - today_hours
        #         if today_hours >= self.__max_hour_daily:
        #             break
        #
        #     day_index += 1
        #     print("DDL sorting completed.")

    def rr_sorting(self):
        sorted_tasks = list(self.__ongoing_task.values()).sort(key=lambda x: x.hour_per_day(), reverse=True)


