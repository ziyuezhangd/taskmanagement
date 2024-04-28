import math
from datetime import date, timedelta
from task import Task, StudyTask, RegularTask
from datetime import datetime
from operator import attrgetter
import time
import math


class TaskManagement:
    def __init__(self):
        self.__ongoing_task = {}
        self.__completed_task = {}
        self.__starting = date.today()
        self.__schedule = []
        self.__mode = 1  # 1 means sorting by deadline, 2 means round-robin style
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

        print(f"Task '{name}' added successfully.")

    def __check_urgency(self, hours_needed, deadline):
        today = datetime.today().date()
        deadline_date = datetime.strptime(deadline, '%Y-%m-%d').date()
        days_available = (deadline_date - today).days
        total_hours_available = days_available * self.__max_hour_daily
        total_hours_with_overtime = days_available * 24

        urgent = hours_needed > total_hours_available
        impossible = hours_needed > total_hours_with_overtime

        return urgent, impossible


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
                            completed_task = self.__ongoing_task.pop(task_name)
                            self.__completed_task.update({task_name: completed_task})
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
            day_index = (day - self.__starting).days
            if day_index < len(self.__schedule):
                daily_schedule = self.__schedule[day_index]

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
        if len(self.__ongoing_task) == 0:
            print("No task in the task board. Please add some tasks.")
        else:
            if self.__mode == 1:
                self.ddl_sorting()
            elif self.__mode == 2:
                self.rr_sorting()
        # 生成一个每日任务安排的sequence
        # 两种算法/mode：1按ddl排序，2round robin（且需满足ddl）
        # 优先满足StudyTask，剩余时间满足RegularTask
        # 如果ddl紧张，一天可以超过daily_working_hour（但不能超过24）

    def ddl_sorting(self):
        sorted_tasks = sorted(self.__ongoing_task.values(),
                              key=lambda task: task.deadline if isinstance(task, StudyTask) else date.max)

        # Initialize variables for schedule generation
        current_day_index = 0

        # Reset the schedule
        self.__schedule = [set() for _ in range(30)]

        # Iterate through each task and allocate time to it
        for task in sorted_tasks:
            if isinstance(task, StudyTask):
                hours_needed = task.hour_left
                days_to_deadline = max((task.deadline - date.today()).days, 1)  # Ensure at least 1 day to deadline

                # Calculate necessary daily hours to meet the deadline
                necessary_daily_hours = hours_needed / days_to_deadline

                # Check if the task requires more hours than the typical max daily hours
                if necessary_daily_hours > self.__max_hour_daily:
                    available_hours = min(24, necessary_daily_hours)  # Allow up to 24 hours if necessary
                else:
                    available_hours = self.__max_hour_daily

                while hours_needed > 0 and current_day_index < 30:
                    hours_today = min(hours_needed, available_hours)
                    self.__schedule[current_day_index].add((task.name, hours_today))
                    hours_needed -= hours_today
                    # Reduce available hours for the day or move to next day
                    if hours_needed > 0:
                        current_day_index += 1
                        if necessary_daily_hours > self.__max_hour_daily:
                            available_hours = min(24, necessary_daily_hours)  # Recalculate if still urgent
                        else:
                            available_hours = self.__max_hour_daily
                if hours_needed > 0:
                    print(f"Warning: Task '{task.name}' cannot be completed by its deadline.")
            else:
                # Regular tasks are continuously scheduled every day for their minimum hours
                for day_index in range(30):
                    total_hours_assigned = sum(hours for _, hours in self.__schedule[day_index])
                    if total_hours_assigned < self.__max_hour_daily:
                        remaining_hours = self.__max_hour_daily - total_hours_assigned
                        hours_to_add = min(task.hour, remaining_hours)
                        self.__schedule[day_index].add((task.name, hours_to_add))

        # Notify that the scheduling has been updated
        print("Schedule updated with deadline sorting.")


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
        # 从today开始往后安排任务
        # 清空之前安排时在Task中的记录
        for task in self.__ongoing_task.values():
            if isinstance(task, StudyTask):
                task.hour_scheduled = 0
        # 记录当前安排的日期
        schedule_date = date.today()
        index = (schedule_date - self.__starting).days
        # 把所有任务按每天所需时长排序
        # 先按平均小时排序
        sorted_tasks = list(sorted(self.__ongoing_task.values(),
                                   key=lambda x: x.get_hour_per_day_schedule(schedule_date),
                                   reverse=True))
        # 再按ddl调整，同时调整regular（仅需调整一次，后面sort的时候相对位置保持不变）
        for i in range(1, len(sorted_tasks)):
            if sorted_tasks[i].get_hour_per_day_schedule(schedule_date) == sorted_tasks[i-1].get_hour_per_day_schedule(schedule_date):
                if isinstance(sorted_tasks[i-1], RegularTask):
                    sorted_tasks[i], sorted_tasks[i-1] = sorted_tasks[i-1], sorted_tasks[i]
                elif isinstance(sorted_tasks[i], StudyTask) and sorted_tasks[i-1].deadline > sorted_tasks[i].deadline:
                    sorted_tasks[i], sorted_tasks[i - 1] = sorted_tasks[i - 1], sorted_tasks[i]
            i += 1

        # 当没有未安排完的study任务时退出循环
        while any(isinstance(task, StudyTask) for task in sorted_tasks):
            if len(self.__schedule) < index:
                # 中间有间断，不应存在这种情况
                for i in range(len(self.__schedule), index):
                    self.__schedule.append(set())
            # 安排一天的任务
            daily_plan = set()
            daily_hour = 0
            for task in sorted_tasks:
                # 当天的任务量超过max hour就停止安排（继续遍历检查是否有ddl临近的任务）
                if self.__max_hour_daily <= daily_hour:
                    # 如果有ddl当天的任务，必须安排
                    if isinstance(task, RegularTask) or task.deadline != schedule_date:
                        continue
                hour_task = math.ceil(task.get_hour_per_day_schedule(schedule_date))
                # 添加任务到当天
                if isinstance(task, StudyTask):
                    if task.deadline == schedule_date:
                        hour_task = task.hour_left - task.hour_scheduled
                    else:
                        hour_task = min(hour_task, task.hour_left - task.hour_scheduled,
                                        self.__max_hour_daily - daily_hour)
                else:
                    hour_task = min(hour_task, self.__max_hour_daily - daily_hour)
                daily_plan.add((task.name, hour_task))
                daily_hour += hour_task
                # 更新该任务的安排情况
                if isinstance(task, StudyTask):
                    task.hour_scheduled += hour_task
            # 如超时，检查当天的任务是否有可以推迟的
            print(daily_hour)
            if daily_hour > self.__max_hour_daily:
                modify_tasks = set()
                for task_name, hour in daily_plan:
                    # 检查regular
                    if isinstance(self.__ongoing_task.get(task_name), RegularTask):
                        while hour != 0 and daily_hour > self.__max_hour_daily:
                            hour -= 1
                            daily_hour -= 1
                        modify_tasks.add((task_name, hour))
                    if daily_hour <= self.__max_hour_daily:
                        break
            # 将当天任务安排添加到总安排列表中
            if len(self.__schedule) == index:
                # 之前的schedule正好只排到前一天（或初始状态：schedule为空，第一次安排）
                self.__schedule.append(daily_plan)
            elif len(self.__schedule) > index:
                # 之前的schedule已经排好，需从中间修改今天及之后的安排
                self.__schedule[index] = daily_plan

            # 更新schedule_date和index，重新排序，准备开启下一天的安排
            schedule_date += timedelta(days=1)
            index += 1
            # 从待安排任务列表中清除已经安排完成的任务，保留所有regular
            sorted_tasks = list(filter(lambda x: isinstance(x, RegularTask) or x.hour_scheduled < x.hour_left,
                                       sorted_tasks))
            sorted_tasks.sort(key=lambda x: x.get_hour_per_day_schedule(schedule_date), reverse=True)



