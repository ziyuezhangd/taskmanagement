from scheduler import TaskManagement
import sys


def main():
    manager = TaskManagement()

    print("Welcome to Task Scheduler!")
    print("Before we start, please set the working mode and daily working hours.")
    print("You can re-modify them anytime.\n")

    # Ask the user if they need to set the working mode and daily working hours
    manager.set_mode()
    manager.set_max_daily_hours()

    while True:
        print('-' * 30)
        print(f"Welcome to task management! Today is {manager.get_today()}")
        print("Select:")
        print("1 Display task board")
        print("2 Add task")
        print("3 Delete task")
        print("4 Show today's schedule")
        print("5 Today's feedback")
        print("6 Show this week's schedule")
        print("7 Set mode")
        print("8 Set maximum daily working hours")
        print("9 Exit")
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
            manager.set_max_daily_hours()
        elif choice == "9":
            sys.exit()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
