class Controller:
    """Бизнес-логика сквозного сценария."""

    def __init__(self, calculator, database, user_interface, notifier):
        self.calculator = calculator
        self.database = database
        self.ui = user_interface
        self.notifier = notifier

    def process(self):
        # 1. Получить ввод через UI
        a_str, b_str, c_str = self.ui.get_input()

        # 2. Попытаться получить запись из БД
        db_key = None
        try:
            db_key = (float(a_str), float(b_str), float(c_str))
        except (ValueError, TypeError):
            db_key = None  # нечисловые данные нельзя сохранить в БД

        cached = self.database.get(*db_key) if db_key else None

        # 3. Есть в БД — берём оттуда; нет — вычисляем и сохраняем
        if cached is not None:
            triangle_type, error = cached
        else:
            triangle_type, error = self.calculator.calculate(a_str, b_str, c_str)
            if db_key is not None:
                self.database.add(*db_key, triangle_type, error)

        # 4. Отправить результат во внешнюю зависимость
        if error:
            result_string = f"Ошибка: {error}"
        else:
            result_string = f"Тип треугольника: {triangle_type}"
        self.notifier.send(result_string)

        # 5. Показать результат пользователю
        self.ui.show_result(result_string)

        return triangle_type, error