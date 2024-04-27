from datetime import date
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
        if choice == 1:
            pass
        else:
            pass


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
while(True):
    taskmanagement = TaskManagement()
    taskmanagement.ui()
