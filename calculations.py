class TriangleCalculator:
    """Класс вычислений / валидации (реализация ЛР1 для треугольника)."""

    def calculate(self, a_str, b_str, c_str):
        """
        Возвращает кортеж (тип_треугольника, сообщение_об_ошибке).
        Если ошибки нет — второй элемент равен пустой строке.
        """
        try:
            a = float(a_str)
            b = float(b_str)
            c = float(c_str)
        except (ValueError, TypeError):
            return "", "Нечисловые данные"

        if a <= 0 or b <= 0 or c <= 0:
            return "не треугольник", "Стороны должны быть положительными"

        if a + b <= c or a + c <= b or b + c <= a:
            return "не треугольник", "Нарушено неравенство треугольника"

        if a == b == c:
            return "равносторонний", ""
        if a == b or b == c or a == c:
            return "равнобедренный", ""
        return "разносторонний", ""