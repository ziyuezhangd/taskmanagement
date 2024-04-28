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
    ongoing_tasks = manager.get_ongoing_tasks()

    while True:
        print('-' * 30)
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
        print("10 Regenerate schedule")  # 添加一个选项用于重新生成日程

        print('-' * 30)
        choice = input()
        if choice == "1":
            manager.show_task_board()
        elif choice == "2":
            manager.add_task()
        elif choice == "3":
            manager.delete_task()
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
        elif choice == "10":
            manager.generate_schedule()
            print("Schedule regenerated.")
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
