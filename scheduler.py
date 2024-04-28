from datetime import date, timedelta
from task import Task, StudyTask, RegularTask
from datetime import datetime
class TaskManagement:
    def __init__(self):
        self.__ongoing_task__ = {}
        self.__completed_task__ = {}
        self.__starting__ = date.today()
        self.__schedule__ = []
        self.__mode__ = 2  # 1 means sorting by deadline, 2 means round-robin style
        self.__max_hour_daily__ = 4


    def add_task(self):
        valid_task_types = ['study', 'regular']
        task_type = input("Enter task type (study/regular): ").lower()

        while task_type not in valid_task_types:
            print("Invalid task type. Please enter 'study' or 'regular'.")
            task_type = input("Enter task type (study/regular): ").lower()

        name = input("Enter task name: ")
        hours = self.__get_valid_hours("Enter total hours needed: ")

        # 如果任务已经存在（同名同类）：
        if name in self.__ongoing_task__ and isinstance(self.__ongoing_task__[name], StudyTask if task_type == "study" else RegularTask):
            existing_task = self.__ongoing_task__[name]
            print(f"Task '{name}' already exists with {existing_task.hour_left} hours remaining.")
            additional_hours = self.__get_valid_hours(int(input("Enter additional hours to add (enter 0 to keep as is): ")), minimum=0)
            if additional_hours > 0:
                existing_task.hour_left += additional_hours
                print(f"Updated hours for task '{name}': {existing_task.hour_left} hours remaining.")
                # 旧任务时间增加，需要重新schedule

            return

        if task_type == "study":
            deadline = self.__get_valid_date("Enter deadline (YYYY-MM-DD): ")
            task = StudyTask(name, hours, deadline)
        elif task_type == "regular":
            daily_hours = self.__get_valid_hours("Enter daily minimum hours: ", minimum=1)
            task = RegularTask(name, hours, daily_hours)

        self.__ongoing_task__[task.name] = task
        print(f"Task '{task.name}' added successfully.")


    def delete_task(self, task_name):
        if task_name in self.__ongoing_task__:
            del self.__ongoing_task__[task_name]
            print(f"Task '{task_name}' has been deleted from the taskboard.")
        else:
            print(f"Task '{task_name}' is not in the taskboard.")



    def show_today_schedule(self):
        today = date.today()  # 获取今天的日期
        today_index = (today - self.__starting__).days
        if today_index < 0 or today_index >= len(self.__schedule__):
            print("Today's schedule is not available.")
            return
        today_schedule = self.__schedule__[today_index] if today_index < len(self.__schedule__) else []
        print("Today's schedule:")
        for task in today_schedule:
            print(f"Task: {task[0]}, Hours: {task[1]}")

    def today_feedback(self):
        today = date.today()
        today_index = (today - self.__starting__).days
        if today_index < 0 or today_index >= len(self.__schedule__):
            print("Today's schedule is not available.")
            return

        today_schedule = self.__schedule__[today_index]

        for task_tuple in today_schedule:
            task_name, hours = task_tuple
            while True:
                completed = input(f"Did you complete '{task_name}' for {hours} hours today? (yes/no): ").lower()
                if completed == 'yes':
                    # 任务完成，移除任务
                    self.delete_task(task_name)
                    print(f"Task '{task_name}' completed and removed.")
                    break
                elif completed == 'no':
                    # 问还想不想继续
                    while True:
                        completed_hours = self.__get_valid_hours(int(input(f"How many hours did you complete for '{task_name}' today? (-1 to abandon task, 0 or positive number for hours completed): ")), minimum=-1)
                        if completed_hours == -1:
                            # 用户选择放弃任务
                            self.delete_task(task_name)
                            print(f"Task '{task_name}' abandoned and removed.")
                            break
                        elif completed_hours >= 0 and completed_hours <= hours:
                            # 更新任务剩余小时数
                            task = self.__ongoing_task__[task_name]
                            task.hour_left -= completed_hours
                            print(f"Updated task '{task_name}': {task.hour_left} hours remaining.")
                            if task.hour_left <= 0:
                                self.delete_task(task_name)
                                print(f"Task '{task_name}' completed and removed.")
                            break
                        else:
                            print(f"Invalid number of hours. Please enter a number between -1 and {hours}.")

                    break
                else:
                    print("Invalid input. Please answer 'yes' or 'no'.")

            # completed = input(f"Did you complete '{task_name}' for {hours} hours today? (yes/no): ").lower()
            #
            # if completed == 'yes':
            #     # 任务完成，减去相应的小时数
            #     task = self.__ongoing_task__[task_name]
            #     task.hour_left -= hours
            #     # 如果任务完成，小时数小于等于0，从任务板删除任务
            #     if task.hour_left <= 0:
            #         self.delete_task(task_name)
            # else:
            #     # 如果未完成，加入到任务排序算法中
            #
            #     print(f"Task '{task_name}' not completed and needs re-scheduling.")



    def show_week_schedule(self):
        print("This week's schedule :")
        for i in range(7):  # 显示接下来7天的日程
            day = self.__starting__ + timedelta(days=i)
            if i < len(self.__schedule__):
                daily_schedule = self.__schedule__[i]
                print(f"Day {day}: {daily_schedule}")
            else:
                print(f"Day {day}: No tasks scheduled.")

    def set_mode(self):
        # self.__mode__ = int(input("Enter mode (1 for DDL sorting, 2 for Round Robin): "))
        # print(f"Mode set to {'DDL sorting' if self.__mode__ == 1 else 'Round Robin'}.")
        while True:
            mode_input = input("Enter mode (1 for DDL sorting, 2 for Round Robin): ")
            if mode_input.isdigit() and mode_input in ['1', '2']:
                self.__mode__ = int(mode_input)
                mode_name = 'DDL sorting' if self.__mode__ == 1 else 'Round Robin'
                print(f"Mode set to {mode_name}.")
                break
            else:
                print("Invalid input. Please enter '1' for DDL sorting or '2' for Round Robin.")


    def set_daily_workinghours(self):
        self.__max_hour_daily__ = self.__get_valid_hours(int(input("Enter daily working hours (1-24): ")))
        print(f"Daily working hours set to {self.__max_hour_daily__}.")

    def statistics(self):
        if not self.__ongoing_task__:
            print("No tasks available")
            return

        print("Task Statistics:")
        for task_name, task in self.__ongoing_task__.items():
            if hasattr(task, 'deadline'):  # StudyTask 有截止日期
                deadline_str = f"Deadline: Day {task.deadline}"
            else:
                deadline_str = "No specific deadline"  # RegularTask 可能没有截止日期

            if task.hour > 0:
                completion_percentage = (task.hour - task.hour_left) / task.hour * 100
            else:
                completion_percentage = 100  # 防止除以零

            print(f"{task_name} - {deadline_str}, Completion: {completion_percentage:.2f}%")



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
        if self.__mode__ == 1:
            self.ddl_sorting()
        elif self.__mode__ == 2:
            self.rr_sorting()
        # 生成一个每日任务安排的sequence
        # 两种算法/mode：1按ddl排序，2round robin（且需满足ddl）
        # 优先满足StudyTask，剩余时间满足RegularTask
        # 如果ddl紧张，一天可以超过daily_working_hour（但不能超过24）
        pass

    def ddl_sorting(self):
        pass

    def rr_sorting(self):
        pass
