from scheduler import TaskManagement
from task import StudyTask, RegularTask
from datetime import datetime

#用户交互
def main():
    manager = TaskManagement()

    print("Welcome to Task Scheduler!")
    print("Before we start, you need to set the working mode and daily working hours.")
    print("But you can modify them later.")

    # 在开始前强制用户设置工作模式和每日工作小时数
    manager.set_mode()
    manager.set_daily_workinghours()

    while True:
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
            for task_name, task in manager.__ongoing_task__.items():
                print(f"{task_name}: {task.hour} hours remaining")
        elif choice == "2":
            manager.add_task()
        elif choice == "3":
            task_name = input("Enter the name of the task to delete: ")
            manager.delete_task(task_name)
        elif choice == "4":
            manager.show_today_schedule()
        elif choice == "5":
            manager.today_feedback()
        elif choice == "6":
            manager.show_week_schedule()
        elif choice == "7":
            manager.set_mode()
        elif choice == "8":
            manager.set_daily_workinghours()
        elif choice == "9":
            manager.statistics()
        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    main()
