from datetime import date, timedelta


# 数据结构
# taskboard是一个hash table - dictionary (key: task name, value: object task)
# 所有的schedule是一个sequence - list
# 每天的schedule是一个set
# 每项任务在每天的安排是一个tuple
# 算法：sorting，round robin

class TaskManagement:
    def __init__(self):
        self.__ongoing_task__ = {}
        self.__completed_task__ = {}
        self.__starting__ = date.today()
        self.__schedule__ = []
        self.__mode__ = 2  # 1 means sorting by deadline, 2 means round-robin style
        self.__max_hour_daily__ = 4


    def add_task(self, task):
        self.__ongoing_task__.update({task.name: task})

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

    #UI部分：
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
            completed = input(f"Did you complete '{task_name}' for {hours} hours today? (yes/no): ").lower()

            if completed == 'yes':
                # 任务完成，减去相应的小时数
                task = self.__ongoing_task__[task_name]
                task.hour_left -= hours
                # 如果任务完成，小时数小于等于0，从任务板删除任务
                if task.hour_left <= 0:
                    self.delete_task(task_name)
            else:
                # 如果未完成，加入到任务排序算法中

                print(f"Task '{task_name}' not completed and needs re-scheduling.")

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
        self.__mode__ = int(input("Enter mode (1 for DDL sorting, 2 for Round Robin): "))
        print(f"Mode set to {'DDL sorting' if self.__mode__ == 1 else 'Round Robin'}.")

    def set_daily_workinghours(self):
        self.__max_hour_daily__ = int(input("Enter daily working hours (1-24): "))
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



    def ui(self):
        print("Welcome to task management!")
        print("Select:")
        print("1 Display task board")
        print("2 Add task")
        print("3 Delete task")
        print("4 Show today's schedule")
        print("5 Today's feedback")
        print("6 Show this week's schedule")
        print("7 Set mode")
        print("8 Set daily working hours")
        print("9 Statistics")  # 展示所有临近的ddl和任务完成百分比
        choice = input()
        if choice == "1":
            for task_name, task in self.__ongoing_task__.items():
                print(f"{task_name}: {task.hour} hours remaining")
        elif choice == "2":
            # Add task 的实现
            pass
        elif choice == "3":
            task_name = input("Enter the name of the task to delete: ")
            self.delete_task(task_name)
        elif choice == "4":
            self.show_today_schedule()
        elif choice == "5":
            self.today_feedback()
        elif choice == "6":
            self.show_week_schedule()
        elif choice == "7":
            self.set_mode()
        elif choice == "8":
            self.set_daily_workinghours()
        elif choice == "9":
            self.statistics()
        else:
            print("Invalid choice. Please try again.")


class Task:
    def __init__(self, name, hour):
        self.name = name
        self.hour = hour
        self.hour_left = hour
class StudyTask(Task):
    def __init__(self, name, hour, deadline):
        super().__init__(name, hour)
        self.deadline = deadline
class RegularTask(Task):
    def __init__(self, name, hour, dailyhour):
        super().__init__(name, hour)
        self.dailyhour = dailyhour


task1 = StudyTask("SE project", "study", 10, 27)

taskmanagement.add_task(task1.name, task1)
seq = [[("SE project", 2), ("Reading", 3)],[],[]]
today = 21
seq[today-taskmanagement.start_day]

# main方法
taskmanagement = TaskManagement()
while True:
    taskmanagement.ui()
