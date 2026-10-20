from abc import ABC, abstractmethod


class UserInterface(ABC):
    """Абстрактный интерфейс взаимодействия с пользователем."""

    @abstractmethod
    def get_input(self):
        """Возвращает кортеж строк (a, b, c)."""
        raise NotImplementedError

    @abstractmethod
    def show_result(self, message: str) -> None:
        """Показывает результат пользователю."""
        raise NotImplementedError


class ConsoleUserInterface(UserInterface):
    """Консольная реализация."""

    def get_input(self):
        a = input("Сторона A: ")
        b = input("Сторона B: ")
        c = input("Сторона C: ")
        return a, b, c

    def show_result(self, message: str) -> None:
        print(message)