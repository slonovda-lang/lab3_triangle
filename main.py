from calculations import TriangleCalculator
from database import TriangleDatabase
from user_interface import ConsoleUserInterface
from notifier import EmailNotifier
from controller import Controller


def main():
    db = TriangleDatabase("triangles.db")  # файловая БД
    controller = Controller(
        calculator=TriangleCalculator(),
        database=db,
        user_interface=ConsoleUserInterface(),
        notifier=EmailNotifier(),
    )
    try:
        while True:
            controller.process()
            again = input("Ещё раз? (y/n): ").strip().lower()
            if again != "y":
                break
    finally:
        db.close()


if __name__ == "__main__":
    main()

# python -m unittest discover -s tests -v