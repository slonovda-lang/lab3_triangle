import unittest
from unittest.mock import MagicMock

from calculations import TriangleCalculator
from database import TriangleDatabase
from user_interface import UserInterface
from notifier import ExternalNotifier
from controller import Controller


# ============================================================
#  ЮНИТ-ТЕСТЫ (не интеграционные)
# ============================================================

class TestCalculatorUnit(unittest.TestCase):
    """Юнит-тест класса вычислений."""

    def test_valid_triangle_returns_correct_type(self):
        calc = TriangleCalculator()
        ttype, err = calc.calculate("5", "5", "8")
        self.assertEqual(ttype, "равнобедренный")
        self.assertEqual(err, "")

    def test_non_numeric_input_returns_error(self):
        calc = TriangleCalculator()
        ttype, err = calc.calculate("x", "1", "1")
        self.assertEqual(ttype, "")
        self.assertNotEqual(err, "")


class TestDatabaseUnit(unittest.TestCase):
    """Юнит-тест класса БД: add / get / delete."""

    def setUp(self):
        self.db = TriangleDatabase(":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_get_delete_cycle(self):
        self.assertTrue(self.db.add(3.0, 4.0, 5.0, "разносторонний", ""))
        self.assertEqual(self.db.get(3.0, 4.0, 5.0),
                         ("разносторонний", ""))
        self.assertTrue(self.db.delete(3.0, 4.0, 5.0))
        self.assertIsNone(self.db.get(3.0, 4.0, 5.0))


# ============================================================
#  ИНТЕГРАЦИОННЫЕ ТЕСТЫ
#  Комбинируем Controller + Calculator + Database + UI/Notifier.
#  Пользовательский ввод и «внешний сервер» — заглушки (mock).
# ============================================================

class TestControllerIntegration(unittest.TestCase):

    def setUp(self):
        # Реальные компоненты
        self.db = TriangleDatabase(":memory:")
        self.calc = TriangleCalculator()

        # Заглушки
        self.ui_mock = MagicMock(spec=UserInterface)          # имитация ввода
        self.notifier_mock = MagicMock(spec=ExternalNotifier) # имитация сервера

        self.controller = Controller(
            calculator=self.calc,
            database=self.db,
            user_interface=self.ui_mock,
            notifier=self.notifier_mock,
        )

    def tearDown(self):
        self.db.close()

    # ---------- ИТ-1: новая запись вычисляется и сохраняется ----------
    def test_new_input_calculated_saved_and_sent(self):
        self.ui_mock.get_input.return_value = ("3", "4", "5")

        ttype, err = self.controller.process()

        # Контроллер вернул правильный результат
        self.assertEqual(ttype, "разносторонний")
        self.assertEqual(err, "")

        # Реальная БД содержит новую запись
        self.assertEqual(self.db.get(3.0, 4.0, 5.0),
                         ("разносторонний", ""))

        # Заглушка notifier'а получила сообщение
        self.notifier_mock.send.assert_called_once_with(
            "Тип треугольника: разносторонний")

        # Заглушка UI показала результат
        self.ui_mock.show_result.assert_called_once()

    # ---------- ИТ-2: повторный вызов берёт данные из БД ----------
    def test_second_call_uses_database_cache(self):
        self.ui_mock.get_input.return_value = ("6", "8", "10")

        # Первый вызов — вычисляет и сохраняет
        self.controller.process()

        # Подменяем калькулятор spy-объектом: он НЕ должен быть вызван
        spy_calc = MagicMock(wraps=self.calc)
        self.controller.calculator = spy_calc

        # Второй вызов — берёт из кеша БД
        self.controller.process()

        spy_calc.calculate.assert_not_called()
        self.assertEqual(self.notifier_mock.send.call_count, 2)

    # ---------- ИТ-3: некорректный треугольник — уходит ошибка ----------
    def test_invalid_triangle_sends_error_message(self):
        self.ui_mock.get_input.return_value = ("1", "1", "5")

        ttype, err = self.controller.process()

        self.assertEqual(ttype, "не треугольник")
        self.assertNotEqual(err, "")

        # В БД запись всё равно сохранена (числовые данные)
        self.assertIsNotNone(self.db.get(1.0, 1.0, 5.0))

        # Строка-результат содержит «Ошибка»
        sent_message = self.notifier_mock.send.call_args[0][0]
        self.assertIn("Ошибка", sent_message)

    # ---------- ИТ-4: нечисловые данные → ошибка, но в БД НЕ пишем ----------
    def test_non_numeric_input_not_saved_to_db(self):
        self.ui_mock.get_input.return_value = ("abc", "def", "ghi")

        ttype, err = self.controller.process()

        self.assertEqual(ttype, "")
        self.assertNotEqual(err, "")

        # В БД ничего не должно быть — невалидный ключ нельзя сохранить
        rows = self.db.conn.execute(
            "SELECT COUNT(*) FROM triangles").fetchone()
        self.assertEqual(rows[0], 0)

        self.notifier_mock.send.assert_called_once()


if __name__ == "__main__":
    unittest.main()