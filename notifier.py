from abc import ABC, abstractmethod


class ExternalNotifier(ABC):
    """Абстрактный интерфейс сторонней зависимости."""

    @abstractmethod
    def send(self, message: str) -> bool:
        """Имитация передачи строки на внешний процесс."""
        raise NotImplementedError


class EmailNotifier(ExternalNotifier):
    """Имитация отправки результата по email."""

    def __init__(self):
        self.sent_messages = []

    def send(self, message: str) -> bool:
        # Имитация: просто сохраняем сообщение в список
        self.sent_messages.append(message)
        return True